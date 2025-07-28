import importlib.metadata
import importlib.resources
import typing as t
from pathlib import Path


def sitepackage_dir(distribution_name: str) -> Path:
    """
    Returns the directory of a installed package, e.g. with
    `pip install <distribution_name>`.
    """

    modulerror: t.Optional[Exception] = None

    try:
        file = importlib.resources.files(distribution_name)

        return Path(str(file))

    except ModuleNotFoundError as e:
        modulerror = e

    try:
        files = [
            file.locate()
            for file in importlib.metadata.files(distribution_name) or []
            if file.name == "__init__.py"
            and len(file.parts) == 2
            and file.parts[0].lower() != "tests"
        ]

        return Path(files[0]).parent
    except (IndexError, ModuleNotFoundError):
        pass

    try:
        dist = importlib.metadata.distribution(distribution_name)

        editable_path = Path(dist.origin.url.removeprefix("file:///")).resolve(True)  # type: ignore[attr-defined] # noqa: E501

        files = [
            file
            for file in editable_path.glob("*/__init__.py")
            if file.relative_to(editable_path).parts[0].lower() != "tests"
        ]

        return Path(files[0]).parent
    except Exception as e:
        raise modulerror from e


def module_name(distribution_name: str) -> str:
    """Returns the module name you have to import for a given distribution name."""

    return sitepackage_dir(distribution_name).name


def main():  # pragma: no cover
    names = (
        "beautifulsoup4",
        "bs4",
        "clickx",
        "click-tools",
        "click_tools",
        "click-validators",
    )

    for name in names:

        try:
            p = sitepackage_dir(name)
        except Exception as e:
            print(f"Error finding package directory for {name}: {e}")
            continue

        print(f"Package directory for {name}: {p} {type(p)}, {module_name(name)}")


if __name__ == "__main__":
    main()
