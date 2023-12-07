import glob, os, datetime, json
from collections import defaultdict 
import pandas as pd
import numpy as np
import dateutil


PATH_PROD = "/ssb/stamme01/utd/utd-felles/formater/"


def info_stored_formats(path_prod: str = PATH_PROD) -> pd.DataFrame:
    """In Prodsone, list all json-format-files in format folder.
    
    Does not look at file content, only what can be extracted from the filesystem.
    Date is parsed from filename, converting datetime strings to true datetimes as well.
    Sorts descending by name and date.
    
    Parameters
    ----------
    path_prod: str
        The path to the folder containing the json-formats-files. 
        Set to a default of "/ssb/stamme01/utd/utd-felles/formater/"
    
    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame containing information extracted from the path names.
    """
    all_paths = glob.glob(f"{path_prod}*.json")
    all_names = ["_".join(os.path.split(p)[1].split(".")[0].split("_")[:-1]) for p in all_paths]
    all_dates_original = [os.path.split(p)[1].split(".")[0].split("_")[-1] for p in all_paths]
    all_dates_datetime = [dateutil.parser.parse(d) for d in all_dates_original]
    df_info = (pd.DataFrame({"name": all_names,
                            "date_original": all_dates_original, 
                            "date_datetime": all_dates_datetime,
                            "path": all_paths,})
                           .sort_values(["name", "date_datetime"]))
    return df_info


def get_path(name: str, date: str = "latest") -> str:
    """Get the path to a json-format-file.

    Parameters
    ----------
    name: str
        The name of the format.
    date: str
        The date of the format.
        If "latest", the latest format will be returned.
        If a datetime string, the format with the closest date will be returned.
    
    Returns
    -------
    str
        The path to the json-format-file.
    """
    
    print(f"Finding path from date: {date}")
    if date != "latest":
        date_time = dateutil.parser.parse(date)
    elif date == "latest":
        date_time = datetime.datetime.now()
    df_info = info_stored_formats()
    df_info = df_info[df_info["name"] == name].sort_values("date_datetime", ascending=False)
    for i, row in df_info.iterrows():
        if row["date_datetime"] < date_time:
            format_date = row["date_datetime"]
            break
    get_path = df_info[df_info["date_datetime"] == format_date]["path"].iloc[0]
    return get_path
                               
def get_format(name: str, date: str = "latest") -> dict|defaultdict:
    """Get the format from a json-format-file, dependent on the name (start of filename).

    Parameters
    ----------
    name: str
        The name of the format.
    date: str
        The date of the format.
        If "latest", the latest format will be returned.
        If a datetime string, the format with the closest date will be returned.
    
    Returns
    -------
    dict|defaultdict
        The format as a dictionary.
        If the format contains a "other" key, a defaultdict will be returned.
        The defaultdict will have the keys of the format, and the default value will be the "other" value.
        If the format contains the SAS-value for missing: ".", or another recognized "empty-datatype":
        Many known keys for empty values, will be inserted in the dict, to hopefully map these correctly.
    """
    path = get_path(name, date)
    print("Getting format from", path)
    with open(path, "r") as format_json:
        ord_dict = json.load(format_json)
    
    # Populate nans with first nan-value found in format
    nan_str_types = [".", "none", "", "NA", "<NA>", "<NaN>"]
    nan_py_types = [None,  np.nan, float('nan')]
    nan_key_str_types = []
    for k in ord_dict.keys():
        for j in nan_str_types:
            if k.lower() == j.lower():
                nan_key_str_types += [k]
    nan_key_py_types = [y for y in [x for x in ord_dict.keys() if not isinstance(x, str)] if z in nan_py_types]
    if nan_key_py_types or nan_key_str_types:
        nan_vals = [v for k, v in ord_dict.items() if k in nan_key_py_types or k in nan_key_str_types]
        # Lets just take the first one
        nan_val = nan_vals[0]
        # We dont want to overwrite the keys that are already defined...
        overwrite_keys = [x for x in nan_str_types + nan_py_types + nan_key_py_types + [pd.NA] if x not in ord_dict.keys()]
        for nan_type in overwrite_keys:
            ord_dict[nan_type] = nan_val
    
    # Consider returning a defualtdict if "other" specified.
    str_keys = {k: v for k, v in ord_dict.items() if isinstance(k, str)}
    if "other" in [x.lower() for x in str_keys.keys()]:
        # Just use the first one we find
        other_val = [v for k, v in str_keys.items() if k.lower() == "other"][0]
        def_dict = defaultdict(lambda: other_val)
        for k, v in ord_dict.items():
            def_dict[k] = v
        return def_dict
    # Otherwise return the populated dict
    return ord_dict
                              
     
    
    