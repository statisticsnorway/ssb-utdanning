"""Retrieves paths and manages versioning."""

from ssb_utdanning.paths.get_paths import get_path_dates
from ssb_utdanning.paths.get_paths import get_path_latest
from ssb_utdanning.paths.get_paths import get_path_reference_date
from ssb_utdanning.paths.get_paths import get_paths
from ssb_utdanning.paths.get_paths import get_paths_dates

__all__ = [
    "get_path_dates",
    "get_path_latest",
    "get_path_reference_date",
    "get_paths",
    "get_paths_dates",
]
