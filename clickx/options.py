from __future__ import annotations

import importlib.metadata
import typing as t

import click

from .types import PackageIcon

if t.TYPE_CHECKING:
    from click.decorators import FC


def version(
    package_name: str,
    url: t.Optional[str] = None,
    **kwargs,
) -> t.Callable[[FC], FC]:

    def decorator(func):

        if package_name is not None and "message" not in kwargs:

            def homepage():
                metadata = importlib.metadata.metadata(package_name)
                return metadata.get("Home-page") or metadata.get("Project-URL") or ""

            kwargs["message"] = f"%(prog)s, version %(version)s\n{url or homepage()}"

        return click.version_option(
            package_name=package_name,
            **kwargs,
        )(func)

    return decorator


def icon(
    filename: str,
    package: t.Optional[str] = None,
) -> t.Callable[[FC], FC]:

    return click.option(
        "--icon",
        type=PackageIcon(filename, package, exitcode=0),
        is_flag=True,
        is_eager=True,
        expose_value=False,
        help="Show path to the package icon.",
    )
