"""ssb_utdanning is an Education-statistics functionality package in python, owned by Statistics Norway."""

from __future__ import annotations

import importlib
import importlib.metadata
import os

import toml

from ssb_utdanning.data.utd_data import UtdData
from ssb_utdanning.format.formats import UtdFormat
from ssb_utdanning.katalog.katalog import UtdKatalog
from ssb_utdanning.orgnrkontroll.orgnrkontroll import orgnrkontroll_func
from ssb_utdanning.utdanning_logger import logger

# Mypy wants an "explicit export?"
__all__ = ["logger", "UtdData", "UtdFormat", "UtdKatalog", "orgnrkontroll_func"]


# Split into function for testing
def _try_getting_pyproject_toml(e: Exception | None = None) -> str:
    """Look for version in pyproject.toml, if not found, set to 0.0.0 ."""
    if e is None:
        passed_excep: Exception = Exception("")
    else:
        passed_excep = e
    try:
        currdir = os.getcwd()
        for _ in range(40):
            if "pyproject.toml" in os.listdir():
                break
            os.chdir("../")
        version: str = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
        os.chdir(currdir)
        return version
    except Exception as e:
        version_missing: str = "0.0.0"
        print(
            f"Error from ssb-utdannings __init__, not able to get version-number, setting it to {version_missing}: {passed_excep}"
        )
        return version_missing


# Gets the installed version from pyproject.toml, then there is no need to update this file
try:
    __version__ = importlib.metadata.version("ssb-utdanning")
except importlib.metadata.PackageNotFoundError as e:
    __version__ = _try_getting_pyproject_toml(e)
