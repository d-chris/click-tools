import click
import pytest
from click.testing import CliRunner

import clickx


@pytest.fixture
def cli():

    def cli_func(exitcode: int) -> int:
        """Dummy cli function to test decorators with."""

        message = f"cli_func({exitcode}) called."

        if exitcode < 0:
            raise RuntimeError(f"Error: {message}")

        print(message)
        return exitcode

    @click.command()
    @click.argument("arg", type=int)
    @clickx.traceback
    def cli(arg):
        return cli_func(arg)

    return cli


@pytest.mark.parametrize(
    "argument, exitcode",
    [
        ("0", 0),
        ("1", 1),
        ("-1", 3),  # raises RuntimeError
    ],
    ids=[
        "Success",
        "Failed",
        "Exception",
    ],
)
def test_traceback_func(cli, argument, exitcode):
    """Test the traceback decorator."""

    runner = CliRunner()

    result = runner.invoke(cli, ["--", argument], catch_exceptions=False)

    assert result.exit_code == exitcode


@pytest.mark.parametrize("exitcode", [-1, 0, 5], ids=lambda x: f"exitcode={x}")
@pytest.mark.parametrize("traceback", [True, False], ids=lambda x: f"traceback={x}")
def test_traceback_exitcode(exitcode, traceback):

    @click.command()
    @clickx.traceback(
        exitcode=exitcode,
    )
    def cli():
        raise RuntimeError(f"Error: pytest traceback test with exitcode {exitcode}")

    runner = CliRunner(mix_stderr=False)

    result = runner.invoke(
        cli,
        ["--traceback"] if traceback else [],
        catch_exceptions=False,
    )

    assert result.exit_code == exitcode
    assert "Error: " in result.stderr

    if traceback:
        assert result.stderr.startswith("Traceback")


@pytest.mark.parametrize(
    "param_decls",
    [
        ["-tb"],
        ["--show-traceback"],
        ["-tb", "--verbose"],
    ],
    ids=lambda x: x[-1],
)
def test_traceback_param_decls(param_decls):
    """Test the traceback decorator with custom parameter declarations."""

    @click.command()
    @clickx.traceback(param_decls=param_decls)
    def cli():
        raise RuntimeError(f"Error: pytest traceback test with {param_decls=}")

    runner = CliRunner(mix_stderr=False)

    result = runner.invoke(cli, [param_decls[-1]], catch_exceptions=False)

    assert result.exit_code == 3
    assert "Error: " in result.stderr
    assert result.stderr.startswith("Traceback")
