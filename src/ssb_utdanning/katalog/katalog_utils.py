import json

import pandas as pd

from ssb_utdanning import logger
from ssb_utdanning.katalog import UtdKatalog
from ssb_utdanning.katalog.katalog import REQUIRED_COLS


def create_new_utd_katalog(
    path: str, key_col_name: str, extra_cols: list[str] | None = None
) -> UtdKatalog:
    """Make a new, empty Katalog.

    Args:
        path (str): Path the katalog should be stored to.
        key_col_name (str): Name of the key column.
        extra_cols (list[str]): Extra columns to add to the katalog. Defaults to an empty list (None).

    Returns:
        UtdKatalog: The new katalog.
    """
    if extra_cols is None:
        extra_cols = []

    # Make empty dataset with recommended columns
    cols = [key_col_name, *extra_cols, *REQUIRED_COLS]
    df = pd.DataFrame({col: [] for col in cols})

    # Ask for metadata / Recommend not making katalog
    metadata = {}
    metadata["team"] = input("Ansvarlig team for katalogen: ")
    # Hva mer?

    logger.info(
        "Add more metadata to the catalogue.metadata before saving if you want. "
    )

    result = UtdKatalog(path, key_col_name, **metadata)
    result.data = df
    return result


def open_utd_katalog_from_metadata(meta_path: str) -> UtdKatalog:
    """The metadata contains the path of the Katalog, this function opens the katalog-data just from being shown the metadata-file.

    Args:
        meta_path (str): Path to the metadata-file.

    Returns:
        UtdKatalog: The katalog.
    """
    with open(meta_path) as jsonmeta:
        metadata = json.load(jsonmeta)
    file_path = meta_path.replace("__META.json", "")
    return UtdKatalog(
        file_path, metadata.pop("key_col"), metadata.pop("versioned"), **metadata
    )
