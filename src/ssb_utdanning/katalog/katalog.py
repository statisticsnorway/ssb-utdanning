"""The main class for Katalogs at 360.

Katalogs are files that are somewhere inbetween real data and metadata.

They usually have a single columns with some sort of identifier, like orgnr or nus2000.
Then they have 2+ columns of other groupings or data that can be "attached" to real data.
They may represent a list of idents that there is no other info on, that we have tracked down info for,
that we would like to "re-attach" each year, for example.

Katalogs can also be called "kodeverk", "kodelister", "omkodingskatalog" etc.
View "katalog" as an umbrella-term above these.
"""

# Standard library
import getpass
import glob
import json
import os
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

import dapla as dp

# External packages
import pandas as pd



if TYPE_CHECKING:
    pass

# Local imports
from fagfunksjoner import auto_dtype

from ssb_utdanning.config import REGION, KATALOGER
from ssb_utdanning.paths.get_paths import get_path_latest
from ssb_utdanning import logger
from ssb_utdanning.data import utd_data

REQUIRED_COLS = ["username", "edited_time", "expiry_date", "validity"]


class UtdKatalog(utd_data.UtdData):
    """The main class for Katalogs at 360."""

    def __init__(
        self,
        path: str | Path,
        key_cols: list[str] | str | None = None,
        **metadata: str | bool,
    ) -> None:
        """Create an instance of UtdKatalog with some baseline attributes."""
        # Correct for the  using "shortname" like "skolereg"
        self.path: str = str(path)
        if isinstance(path, str) and "/" not in path:
            glob_patterns = [v["glob"] for k, v in KATALOGER.items() if k.lower().startswith(path.lower())]
            if glob_patterns:
                self.path = get_path_latest(glob_patterns[0])
                
        if key_cols is None:
            print("key_cols er None")
            key_cols_from_conf = [v["key_cols"] for k, v in KATALOGER.items() if k.lower().startswith(path.lower())]
            print(key_cols_from_conf)
            if key_cols_from_conf:
                print("inni her")
                self.key_cols = key_cols_from_conf[0]
            
        elif isinstance(key_cols, str):
            self.key_cols = [key_cols]
        else:
            self.key_cols = key_cols       

        
        self.metadata: dict[str, str | bool] = metadata
        #self._correct_path()
        self.get_data(self.path)

        # Make metadata available directly below object as attributes?
        # for key, value in self.metadata.items():
        #    setattr(self, key, value)


    def diff_against_dataset(
        self, dataset: pd.DataFrame, key_col_data: str = "", merge_both: bool = False
    ) -> dict[str, pd.DataFrame]:
        """Compares the idents in a dataset against the Katalog.

        Args:
            dataset (pd.DataFrame): The dataset to compare against.
            key_col_data (str): The column name in the dataset that should be used as the key. Defaults to "".
            merge_both (bool): If True, the katalog's data is merged onto the data, where there is a match on the "in_both" dataset. Defaults to False.

        Returns:
            dict[str, pd.DataFrame]: A dictionary containing the following keys:
                - only_in_dataset: A dataframe containing the rows in the dataset that are not in the Katalog.
                - in_both: A dataframe containing the rows in the Katalog that are also in the dataset.
                - only_in_katalog: A dataframe containing the rows in the Katalog that are not in the dataset.
        """
        if not key_col_data:
            key_col_data = self.key_cols
        ids_in_kat = list(self.data[self.key_cols].unique())
        ids_in_dataset = list(dataset[key_col_data].unique())
        both_ids = [ident for ident in [ids_in_dataset] if ident in ids_in_kat]
        in_both_df = self.data[self.data[self.key_cols].isin(both_ids)].copy()
        if merge_both:
            in_both_df = dataset[dataset[key_col_data].isin(both_ids)].merge(
                (in_both_df.drop(columns=REQUIRED_COLS)),
                how="left",
                left_on=key_col_data,
                right_on=self.key_cols,
            )
        return {
            "only_in_dataset": dataset[~dataset[key_col_data].isin(both_ids)].copy(),
            "in_both": in_both_df,
            "only_in_katalog": self.data[
                ~self.data[self.key_cols].isin(both_ids)
            ].copy(),
        }

    def to_dict(
        self,
        col: str = "",
        level: int = 0,
        key_col: str = "",
    ) -> dict[str, str]:
        """Convert one of the columns in the Katalog to a dict, with the ident as the keys (usually).

        Usually you will only specify the "col"-parameter.

        Args:
            col (str): The column from the Katalog to convert to the values in the dict. Defaults to "".
            level (int): The level (length of string-positions) of the ident to use as the key. Defaults to 0 (All).
            key_col (str): The column to use as the key. Defaults to "". Will use the setting on the Katalog attributes if not specified.

        Returns:
            dict[str, str]: A dictionary of the two columns from the Katalog.
        """
        if not key_col:  # If not passed in to function
            key_col = self.key_cols
        if not key_col:  # If not registred in class-instance
            key_col = self.data.columns[0]  # Just pick the first column
        if not col:
            col = self.data.columns[1]  # Just pick the second column
        if level:
            mask = self.data[key_col].str.len() == level
            return dict(zip(self.data[mask][key_col], self.data[col]))
        return dict(zip(self.data[key_col], self.data[col]))

    def apply_format(
        self,
        df: pd.DataFrame,
        catalog_col_name: str = "",
        data_key_col_name: str = "",
        catalog_key_col_name: str = "",
        new_col_data_name: str = "",
        level: int = 0,
        ordered: bool = False,
        remove_unused: bool = False,
    ) -> pd.DataFrame:
        """Applies the katalog onto a dataset as if it was a format (dict).

        Args:
            df (pd.DataFrame): The dataset to apply the katalog onto.
            catalog_col_name (str): The column name in the katalog to apply. Defaults to "".
            data_key_col_name (str): The column name in the dataset to apply the katalog onto. Defaults to "".
            catalog_key_col_name (str): The column name in the katalog to use as the key. Defaults to "".
            new_col_data_name (str): The column name to use in the dataset. Defaults to "".
            level (int): The level (length of string-positions) of the ident to use as the key. Defaults to 0 (All).
            ordered (bool): If True, the resulting column will be ordered. Defaults to False.
            remove_unused (bool): If True, unused categories will be removed. Defaults to False.

        Returns:
            pd.DataFrame: The dataset with the katalog applied.

        Raise:
            ValueError: Something went wrong when trying to convert to a categorical column.
        """
        # Guessing on key column name
        if not data_key_col_name:
            data_key_col_name = catalog_key_col_name
        if not data_key_col_name:
            data_key_col_name = self.key_cols
        if not data_key_col_name:
            self.data.columns[0]
        if not catalog_key_col_name:
            catalog_key_col_name = data_key_col_name

        # Guessing on col name
        if not catalog_col_name:
            catalog_col_name = self.data.columns[1]
        if not new_col_data_name:
            new_col_data_name = catalog_col_name

        logger.info(
            "new_col_data_name=%s data_key_col_name=%s catalog_col_name=%s catalog_key_col_name=%s",
            str(new_col_data_name),
            str(data_key_col_name),
            str(catalog_col_name),
            str(catalog_key_col_name),
        )

        mapping = self.to_dict(
            col=catalog_col_name, level=level, key_col=catalog_key_col_name
        )
        mapping_unique_vals = list(pd.unique(list(mapping.values())))
        df[new_col_data_name] = df[data_key_col_name].map(mapping)
        try:
            series = df[new_col_data_name].copy()
            series = series.astype(
                pd.CategoricalDtype(categories=mapping_unique_vals, ordered=ordered)
            )
            if remove_unused:
                series = series.cat.remove_unused_categories()
            df[new_col_data_name] = series
        except ValueError as e:
            logger.warning(
                "Couldnt convert column %s to categorical because of error: %s",
                str(new_col_data_name),
                str(e),
            )

        return df
