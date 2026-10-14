# click-tools

[![Pyhton](https://img.shields.io/badge/python-%5E3.9-blue?logo=python&logoColor=yellow)](https://python.org)
[![Static Badge](https://img.shields.io/badge/cli-clickx-orange?logo=gnubash&logoColor=white&label=cli)](#command-line-interface)
[![Poetry](https://img.shields.io/badge/packaging-poetry-%233B82F6?logo=poetry)](https://python-poetry.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](#pre-commit-hooks)

---

## Installation

```cmd
pip install click-tools
```

## Usage

```python
# filename: example.py

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
```

```console
$ python example.py  --version

example.py, version 26.2.1
Changelog, https://pip.pypa.io/en/stable/news/
Documentation, https://pip.pypa.io
Homepage, https://pip.pypa.io/
Source, https://github.com/pypa/pip
```

## Command Line Interface

Command line interface see help for more information.

```console
$ clickx --help

Usage: clickx [OPTIONS] COMMAND [ARGS]...

Options:
  --icon     Show path to the package icon.
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  icon  convert a image to an icon with multiple sizes.
```

## pre-commit-hooks

convert a picture to an icon using `pillow`.

```yaml
- repo: https://github.com/d-chris/click-tools
  rev: v0.1.0
  hooks:
    - id: clickx-icon
      files: clickx.png$
      args: ["--icon", "clickx/clickx.ico"]
```

## PyInstaller

> `clickx.version(package_name=PACKAGE)` uses metadata, make sure to include this into your pyinstaller command with `--copy-metadata=PACKAGE` option.

to create onefile executable with `pyinstaller` use the **build task** <ctrl+shift+b> in vscode or run the following command in terminal.

```cmd
poetry install --with build
poetry run vtr build-exe
```
