from importlib.metadata import PackageNotFoundError

import click
import pytest

import clickx


def test_version() -> None:

    with pytest.raises(PackageNotFoundError) as e:

        @click.command()
        @clickx.version("nonexisting")
        def cli():
            pass

    assert "No package metadata was found for nonexisting" in str(e.value)


def test_version_frozen(mocker):

    mocker.patch("sys.frozen", True, create=True)

    with pytest.raises(RuntimeError) as e:

        @click.command()
        @clickx.version("nonexisting")
        def cli():
            pass

    assert "--copy-metadata=nonexisting" in str(e.value)
