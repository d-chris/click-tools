from __future__ import annotations

import contextlib as cl
import functools
import traceback as tb
import typing as t

import click

if t.TYPE_CHECKING:
    from click.decorators import FC


def param(param_decls: t.List[str]) -> str:

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

    if not param_decls:
        param_decls = ["--redirect"]

    keyword = param(param_decls)

    kwargs = {
        k: attrs.pop(k, v)
        for k, v in {
            "mode": "a+",
            "encoding": None,
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

            redirect = kwargs.pop(keyword, None)

            if redirect is None:
                return func(*args, **kwargs)

            with cl.ExitStack() as stack:
                if stdout:
                    stack.enter_context(cl.redirect_stdout(redirect))
                if stderr:
                    stack.enter_context(cl.redirect_stderr(redirect))

                try:
                    return func(*args, **kwargs)
                except:  # noqa: E722
                    if errors:
                        tb.print_exc(file=redirect)
                    raise
                finally:
                    redirect.flush()

        return wrapper

    return decorator(func) if callable(func) else decorator


def traceback(
    func: t.Optional[t.Callable] = None,
    exitcode: t.Optional[int] = 3,
    param_decls: t.Optional[t.List[str]] = None,
) -> t.Union[FC, t.Callable[[FC], FC]]:
    """Decorator to catch all unhandled exception and print optionally the traceback."""

    if not param_decls:
        param_decls = ["--traceback"]

    keyword = param(param_decls)

    def decorator(func):
        @click.option(
            *param_decls,
            is_flag=True,
            help="Show the full traceback in case of an error.",
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            traceback = kwargs.pop(keyword, False)

            try:
                result = func(*args, **kwargs) or 0
            except (Exception, KeyboardInterrupt) as e:
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
