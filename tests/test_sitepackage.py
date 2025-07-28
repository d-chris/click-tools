from pathlib import Path

import pytest

from clickx.sitepackage import module_name
from clickx.sitepackage import sitepackage_dir


@pytest.mark.parametrize(
    "distname, package",
    [
        ("pip", "pip"),
        ("clickx", "clickx"),
        ("click-tools", "clickx"),
        ("click_tools", "clickx"),
    ],
)
def test_module_name(distname, package):

    assert module_name(distname) == package


@pytest.mark.parametrize(
    "distname",
    [
        "clickx",
        "click-tools",
        "click_tools",
    ],
)
def test_sitepackage_dir(distname):

    dir = sitepackage_dir(distname)

    assert dir == Path("clickx").resolve()


def test_module_name_not_found():

    with pytest.raises(ModuleNotFoundError):
        module_name("nonexistent-package")
