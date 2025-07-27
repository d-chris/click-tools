from __future__ import annotations

import importlib.metadata
import sys
import typing as t

import click

from .types import PackageIcon

if t.TYPE_CHECKING:
    from click.decorators import FC


def version(
    distirbution_name: str,
    url: t.Optional[str] = None,
    **kwargs,
) -> t.Callable[[FC], FC]:
    """
    A variant of `click.version_option` that also prints the homepage URL from
    the package metadata.
    """

    def decorator(func):

        if distirbution_name is not None and "message" not in kwargs:

            def homepage():

                try:
                    metadata = importlib.metadata.metadata(distirbution_name)
                except importlib.metadata.PackageNotFoundError as e:
                    if getattr(sys, "frozen", False):
                        raise RuntimeError(
                            "\n".join(
                                [
                                    "Package metadata not found in executable.",
                                    f'Add "--copy-metadata={distirbution_name}"'
                                    "to the pyinstaller command.",
                                ]
                            )
                        ) from e

                    raise e

                return metadata.get("Home-page") or metadata.get("Project-URL") or ""

            kwargs["message"] = f"%(prog)s, version %(version)s\n{url or homepage()}"

        return click.version_option(
            package_name=distirbution_name,
            **kwargs,
        )(func)

    return decorator


def icon(
    filename: str,
    distribution_name: t.Optional[str] = None,
    param_decls: t.Optional[t.List[str]] = None,
) -> t.Callable[[FC], FC]:
    """
    Option for displaying the path to the package icon. If the package is frozen, e.g.
    with `pyinstaller`, the path to the executable will be returned.
    """

    if not param_decls:
        param_decls = ["--icon"]

    return click.option(
        *param_decls,
        type=PackageIcon(filename, distribution_name, exitcode=0),
        is_flag=True,
        is_eager=True,
        expose_value=False,
        help="Show path to the package icon.",
    )
