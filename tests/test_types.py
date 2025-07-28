from pathlib import Path

import click
from click.testing import CliRunner

import clickx


def test_packageicon(mocker):

    mocker.patch("clickx.types.sitepackage_dir", return_value=Path.cwd())

    @click.command()
    @clickx.icon("clickx.png")
    def cli():
        pass

    runner = CliRunner()
    result = runner.invoke(cli, ["--icon"])

    assert result.exit_code == 0
    assert "clickx.png" in result.output


def test_packageicon_frozen(mocker):

    mocker.patch("sys.frozen", True, create=True)
    mocker.patch("sys.executable", "clickx.png")

    @click.command()
    @clickx.icon("clickx.png")
    def cli():
        pass

    runner = CliRunner()
    result = runner.invoke(cli, ["--icon"])

    assert result.exit_code == 0
    assert "clickx.png" in result.output
