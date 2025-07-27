from __future__ import annotations

import functools
import traceback as tb
import typing as t

import click

if t.TYPE_CHECKING:
    from click.decorators import FC


def traceback(
    func: t.Optional[t.Callable] = None,
    exitcode: t.Optional[int] = 3,
    param_decls: t.Optional[t.List[str]] = None,
) -> t.Union[FC, t.Callable[[FC], FC]]:
    """Decorator to catch all unhandled exception and print optionally the traceback."""

    if not param_decls:
        param_decls = ["--traceback"]

    def decorator(func):
        @click.option(
            *param_decls,
            is_flag=True,
            help="Show the full traceback in case of an error.",
        )
        @functools.wraps(func)
        def wrapper(*args, traceback, **kwargs):

            try:
                result = func(*args, **kwargs) or 0
            except (Exception, KeyboardInterrupt) as e:
                result = exitcode

                if traceback:
                    message = tb.format_exc()
                else:
                    message = str(e)
                click.echo(message, err=True)
            finally:
                raise SystemExit(result)

        return wrapper

    return decorator(func) if callable(func) else decorator
