import click

import clickx  # namespace for click-tools


@click.command(help="example for option.")
@clickx.version("pip")  # print version and url from packages metadata
def cli() -> None:

    click.echo(
        "Call with option `--version` to print pip version and url from metadata."
    )


if __name__ == "__main__":
    cli()
