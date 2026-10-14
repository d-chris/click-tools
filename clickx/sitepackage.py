import importlib.metadata
import importlib.resources
import json
import typing as t

from pathlibutil import Path


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

        # def get_url(dist: importlib.metadata.Distribution) -> Path:
        #     if hasattr(dist, "origin"):
        #         return Path.from_uri(dist.origin.url).resolve(True)

        origin = getattr(
            dist,
            "origin",
            json.loads(
                dist.read_text("direct_url.json") or "{}",
            ),
        )

        filepath = (
            origin.get("url") if hasattr(origin, "get") else getattr(origin, "url")
        )
        editable_path = Path.from_uri(filepath).resolve(True)

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


if __name__ == "__main__":
    sitepackage_dir("click-tools")
