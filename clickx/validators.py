try:
    from clicktypes import *  # noqa
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("pip install click-tools[validators]") from e
