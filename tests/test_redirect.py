import sys

import click
import pytest
from click.testing import CliRunner

import clickx


@pytest.fixture
def tmp_file(tmp_path):
    """Fixture to create a temporary file for redirection."""
    return tmp_path / "redirect.txt"


def test_noredirect():
    """Test the redirect decorator with no redirection."""

    @click.command()
    @clickx.redirect
    def cli():
        print("print to stdout.", file=sys.stdout, flush=True)
        print("print to stderr.", file=sys.stderr, flush=True)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert "stdout" in result.output
    assert "stderr" in result.stderr


def test_redirect_stdout(tmp_file):
    """Test the redirect decorator with no redirection."""

    @click.command()
    @clickx.redirect()
    def cli():
        print("print to stdout.", file=sys.stdout, flush=True)
        print("print to stderr.", file=sys.stderr, flush=True)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["--redirect", str(tmp_file)])

    assert result.exit_code == 0
    assert result.output == ""
    assert "stdout" in tmp_file.read_text()
    assert "stderr" in result.stderr


def test_redirect_stderr(tmp_file):
    """Test the redirect decorator with no redirection."""

    @click.command()
    @clickx.redirect(stdout=False, stderr=True)
    def cli():
        print("print to stdout.", file=sys.stdout, flush=True)
        print("print to stderr.", file=sys.stderr, flush=True)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["--redirect", str(tmp_file)])

    assert result.exit_code == 0
    assert "stdout" in result.output
    assert result.stderr == ""
    assert "stderr" in tmp_file.read_text()


def test_redirect_stdout_stderr(tmp_file):
    """Test the redirect decorator with no redirection."""

    @click.command()
    @clickx.redirect(stderr=True)
    def cli():
        print("print to stdout.", file=sys.stdout, flush=True)
        print("print to stderr.", file=sys.stderr, flush=True)

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["--redirect", str(tmp_file)])

    assert result.exit_code == 0
    assert result.output == ""
    assert result.stderr == ""

    content = tmp_file.read_text()

    assert "stdout" in content
    assert "stderr" in content


def test_redirect_path(tmp_path):
    @click.command()
    @clickx.redirect()
    def cli():
        pass

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["--redirect", str(tmp_path)])

    assert result.exit_code == 2, "Expected error when redirecting to a directory"
    assert "Invalid value for '--redirect':" in result.stderr


def test_noredirect_error(tmp_file):
    """Test the redirect decorator with no redirection and an error."""

    @click.command()
    @clickx.redirect(errors=False)
    def cli():
        raise RuntimeError("This is an error.")

    runner = CliRunner()
    result = runner.invoke(cli, ["--redirect", str(tmp_file)])

    assert result.exit_code == 1
    assert type(result.exception) is RuntimeError
    assert tmp_file.read_text() == ""


def test_redirect_error(tmp_file):
    """Test the redirect decorator with no redirection and an error."""

    @click.command()
    @clickx.redirect()
    def cli():
        raise RuntimeError("This is an error.")

    runner = CliRunner()
    result = runner.invoke(cli, ["--redirect", str(tmp_file)])

    assert result.exit_code == 1
    assert type(result.exception) is RuntimeError

    content = tmp_file.read_text()

    assert "Traceback (most recent call last)" in content
    assert repr(result.exception).replace("'", '"') in content


@pytest.mark.parametrize(
    "param_decls",
    [
        ["-r"],
        ["--redirect"],
        ["-l", "--log"],
    ],
    ids=lambda x: x[-1],
)
def test_redirect_param_decls(param_decls, tmp_file):
    """Test the redirect decorator with custom parameter declarations."""

    stdout = f"{param_decls[-1]} to stdout."

    @click.command()
    @clickx.redirect(param_decls=param_decls)
    def cli():
        print(stdout, flush=True)

    runner = CliRunner()
    result = runner.invoke(cli, [param_decls[-1], str(tmp_file)])

    assert result.exit_code == 0
    assert stdout in tmp_file.read_text()
