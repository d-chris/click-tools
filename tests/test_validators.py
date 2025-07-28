import pytest


def test_validators_missing(mocker):

    mocker.patch.dict("sys.modules", {"clicktypes": None})

    with pytest.raises(ModuleNotFoundError) as e:
        import clickx.validators  # noqa: F401

    assert "pip install click-tools[validators]" in str(e.value)
