# click-tools

[![Pyhton](https://img.shields.io/badge/python-%3E%3D3.9-blue?logo=python&logoColor=yellow)](https://python.org)
[![Static Badge](https://img.shields.io/badge/cli-clickx-orange?logo=gnubash&logoColor=white&label=cli)](#command-line-interface)
[![Poetry](https://img.shields.io/badge/packaging-poetry-%233B82F6?logo=poetry)](https://python-poetry.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](#pre-commit-hooks)

---

## Command Line Interface

Command line interface see help for more information.

```cmd
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
