import datetime
import glob
import json
import os
from typing import Any

import dateutil.parser
import pandas as pd

from ssb_utdanning.config import PROD_FORMATS_PATH

UTDFORMAT_INPUT_TYPE = dict[str | int, Any] | dict[str, Any]


class UtdFormat(dict[Any, Any]):
    """Custom dictionary class designed to handle specific formatting conventions."""

    def __init__(self, start_dict: UTDFORMAT_INPUT_TYPE | None = None):
        """Initializes the UtdFormat instance.

        Args:
            start_dict (dict, optional): Initial dictionary to populate UtdFormat.
        """
        super(dict, self).__init__()
        self.cached = True  # Switching the default to False, will f-up __setitem__
        if start_dict:
            for k, v in start_dict.items():
                dict.__setitem__(self, k, v)
        self.update_format()

    def update_format(self) -> None:
        """Update method to set special instance attributes."""
        self.set_na_value()
        self.store_ranges()
        self.set_other_as_lowercase()

    def __setitem__(self, key: str | int, value: Any) -> None:
        """Overrides the '__setitem__' method of dictionary to perform custom actions on setting items.

        Args:
            key: Key of the item to be set.
            value: Value to be set for the corresponding key.
        """
        if self.cached:
            dict.__setitem__(self, key, value)
            if isinstance(key, str):
                if "-" in key and key.count("-") == 1:
                    self.store_ranges()
                if key.lower() == "other" and key != "other":
                    self.set_other_as_lowercase()
            if self.check_if_na(key):
                self.set_na_value()

    def __missing__(self, key: str | int) -> Any:
        """Overrides the '__missing__' method of dictionary to handle missing keys.

        Args:
            key: Key that is missing in the dictionary.

        Returns:
            Any: Value of key in any special conditions: confusion int/str, in one of the ranges, NA or if other is defined.

        Raises:
            ValueError: If the key is not found in the format and no 'other' key is specified.
        """
        int_str_confuse = self.int_str_confuse(key)
        if int_str_confuse:
            if self.cached:
                self[key] = int_str_confuse
            return int_str_confuse

        key_in_range = self.look_in_ranges(key)
        if key_in_range:
            if self.cached:
                self[key] = key_in_range
            return key_in_range

        if self.check_if_na(key):
            if self.set_na_value():
                if self.cached:
                    self[key] = self.na_value
                return self.na_value

        other = self.get("other", "")
        if other:
            if self.cached:
                self[key] = other
            return other

        raise ValueError(f"{key} not in format, and no other-key is specified.")

    def store_ranges(self) -> None:
        """Stores ranges based on specified keys in the dictionary."""
        self.ranges: dict[str, tuple[float, float]] = {}
        for key, value in self.items():
            if isinstance(key, str):
                if "-" in key and key.count("-") == 1:
                    bottom, top = key.split("-")[0].strip(), key.split("-")[1].strip()
                    if (bottom.isdigit() or bottom.lower() == "low") and (
                        top.isdigit() or top.lower() == "high"
                    ):
                        if bottom.lower() == "low":
                            bottom_float = float("-inf")
                        else:
                            bottom_float = float(bottom)
                        if top.lower() == "high":
                            top_float = float("inf")
                        else:
                            top_float = float(top)
                        self.ranges[value] = (bottom_float, top_float)

    def look_in_ranges(self, key: str | int | float) -> None | str:
        """Looks for the specified key within the stored ranges.

        Args:
            key: Key to search within the stored ranges.

        Returns:
            The value associated with the range containing the key, if found; otherwise, None.
        """
        # print(f"looking in ranges for {key}")
        try:
            key = float(key)
        except ValueError:
            return None
        for range_key, (bottom, top) in self.ranges.items():
            # print(f"Looking in ranges at {range_key}, {bottom=} {top=}")
            if key >= bottom and key <= top:
                return range_key
        return None

    def int_str_confuse(self, key: str | int) -> None | Any:
        """Handles conversion between integer and string keys.

        Args:
            key: Key to be converted or checked for existence in the dictionary.

        Returns:
            The value associated with the key (if found) or None.
        """
        if isinstance(key, str):
            try:
                key = int(key)
                if key in self:
                    return self[key]
            except ValueError:
                return None
        elif isinstance(key, int):
            key = str(key)
            if key in self:
                return self[key]
        return None

    def set_other_as_lowercase(self) -> None:
        """Sets the key 'other' to lowercase if mixed cases are found."""
        found = False
        for key in self:
            if isinstance(key, str):
                if key.lower() == "other":
                    found = True
                    break
        if found:
            value = self[key]
            del self[key]
            self["other"] = value

    def set_na_value(self) -> bool:
        """Sets the value for NA (Not Available) keys in the UtdFormat.

        Returns:
            bool: True if NA value is successfully set, False otherwise.
        """
        for key, value in self.items():
            if self.check_if_na(key):
                self.na_value = value
                return True
        else:
            self.na_value = None
            return False

    @staticmethod
    def check_if_na(key: str | Any) -> bool:
        """Checks if the specified key represents a NA (Not Available) value.

        Args:
            key: Key to be checked for NA value.

        Returns:
            bool: True if the key represents NA, False otherwise.
        """
        if pd.isna(key):
            return True
        if isinstance(key, str):
            if key in [".", "none", "", "NA", "<NA>", "<NaN>"]:
                return True
        return False

    def store(
        self,
        format_name: str,
        output_path: str = PROD_FORMATS_PATH,
        force: bool = False,
    ) -> None:
        """Stores the UtdFormat instance in a specified output path.

        Args:
            format_name (str): Name of the format to be stored.
            output_path (str): Path where the format will be stored.
            force (bool): Flag to force storing even for cached instances.

        Raises:
            ValueError: If storing a cached UtdFormat might lead to an unexpectedly large number of keys.
        """
        if self.cached and not force:
            error_msg = """Storing a cached UtdFormat might lead to many more keys than you want.
            Please check the amount of keys before storing.
            You can reopen the dict, set it as False on .cached, then store again, or send force=True to the store method."""
            raise ValueError(error_msg)
        store_format_prod({format_name: self}, output_path)


