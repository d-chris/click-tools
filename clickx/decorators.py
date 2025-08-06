from __future__ import annotations

import contextlib as cl
import functools
import traceback as tb
import typing as t

import click

if t.TYPE_CHECKING:
    from click.decorators import FC

    ExceptionTuple = t.Tuple[t.Type[BaseException], ...]


def param(param_decls: t.List[str]) -> str:
    """
    Extract the keyword from the parameter declarations.

    `click.option()` uses first parameter with `--` as keyword for a value in `kwargs`.
    """

    try:
        keyword = next(param for param in param_decls if param.startswith("--"))
    except StopIteration:
        keyword = param_decls[0]

    return keyword.lstrip("-").replace("-", "_")


def redirect(
    func: t.Optional[t.Callable] = None,
    /,
    stdout: bool = True,
    stderr: bool = False,
    errors: bool = True,
    param_decls: t.Optional[t.List[str]] = None,
    **attrs,
) -> t.Union[FC, t.Callable[[FC], FC]]:
    """
    This decorator adds an option to a `click.command()` that allows the user to specify
    a file to which the command's output will be redirected and appended.
    """

    if not param_decls:
        param_decls = ["--redirect"]

    keyword = param(param_decls)
    exceptions: ExceptionTuple = attrs.pop("exceptions", (Exception,))

    kwargs = {
        k: attrs.pop(k, v)
        for k, v in {
            "mode": "w",
            "encoding": "utf-8",
            "errors": "strict",
            "lazy": False,
            "atomic": False,
        }.items()
    }

    attrs.setdefault("help", "Redirect console output to file.")
    attrs.setdefault("default", None)

    def decorator(func):
        @click.option(
            *param_decls,
            type=click.File(**kwargs),
            **attrs,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            redirect: t.IO = kwargs.pop(keyword, None)

            if redirect is None:
                return func(*args, **kwargs)

            with cl.ExitStack() as stack:
                if stdout:
                    stack.enter_context(cl.redirect_stdout(redirect))
                if stderr:
                    stack.enter_context(cl.redirect_stderr(redirect))

                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if errors:
                        tb.print_exception(e, file=redirect)
                    raise
                finally:
                    redirect.flush()

        return wrapper

    return decorator(func) if callable(func) else decorator


def traceback(
    func: t.Optional[t.Callable] = None,
    /,
    exitcode: t.Optional[int] = 3,
    param_decls: t.Optional[t.List[str]] = None,
    **attrs,
) -> t.Union[FC, t.Callable[[FC], FC]]:
    """Decorator to catch all unhandled exception and print optionally the traceback."""

    if not param_decls:
        param_decls = ["--traceback"]

    keyword = param(param_decls)
    exceptions: ExceptionTuple = attrs.pop("exceptions", (Exception, KeyboardInterrupt))

    attrs.setdefault("help", "Show the full traceback in case of an error.")

    def decorator(func):
        @click.option(
            *param_decls,
            is_flag=True,
            **attrs,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            traceback = kwargs.pop(keyword, False)

            try:
                result = func(*args, **kwargs) or 0
            except exceptions as e:
                result = exitcode

                if traceback:
                    message = tb.format_exc()
                else:
                    message = repr(e)
                click.echo(message, err=True)
            finally:
                raise SystemExit(result)

        return wrapper

    return decorator(func) if callable(func) else decorator
