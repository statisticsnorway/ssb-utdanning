import glob, os, datetime
import dateutil
import pandas as pd
import numpy as np

from utd_felles.config import PROD_FORMATS_PATH

       



def info_stored_formats(select_name: str = "", path_prod: str = PROD_FORMATS_PATH) -> pd.DataFrame:
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
    if not os.path.isdir(path_prod):
        raise OSError(f"Cant find folder {path_prod}")
    all_paths = glob.glob(f"{path_prod}*.json")
    all_names = ["_".join(os.path.split(p)[1].split(".")[0].split("_")[:-1]) for p in all_paths]
    all_dates_original = [os.path.split(p)[1].split(".")[0].split("_")[-1] for p in all_paths]
    all_dates_datetime = [dateutil.parser.parse(d) for d in all_dates_original]
    df_info = (pd.DataFrame({"name": all_names,
                            "date_original": all_dates_original, 
                            "date_datetime": all_dates_datetime,
                            "path": all_paths,})
                           .sort_values(["name", "date_datetime"]))
    
    if select_name:
        df_info = df_info[df_info["name"] == select_name]
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
    df_info = info_stored_formats(name)
    df_info = df_info.sort_values("date_datetime", ascending=False)
    for i, row in df_info.iterrows():
        if row["date_datetime"] < date_time:
            format_date = row["date_datetime"]
            break
    get_path = df_info[df_info["date_datetime"] == format_date]["path"].iloc[0]
    return get_path
                     