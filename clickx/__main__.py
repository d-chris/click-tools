from __future__ import annotations

import click

import clickx
from clickx.icon import cli as icon


@click.group()
@clickx.version("click_tools")
def cli():
    pass


cli.add_command(icon, name="icon")

if __name__ == "__main__":
    cli()
