import importlib.resources
import sys
import typing as t
from pathlib import Path

import click


class PackageIcon(click.ParamType):
    name = "ICON"

    def __init__(
        self,
        filename: t.Optional[str] = None,
        package: t.Optional[str] = None,
        exitcode: t.Optional[int] = None,
    ):
        self._filename = filename
        self._package = package or __package__
        self._exitcode = exitcode

    def convert(self, value, param, ctx):
        # value here is the flag‐value (True or False)
        if value is False:
            # If the flag is not set, we return None
            return value

        # exactly the same logic you had in your callback:
        try:
            if getattr(sys, "frozen", False):
                file = sys.executable
            else:
                if self._package is None:
                    raise ctx.fail("'package_name' name is missing.")

                filename = value if isinstance(value, str) else self._filename

                with importlib.resources.path(self._package, filename) as icon_file:
                    file = icon_file

            icon = Path(file).resolve(True)

        except Exception as e:
            ctx.fail(str(e))
        else:
            if self._exitcode is not None:
                click.echo(message=str(icon), err=True)
                ctx.exit(self._exitcode)

            return icon
