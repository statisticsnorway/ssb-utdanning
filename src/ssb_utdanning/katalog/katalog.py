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

from ssb_utdanning import logger

if TYPE_CHECKING:
    pass

# Local imports
from fagfunksjoner import auto_dtype

from ssb_utdanning.config import REGION, PROD_KATALOGER
from ssb_utdanning.paths.get_paths import get_path_latest

REQUIRED_COLS = ["username", "edited_time", "expiry_date", "validity"]


class UtdKatalog:
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
            glob_patterns = [v["glob"] for k, v in PROD_KATALOGER.items() if k.lower().startswith(path.lower())]
            if glob_patterns:
                self.path = get_path_latest(glob_patterns[0])
                
        if key_cols is None:
            print("key_cols er None")
            key_cols_from_conf = [v["key_cols"] for k, v in PROD_KATALOGER.items() if k.lower().startswith(path.lower())]
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

    def __str__(self) -> str:
        """Print some of the content of the Katalog."""
        result = "En Katalog fra utdannings-fellesfunksjonene."
        for key, attr in vars(self).items():
            if key != "data":
                result += f"\n{key}: {attr}"
        result += "\n\nKolonne-info:\n"
        buf = StringIO()
        self.data.info(buf=buf)
        result += buf.getvalue()
        return result

    def _update_metadata(
        self, metadata: dict[str, str | bool] | None = None
    ) -> dict[str, str | bool]:
        new_metadata: dict[str, str | bool] = {}
        if hasattr(self, "metadata"):
            new_metadata |= self.metadata
        if isinstance(metadata, dict):
            new_metadata |= metadata
        new_metadata |= {
            # "path": self.path,  # Should this always be guessed from placement? Not included in metadata?
            "key_cols": self.key_cols,
        }
        self.metadata = new_metadata
        return new_metadata

    def _correct_path(self) -> None:
        """Sas-people are used to not specifying file-extension, this method makes an effort looking for the file in storage."""
        # and the path contains no version,
        # and the user has not specified full path (depends on extension present), pick the newest one.
        # Meaning if the user specifies the version number, they should get that instead
        version = self._extract_version()
        _, _, _, ext = self._split_path(self.path)
        has_no_ext = not ext
        if not (self.path.endswith(".parquet") or self.path.endswith(".sas7bdat")):
            if os.path.isfile(self.path + ".parquet"):
                self.path = self.path.rstrip(".") + ".parquet"
            elif os.path.isfile(self.path + ".sas7bdat"):
                self.path = self.path.rstrip(".") + ".sas7bdat"
            else:
                logger.info(
                    "Cant find a sas7bdat or parquetfile at %s...", str(self.path)
                )
                return None
        # If we find a file on disk, and the dataframe is still unpopulated
        if not hasattr(self, "data"):
            self.get_data()
            return None
        if not isinstance(self.data, pd.DataFrame):
            self.get_data()  # type: ignore[unreachable]

    def _path_to_newest_version(self) -> None:
        self.path = self.get_latest_version_path()

    def get_latest_version_path(self) -> str:
        """Figure out the most recent path/version for the current Katalog."""
        parent, first_part, last_part, ext = self._split_path(self.path)
        if not self._extract_version():
            first_part = "_".join([first_part, last_part])
        pattern = os.path.join(parent, first_part) + "*"
        fileversions = glob.glob(pattern)
        fileversions = [
            file
            for file in fileversions
            if "__" not in file
            and (file.endswith(".sas7bdat") or file.endswith(".parquet"))
        ]
        if fileversions:
            lastversion = sorted(fileversions)[-1]
            _, _, latest_version, ext = self._split_path(lastversion)
            if latest_version.startswith("v") and latest_version[1:].isnumeric():
                latest_path = (
                    os.path.join(parent, first_part) + f"_{latest_version}{ext}"
                )
            else:
                latest_path = os.path.join(parent, first_part) + ext
            return latest_path
        logger.info(
            "Cant find any files on disk, assuming the current path is the latest one."
        )
        return self.path

    def get_data(
        self, path: str = ""
    ) -> None | tuple[pd.DataFrame, dict[str, str | bool]]:
        """Get the data and metadata for the catalogue, dependant on the environment we are in.

        Args:
            path (str): The path to the file to open. Defaults to "".

        Returns:
            None | tuple[pd.DataFrame, dict[str, str|bool]]: The dataframe and metadata for the catalogue. Returns None, if you're not sure.p

        Raises:
            OSError: If the file extension is not parquet or sas7bdat.
        """
        if not path:
            path = str(self.path)

        # Warn user if not opening the latest version?
        if self.get_latest_version_path() != self.path:
            sure = input(
                f"You are not opening the latest version of the file: {self.get_latest_version_path()} \n Are you sure? Y/y: "
            )
            if not sure.lower() == "y":
                return None

        if REGION == "ON_PREM":
            path_kat = Path(path)
            path_metadata = (
                path_kat.parent / (str(path_kat.stem) + "__META")
            ).with_suffix(".json")
            metadata = {}
            if os.path.isfile(path_metadata):
                with open(path_metadata) as metafile:
                    metadata = json.load(metafile)
            if path_kat.suffix == ".parquet":
                df_get_data: pd.DataFrame = pd.read_parquet(path_kat)
            elif path_kat.suffix == ".sas7bdat":
                df_get_data = auto_dtype(pd.read_sas(path_kat))
            else:
                raise OSError(
                    f"Can only open parquet and sas7bdat, you gave me {path_kat.suffix}"
                )
        elif REGION == "DAPLA":
            path_metadata_dapla: str = path.replace(".parquet", "_META.json")
            try:
                with dp.FileClient.gcs_open(str(path_metadata_dapla), "r") as metafile:
                    metadata = json.load(metafile)
            except FileNotFoundError:
                metadata = {}
            result: pd.DataFrame = dp.read_pandas(path)
            df_get_data = result
        # Insert missing columns into dataframe?
        for col in REQUIRED_COLS:
            if col not in df_get_data.columns:
                df_get_data[col] = ""
                df_get_data[col] = df_get_data[col].astype("string[pyarrow]")

        self._update_metadata(metadata)
        self.data = df_get_data
        return df_get_data, metadata

    def _split_path(self, path: str = "") -> tuple[str, str, str, str]:
        if not path:
            path = self.path
        parent = os.path.split(path)[0]
        file, ext = os.path.splitext(os.path.basename(path))
        filename_parts = file.split("_")
        last_part = filename_parts[-1]
        return parent, "_".join(filename_parts[:-1]), last_part, ext

    def _extract_version(self, path: str = "") -> int:
        if not path:
            path = self.path
        _, _, path_version, _ = self._split_path(path)
        if path_version.startswith("v") and path_version[1:].isnumeric():
            return int(path_version[1:])
        else:
            return 0

    def _bump_path(self, path: str, version: int = 0) -> str:
        path_version = self._extract_version()
        parent, first_part, last_part, ext = self._split_path(path)
        # Didnt send the parameter
        if not version:
            # Take the version from the path
            version = path_version + 1
        # If last part wasnt a version-number, add the last part back (we dont like v0)
        if not path_version:
            first_part = "_".join([first_part, last_part])
        if not version:
            logger.info(
                "Class set to versioned, but read file does not contain correctly placed version-number."
                "The read file should end in _v1 or similar."
            )
            version = 1
        first_part += f"_v{version}"
        # Add extensions back to filename
        filename = "".join([first_part, ext])
        path = os.path.join(os.path.split(path)[0], filename)
        return path

    def save(
        self, path: str = "", bump_version: bool = True, existing_file: str = ""
    ) -> None:
        """Stores class to disk in prod or dapla as parquet, also stores metadata as json?

        Args:
            path (str): Path to save the file to. Defaults to "".
            bump_version (bool): Whether or not to bump the version of the file. Defaults to True.
            existing_file (str): What to do if the file already exists on the path. Defaults to "". Can also be set to "overwrite" or "filedump".

        Raises:
            ValueError: If existing_file is not one of the valid options.
            OSError: If the file already exists on the path and existing_file is not set to "overwrite" or "filebump".

        Returns:
            None
        """
        if not path:
            path = self.path

        valid_existing_file_args = ["", "overwrite", "filebump"]
        if existing_file not in valid_existing_file_args:
            raise ValueError(
                f"Set the existing_file parameter as one of: {valid_existing_file_args}"
            )

        # Force path to be parquet before writing
        file, ext = os.path.splitext(os.path.basename(path))
        if ext != ".parquet":
            ext = ".parquet"
            path = os.path.join(os.path.split(path)[0], "".join([file, ext]))

        # Automatic versioning
        if bump_version:
            path = self._bump_path(path)

        # Check that we are not writing to an existing file
        if existing_file == "" and os.path.isfile(path):
            error = f""""File already on path we are trying to write to: {path}
            If you want to overwrite, set the existing_file parameter to "overwrite",
            if you want to instead set this to the newest placement available on disk set it to "filebump"
            Be aware that this might indicate you have opened a file that is not the latest,
            and you might want to take further steps to avoid losing work or similar.
            """
            raise OSError(error)
        if existing_file == "overwrite" and os.path.isfile(path):
            logger.warning(
                "Youve set overwrite, AND YOU ARE ACTUALLY OVERWRITING A FILE RIGHT NOW DUDE: %s",
                path,
            )
            sure = input("YOU SURE ABOUT THIS!?!?! Type Y/y if you are: ")
            if sure.lower() != "y":
                logger.info("aborting save")
                return None

        # If filebump is selected get current version from the filesystem instead'
        if existing_file == "filebump":
            latest_path = self.get_latest_version_path()
            latest_version = self._extract_version(latest_path)
            current_version = self._extract_version()  # Returns int
            target_version = latest_version + 1
            if current_version != latest_version:
                logger.info(
                    """Filebump actually changing the versioning number to %s,
                    this might indicate you opened an older file than the newest available...""",
                    str(target_version),
                )
                sure = input(
                    "You sure you dont want to check if you opened an older file? Y/y: "
                )
                if sure.lower() != "y":
                    logger.info("aborting save")
                    return None
                path = self._bump_path(path, target_version)

        # Reset the classes path, as when we write somewhere, thats were we should open it from again...
        self.path = path

        # Make sure metadata attr is updated
        self._update_metadata()

        # Fill empty cells in required columns with data
        self.data["username"] = getpass.getuser()
        self.data["edited_time"] = datetime.now().isoformat("T", "seconds")
        # Expiry?
        # Validity?

        path_metadata = ""
        if REGION == "ON_PREM":
            self.data.to_parquet(path)
            path_kat = Path(path)
            if self.metadata:
                path_metadata_combine = (
                    path_kat.parent / (str(path_kat.stem) + "__META")
                ).with_suffix(".json")
                with path_metadata_combine.open("w") as metafile:
                    json.dump(self.metadata, metafile)
        elif REGION == "DAPLA":
            dp.write_pandas(self.data, path)
            if self.metadata:
                path_metadata = path.replace(".parquet", "_META.json")
                with dp.FileClient.gcs_open(path_metadata, "w") as metafile:
                    json.dump(self.metadata, metafile)
        logger.info(
            "Wrote file to %s. Wrote metadata to %s", str(path), str(path_metadata)
        )
        return None

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
