"""Automatically changes dtypes on pandas dataframes using logic.

Tries to keep objects as strings if numeric, but with leading zeros.
Downcasts ints to smalles size. Changes possible columns to categoricals.
"""

import json

import gcsfs
import pandas as pd


def dtype_store_json(
    df: pd.DataFrame, json_path: str, filesystem: None | gcsfs.GCSFileSystem
) -> None:
    """Store dtypes of a pandas dataframe as a jsonfile.

    Args:
        df (pd.DataFrame): Dataframe to store dtypes from.
        json_path (str): Path to json file to store dtypes in.
        filesystem (gcsfs.GCSFileSystem): If working on google, provide the GCSFileSystem.

    Returns:
        None
    """
    dtype_metadata = {}
    for col, dtype in df.dtypes.items():
        second_dtype = None
        if dtype == "category":
            second_dtype = str(df[col].cat.categories.dtype)
        dtype = str(dtype)
        dtype_metadata[col] = {"dtype": dtype, "secondary_dtype": second_dtype}
    if filesystem:
        with filesystem.open(json_path, "w") as json_file:
            json.dump(dtype_metadata, json_file)
            return None
    with open(json_path, "w") as json_file:
        json.dump(dtype_metadata, json_file)


def dtype_apply_from_json(
    df: pd.DataFrame, json_path: str, filesystem: None | gcsfs.GCSFileSystem
) -> pd.DataFrame:
    """Apply dtypes onto a pandas dataframe from a json stored on disk.

    Args:
        df (pd.DataFrame): Dataframe to apply dtypes to.
        json_path (str): Path to json file with dtypes.
        filesystem (gcsfs.GCSFileSystem): If working on google, provide the GCSFileSystem.

    Returns:
        pd.DataFrame: Dataframe with dtypes applied.
    """
    if filesystem:
        with filesystem.open(json_path, "r") as json_file:
            json_dtypes = json.load(json_file)
    else:
        with open(json_path) as json_file:
            json_dtypes = json.load(json_file)
    for col, dtypes in json_dtypes.items():
        if dtypes["secondary_dtype"]:
            df[col] = df[col].astype(dtypes["secondary_dtype"])
        df[col] = df[col].astype(dtypes["dtype"])
    return df
