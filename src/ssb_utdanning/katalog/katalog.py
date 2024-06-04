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
from pathlib import Path

# External packages
import pandas as pd
from cloudpathlib import GSPath

# Local imports
from ssb_utdanning import utdanning_logger
from ssb_utdanning.data.utd_data import UtdData

REQUIRED_COLS = ["username", "edited_time", "expiry_date", "validity"]


class UtdKatalog(UtdData):
    """The main class for handling catalog-like datasets, extending UtdData with additional catalog-specific functionalities."""

    def __init__(
        self,
        key_cols: list[str] | str,
        data: pd.DataFrame | None = None,
        path: Path | GSPath | str = "",
        glob_pattern: str = "",
        exclude_keywords: list[str] | None = None,
    ) -> None:
        """Initializes a UtdKatalog instance with specified key columns and optional data parameters.

        Args:
            key_cols (list[str] | str): The key column(s) used for merging and indexing within the catalog.
            data (pd.DataFrame | None): Data to be directly loaded into the UtdKatalog instance.
            path (Union[Path, GSPath, str]): File path for data loading.
            glob_pattern (str): Glob pattern to identify data files if path is not specific.
            exclude_keywords (list[str] | None): Keywords to exclude when searching for data files using the glob pattern.

        Raises:
            TypeError: If any non-string type is found within key_cols when it's provided as a list.
        """
        super().__init__(data, path, glob_pattern, exclude_keywords)

        if isinstance(key_cols, str):
            self.key_cols: list[str] = [key_cols]
        else:
            if not all([isinstance(col, str) for col in key_cols]):
                error_msg = "Excpecting all key_cols in iterable to be strings."
                raise TypeError(error_msg)
            self.key_cols = key_cols

    def merge_on(
        self,
        dataset: pd.DataFrame | UtdData,
        key_col_in_data: str,
        keep_cols: list[str] | set[str] | None = None,
        merge: bool = False,
        return_lengths: bool = False,
    ) -> pd.DataFrame:
        """Merges catalog data with an external dataset based on a specified key column.

        Args:
            dataset (pd.DataFrame | UtdData): The dataset to merge with the catalog.
            key_col_in_data (str): The key column name in the dataset for merging.
            keep_cols (list[str] | None): Specific columns to keep from the catalog in the merged data.
            merge (bool): If True, performs an actual merge operation; otherwise just checks for matching keys.
            return_lengths (bool): If True, returns a tuple of the merged DataFrame and a dictionary of lengths of each category after merge.

        Returns:
            pd.DataFrame: The result of the merge operation, containing data from both the catalog and the input dataset.
        """
        if keep_cols is None:
            keep_cols_kat: set[str] = set(self.data.columns)
            keep_cols_kat = keep_cols_kat - set(self.key_cols)
        else:
            keep_cols_kat = set(keep_cols)
        parts: list[pd.DataFrame] = []
        if isinstance(dataset, pd.DataFrame):
            rest: pd.DataFrame = dataset
        else:
            rest = dataset.data

        for col in self.key_cols:
            if (self.data[col].value_counts() > 1).any():
                utdanning_logger.logger.warning(
                    f"Looks like duplicate entries in the catalog column {col}"
                )
            keep_cols_copy = keep_cols_kat.copy()
            keep_cols_copy.add(col)
            temp = rest.merge(
                self.data[list(keep_cols_copy)],
                left_on=key_col_in_data,
                right_on=col,
                how="left",
                indicator=True,
            )
            new_cat = f"{col}_both"
            temp["_merge"] = temp["_merge"].cat.add_categories([new_cat])
            temp.loc[temp["_merge"] == "both", "_merge"] = new_cat
            parts += [temp[temp["_merge"] == new_cat].copy()]
            rest = rest[~rest[key_col_in_data].isin(self.data[col])]
        parts += [rest]
        result = pd.concat(parts)
        result["_merge"] = result["_merge"].fillna("left_only")
        utdanning_logger.logger.info(
            "\n%s", result["_merge"].value_counts(dropna=False)
        )
        if len(result) > len(dataset):
            utdanning_logger.logger.warning(
                "Merge resulted in additional rows. Duplicated may need to be handled"
            )
        return result

    def to_dict(
        self,
        col: str = "",
        level: int = 0,
        key_col: str = "",
    ) -> dict[str, str | int | float]:
        """Converts a column from the Katalog data into a dictionary, mapping keys from another column to these values.

        Args:
            col (str): The column whose values will be used as dictionary values. Defaults to the second column if not specified.
            level (int): The level (length) of the key entries to be included. Defaults to all if 0.
            key_col (str): The column to use as keys in the dictionary. Defaults to the first key column specified in key_cols.

        Returns:
            dict[str, str | int | float]: A dictionary mapping keys to values as per the specified columns and level.
        """
        if not key_col:  # If not passed in to function
            key_col = self.key_cols[0]
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
        """Applies format on DataFrame.

        Applies the catalog formatting to a DataFrame by mapping values from a catalog column to a dataset column
        based on a key. The function can also set the new column as a categorical type, with options for ordering
        and removing unused categories.

        Args:
            df (pd.DataFrame): The dataset to which the catalog formatting will be applied.
            catalog_col_name (str): The name of the column in the catalog whose values will be applied to the dataset.
                                    If not specified, the second column of the catalog data is used by default.
            data_key_col_name (str): The name of the column in the dataset to which the catalog values will be mapped.
                                     If not specified, it defaults to the catalog key column name.
            catalog_key_col_name (str): The name of the key column in the catalog used for mapping. If not specified,
                                        it defaults to the first key column of the catalog.
            new_col_data_name (str): The name for the new column in the dataset after applying the catalog format.
                                     If not specified, it defaults to the catalog column name.
            level (int): The level of detail (length of string positions) for the key used in formatting. Defaults to 0, which includes all.
            ordered (bool): Specifies whether the new column should be treated as an ordered categorical. Defaults to False.
            remove_unused (bool): Whether to remove unused categories from the new categorical column. Defaults to False.

        Returns:
            pd.DataFrame: The DataFrame with the new formatting applied.

        Notes:
            This method involves several default behaviors when parameters are not specified, including defaulting to the second column of
            the catalog for the value mapping and the first key column for the key mapping. Care should be taken when leaving parameters
            unspecified to ensure the correct application of the format.
        """
        # Guessing on key column name
        if not data_key_col_name:
            data_key_col_name = catalog_key_col_name
        if not data_key_col_name:
            data_key_col_name = self.key_cols[0]
        if not data_key_col_name:
            self.data.columns[0]
        if not catalog_key_col_name:
            catalog_key_col_name = data_key_col_name

        # Guessing on col name
        if not catalog_col_name:
            catalog_col_name = self.data.columns[1]
        if not new_col_data_name:
            new_col_data_name = catalog_col_name

        utdanning_logger.logger.info(
            "new_col_data_name=%s data_key_col_name=%s catalog_col_name=%s catalog_key_col_name=%s",
            str(new_col_data_name),
            str(data_key_col_name),
            str(catalog_col_name),
            str(catalog_key_col_name),
        )

        mapping = self.to_dict(
            col=catalog_col_name, level=level, key_col=catalog_key_col_name
        )
        mapping_unique_vals = list(set(mapping.values()))
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
            utdanning_logger.logger.warning(
                "Couldnt convert column %s to categorical because of error: %s",
                str(new_col_data_name),
                str(e),
            )

        return df
