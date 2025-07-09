import click

import clickx
from clickx.cli import cli_icon


@click.group()
@clickx.icon("clickx.ico", "clickx")
@clickx.version("click_tools")
def cli() -> None:
    pass


cli.add_command(cli_icon, name="icon")

if __name__ == "__main__":
    cli()
