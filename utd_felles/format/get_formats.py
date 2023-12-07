import glob, os, datetime, json
from collections import defaultdict 
import pandas as pd
import numpy as np
import dateutil

from utd_felles.format.formats import get_path
          
def get_format(name: str, date: str = "latest", convert_ranges: bool = True) -> dict|defaultdict:
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
    
    # Sas can have ranges like "22-33" these should be converted to individual keys
    if convert_ranges:
        new_dict = {}
        keys_to_remove = []
        for key, value in ord_dict.items():
            if "-" in key:
                parts = key.split("-")
                if len(parts) == 2 and all([x.isnumeric() for x in parts]):
                    keys_to_remove += [key]
                    parts = [int(x) for x in parts]
                    for i in range(min(parts), max(parts) + 1):
                        if str(i) not in ord_dict:
                            new_dict[str(i)] = value
                        if i not in ord_dict:
                            new_dict[i] = value
        for key in keys_to_remove:
            del ord_dict[key]
        ord_dict |= new_dict
    
    # Populate nans with first nan-value found in format
    nan_str_types = [".", "none", "", "NA", "<NA>", "<NaN>"]
    nan_py_types = [None,  np.nan, float('nan')]
    nan_key_str_types = []
    for k in [x for x in ord_dict if isinstance(x, str)]:
        for j in nan_str_types:
            if k.lower() == j.lower():
                nan_key_str_types += [k]
    nan_key_py_types = [y for y in [x for x in ord_dict if not isinstance(x, str)] if y in nan_py_types]
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
    if "other" in [x.lower() for x in str_keys]:
        # Just use the first one we find
        other_val = [v for k, v in str_keys.items() if k.lower() == "other"][0]
        def_dict = defaultdict(lambda: other_val)
        for k, v in ord_dict.items():
            def_dict[k] = v
        return def_dict
    # Otherwise return the populated dict
    return ord_dict
                              
     
    
    