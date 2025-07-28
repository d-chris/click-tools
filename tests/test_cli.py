import pytest
from click.testing import CliRunner

from clickx.__main__ import cli
from clickx.cli import icon


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


def test_cli_icon(tmp_path) -> None:
    """Test the icon command."""
    icon_path = tmp_path / "clickx.ico"

    command = [
        "icon",
        "--icon",
        str(icon_path),
        "clickx.png",
    ]

    runner = CliRunner()
    result = runner.invoke(cli, command)

    assert result.exit_code == 1
    assert str(icon_path) in result.output

    result = runner.invoke(cli, command)
    assert result.exit_code == 0
    assert str(icon_path) in result.output


def test_icon_nopillow(capsys, mocker):
    mocker.patch.dict("sys.modules", {"PIL": None})

    result = icon("clickx.png")
    stdout, _ = capsys.readouterr()

    assert result == 2
    assert "pip install click-tools[pillow]" in stdout
