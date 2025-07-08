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
) -> t.Union[FC, t.Callable[[FC], FC]]:
    """Decorator to catch all unhandled exception and print optionally the traceback."""

    def decorator(func):
        @click.option(
            "-tb",
            "--traceback",
            is_flag=True,
            help="Prints the full traceback in case of an error.",
        )
        @functools.wraps(func)
        def wrapper(*args, traceback, **kwargs):

            result = exitcode
            try:
                result = func(*args, **kwargs)
            except (Exception, KeyboardInterrupt) as e:
                if traceback:
                    message = tb.format_exc()
                else:
                    message = str(e)
                click.echo(message, err=True)
            finally:
                raise SystemExit(result or 0)

        return wrapper

    return decorator(func) if callable(func) else decorator
