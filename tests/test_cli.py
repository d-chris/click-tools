import pytest
from click.testing import CliRunner

from clickx.__main__ import cli
from clickx.cli import icon


@pytest.fixture
def tmp_icon(tmp_path):
    """Fixture to create a temporary icon file."""
    return tmp_path / "clickx.ico"


@pytest.mark.parametrize(
    "command",
    [
        "--help",
        "--version",
        "icon --help",
    ],
)
def test_cli_commands(command: str) -> None:
    """Test the main CLI entry point."""
    runner = CliRunner()
    result = runner.invoke(cli, command.split())
    assert result.exit_code == 0


def test_cli_icon(tmp_icon) -> None:
    """Test the icon command."""

    command = [
        "icon",
        "--icon",
        str(tmp_icon),
        "clickx.png",
    ]

    runner = CliRunner()
    result = runner.invoke(cli, command)

    assert result.exit_code == 1
    assert str(tmp_icon) in result.output

    result = runner.invoke(cli, command)
    assert result.exit_code == 0
    assert str(tmp_icon) in result.output


def test_icon_nopillow(capsys, mocker):
    mocker.patch.dict("sys.modules", {"PIL": None})

    result = icon("clickx.png")
    stdout, _ = capsys.readouterr()

    assert result == 2
    assert "pip install click-tools[pillow]" in stdout


def test_icon_no_file(capsys, tmp_icon, mocker):

    mocker.patch("pathlib.Path.is_file", return_value=False)

    result = icon("clickx.png", icon=str(tmp_icon))
    stdout, _ = capsys.readouterr()

    assert result == 1
    assert str(tmp_icon) in stdout