def info_stored_formats(
    select_name: str = "", path_prod: str = PROD_FORMATS_PATH
) -> pd.DataFrame:
    """In Prodsone, list all json-format-files in format folder.

    Does not look at file content, only what can be extracted from the filesystem.
    Date is parsed from filename, converting datetime strings to true datetimes as well.
    Sorts descending by name and date.

    Args:
        select_name (str): Name of the specific format to select information for.
        path_prod (str): Path to the directory containing stored format files. Set to a default of "/ssb/stamme01/utd/utd-felles/formater/"

    Returns:
        pd.DataFrame: Information extracted from the path names.

    Raises:
        OSError: If the specified path_prod directory does not exist.
    """
    if not os.path.isdir(path_prod):
        raise OSError(f"Cant find folder {path_prod}")
    all_paths = glob.glob(f"{path_prod}*.json")
    all_names = [
        "_".join(os.path.split(p)[1].split(".")[0].split("_")[:-1]) for p in all_paths
    ]
    all_dates_original = [
        os.path.split(p)[1].split(".")[0].split("_")[-1] for p in all_paths
    ]
    all_dates_datetime = [dateutil.parser.parse(d) for d in all_dates_original]
    df_info = pd.DataFrame(
        {
            "name": all_names,
            "date_original": all_dates_original,
            "date_datetime": all_dates_datetime,
            "path": all_paths,
        }
    ).sort_values(["name", "date_datetime"])

    if select_name:
        df_info = df_info[df_info["name"] == select_name]
    return df_info


