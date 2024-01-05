"""A Python package built on top of Statistics Norway's code- and classification-system "KLASS".

The package aims to make Klass's API for retrieving data easier to use by re-representing Klass's internal hierarchy as python-classes.
Containing methods for easier traversal down, search classes and widgets, reasonable defaults to parameters etc.
Where data is possible to fit into pandas DataFrames, this will be preferred, but hirerachical data will be kept as json / dict structure.
"""

import importlib
import toml

# Split into function for testing
def _try_getting_pyproject_toml(e: Exception | None = None) -> str:
    """Look for version in pyproject.toml, if not found, set to 0.0.0"""
    if e is None:
        passed_excep: Exception = Exception("")
    else:
        passed_excep = e
    try:
        version: str = toml.load("../pyproject.toml")["tool"]["poetry"]["version"]
        return version
    except Exception as e:
        version_missing: str = "0.0.0"
        print(
            f"Error from ssb-klass-pythons __init__, not able to get version-number, setting it to {version_missing}: {passed_excep}"
        )
        return version_missing
# Gets the installed version from pyproject.toml, then there is no need to update this file
try:
    __version__ = importlib.metadata.version("ssb-utdanning")
except importlib.metadata.PackageNotFoundError as e:
    __version__ = _try_getting_pyproject_toml(e)


__all__ = []
local_imports = {
    "format.formats": ["info_stored_formats", "get_format", "UtdFormat"],
}

# Loop that imports local files into this namespace and appends to __all__ for star imports
for file, funcs in local_imports.items():
    for func in funcs:
        globals()[func] = getattr(importlib.import_module(f"ssb_utdanning.{file}", func), func)
        __all__.append(func)