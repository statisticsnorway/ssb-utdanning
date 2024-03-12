from pathlib import Path
import dateutil.parser
import datetime
import dapla as dp
import glob

from ssb_utdanning.config import REGION
from ssb_utdanning.config import DEFAULT_DATE

def get_paths(glob_pattern: str,
              exclude_keywords: list[str] | None = None) -> list[str]:
    if exclude_keywords is None:
        exclude_keywords = []
    if REGION == "DAPLA":
        fs = dp.FileClient().get_gcs_file_system()
        paths = fs.glob(glob_pattern)
    else: 
        paths = glob.glob(glob_pattern)
    for exclude in exclude_keywords:
        paths = [x for x in paths if exclude not in x.split("/")[-1]]
    paths = sorted(paths)[::-1]
    return paths

def get_path_latest(glob_pattern: str,
                    exclude_keywords: list[str] | None = None) -> list[str]:
    return get_paths(glob_pattern, exclude_keywords)[0]

def get_path_dates(glob_pattern: str,
                   exclude_keywords: list[str] | None = None) -> dict[str, str]:
    paths = get_paths(glob_pattern, exclude_keywords)
    result: dict[str, str] = {}
    for path in paths:
        filename_parts = path.split("/")[-1].split(".")[0].split("_")
        last_period = filename_parts[-2]
        last_period_datetime = dateutil.parser.parse(last_period[1:], default=DEFAULT_DATE)
        
        first_period = filename_parts[-3]
        if first_period.startswith("p") and first_period[1:].replace("-","").isdigit():
            first_period_datetime = dateutil.parser.parse(first_period[1:], default=DEFAULT_DATE)
            result[path] = (first_period_datetime, last_period_datetime)
            continue
        result[path] = (last_period_datetime,)
    return result

def get_path_reference_date(
    reference_datetime: datetime.datetime | str,
    glob_pattern: str,
    exclude_keywords: list[str] | None = None) -> str:
    if isinstance(reference_datetime, str):
        reference_datetime_dt = dateutil.parser.parse(before_datetime, default=DEFAULT_DATE)
    else:
        reference_datetime_dt = reference_datetime
    paths_datetime = get_path_dates(glob_pattern, exclude_keywords)
    for path, check_dates in paths_datetime.items():
        if len(check_dates) == 2:
            if check_dates[1] == reference_datetime_dt or check_dates[0] == reference_datetime_dt:
                error_msg = "With two dates, please specify a date between the two periods, not on an overlapping day."
                raise ValueError(error_msg)
            if check_dates[0] <= reference_datetime_dt and check_dates[1] > reference_datetime_dt:
                return path
        else:
            if check_dates[0] <= reference_datetime_dt:
                return path
    error_msg = f"Cant find a valid version for {reference_datetime}, last datetime is {check_date} for glob pattern {glob_pattern}."
    raise ValueError(error_msg) 