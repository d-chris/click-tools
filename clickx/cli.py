import typing as t
from pathlib import Path

import click

from .decorators import traceback


def icon(
    picture: str,
    icon: t.Optional[str] = None,
    size: t.Optional[tuple[int]] = None,
) -> int:
    """convert a image to an icon with multiple sizes."""

    pic = Path(picture)
    ico = Path(icon) if icon else pic.with_suffix(".ico")
    siz = size if size else (64, 128, 256)

    try:
        from PIL import Image

        exitcode = 0 if ico.is_file() else 1

        img = Image.open(pic)
        img.save(ico, format="ICO", sizes=[(s, s) for s in siz])

        if not ico.is_file():
            exitcode = 1

        print(str(ico))
    except ModuleNotFoundError:
        print("pip install click-tools[pillow]")

        exitcode = 2

    return exitcode


@click.command(help=icon.__doc__)
@click.argument(
    "picture",
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "-i",
    "--icon",
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Output icon file name.",
)
@click.option(
    "-s",
    "--size",
    default=(64, 128, 256),
    show_default=True,
    multiple=True,
    help="Multiple sizes for the icon.",
)
@traceback
def cli_icon(**kwargs):
    return icon(**kwargs)