def get_path(name: str, date: str = "latest") -> str | None:
    """Retrieves the path for a specific format on a given date.

    Args:
        name (str): Name of the format.
        date (str): Date string to find the path for. Defaults to "latest". If a datetime string, the format with the closest date will be returned.

    Returns:
        str: The path associated with the specified format and date, if found; otherwise, None.
    """
    print(f"Finding path from date: {date}")
    if date != "latest":
        date_time = dateutil.parser.parse(date)
    elif date == "latest":
        date_time = datetime.datetime.now()
    df_info = info_stored_formats(name)
    df_info = df_info.sort_values("date_datetime", ascending=False)
    if len(df_info):
        for _, row in df_info.iterrows():
            if row["date_datetime"] < date_time:
                format_date = row["date_datetime"]
                break
        get_path: str = df_info[df_info["date_datetime"] == format_date]["path"].iloc[0]
        return get_path
    return None


def get_format(name: str, date: str = "latest") -> UtdFormat | None:
    """Retrieves the format from a json-format-file, dependent on the name (start of filename).

    Args:
        name (str): Name of the format.
        date (str): Date string to find the format for. Defaults to "latest". If a datetime string, the format with the closest date will be returned.

    Returns:
        dict or defaultdict: The formatted dictionary or defaultdict for the specified format and date. If the format contains a "other" key, a defaultdict will be returned. If the
            format contains the SAS-value for missing: ".", or another recognized "empty-datatype":
            Many known keys for empty values, will be inserted in the dict, to hopefully map these correctly.
    """
    path = get_path(name, date)
    print("Getting format from", path)
    if path:
        with open(path) as format_json:
            ord_dict = json.load(format_json)
        return UtdFormat(ord_dict)
    return None


def store_format_prod(
    formats: dict[str, UtdFormat] | UtdFormat,
    output_path: str = PROD_FORMATS_PATH,
) -> None:
    """Takes a nested or unnested dictionary and saves it to prodsone-folder as a timestamped json.

    Args:
        formats (dict[str, dict[str, str]] | dict[str, str]): Dictionary containing format information.
            Nested dictionary structure expected if multiple formats are passed. If nested, the first layer of keys should be the format-names.
            The values of the dictionary are the dict contents of the formats.¨
            If unnested, we assume, this is a single format, and we ask for the name using input().
        output_path (str): Path to store the format data. Not including the filename itself, only the base folder. Defaults to PROD_FORMATS_PATH.

    Raises:
        NotImplementedError: If the provided formats structure is neither nested nor unnested dictionaries of strings.
    """
    if all([isinstance(x, dict) for x in formats.values()]):
        nested = True
    elif all([isinstance(x, str) for x in formats.values()]):
        nested = False
        format_name = input("Please specify the name of the format: ")
    else:
        raise NotImplementedError("Expecting a nested or unnested dict of strings.")

    now = datetime.datetime.now().isoformat("T", "seconds")
    if nested:
        formats_nested: dict[str, UtdFormat] = formats
        for format_name, format_content in formats_nested.items():
            if is_different_from_last_time(format_name, format_content):
                with open(
                    os.path.join(output_path, f"{format_name}_{now}.json"), "w"
                ) as json_file:
                    json.dump(format_content, json_file)
    elif not nested and isinstance(formats, UtdFormat):
        format_not_nested: UtdFormat = formats
        if is_different_from_last_time(format_name, format_not_nested):
            with open(
                os.path.join(output_path, f"{format_name}_{now}.json"), "w"
            ) as json_file:
                json.dump(format_not_nested, json_file)


def is_different_from_last_time(format_name: str, format_content: UtdFormat) -> bool:
    """Checks if the current format content differs from the last saved version.

    Args:
        format_name (str): The short name of the format (first part of json-filename).
        format_content (UtdFormat): Content of the format in dictionary format to be compared against the content stored on disk.

    Returns:
        bool: True if the current format content is different from the last saved version; otherwise, False.
    """
    path_latest = get_path(format_name, date="latest")
    print(path_latest)
    if path_latest:
        path = get_path(format_name, date="latest")
        if path:
            with open(path) as format_json:
                content = json.load(format_json)
            if content != format_content:
                return True
    # No previous format found
    else:
        return True
    print("Content of format looks the same as previous version, not saving.")
    return False
