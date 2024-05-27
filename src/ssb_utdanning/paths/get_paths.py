import datetime
import glob

import dapla as dp
import dateutil.parser
from pathlib import Path
from cloudpathlib import GSPath

from ssb_utdanning.config import DEFAULT_DATE
from ssb_utdanning.config import REGION


def get_paths(
    glob_pattern: str, exclude_keywords: str | list[str] | None = None
) -> list[str]:
    """Retrieves a list of file paths that match a specified glob pattern and do not include any of the specified exclude keywords.

    This function supports both local file systems and Google Cloud Storage (GCS) through the Data Platform (DP) interface,
    adapting based on the execution environment (REGION). It filters out any paths that contain keywords specified in
    `exclude_keywords`.

    Args:
        glob_pattern (str): The glob pattern used to find files. This pattern can represent a path on the local filesystem
                            or a GCS bucket depending on the REGION.
        exclude_keywords (str | list[str] | None, optional): A string or list of strings representing keywords to exclude
                                                             in the file search. Files containing these keywords in their paths
                                                             will be excluded from the results. Defaults to None, which means no exclusions.

    Returns:
        list[str]: A list of strings, each representing a path to a file that matches the glob pattern and does not include
                   the exclude keywords. The list is sorted in descending order based on the natural sorting of the paths.

    Raises:
        None directly, but may log errors or raise exceptions depending on the file system access permissions and availability.
    """
    if exclude_keywords is None:
        exclude_keywords = []
    elif isinstance(exclude_keywords, str):
        exclude_keywords = [exclude_keywords]
    if REGION == "BIP":
        fs = dp.FileClient().get_gcs_file_system()
        paths = fs.glob(glob_pattern)
    else:
        paths = glob.glob(glob_pattern)
    for exclude in exclude_keywords:
        paths = [x for x in paths if exclude not in x.split("/")[-1]]
    paths = sorted(paths)[::-1]
    return list(paths)


def get_path_latest(
    glob_pattern: str, exclude_keywords: list[str] | None = None
) -> str:
    """Retrieves path for most recent file matching glob pattern.

    Retrieves the path of the most recently modified file that matches a specified glob pattern,
    excluding any files containing specified keywords. This function uses the `get_paths` function
    to gather all matching paths, then returns the first path from the sorted list, which represents
    the most recent file due to the sorting order set in `get_paths`.

    Args:
        glob_pattern (str): The glob pattern used to identify files. This pattern can specify locations
                            within the local filesystem or a cloud storage path, depending on the execution environment.
        exclude_keywords (list[str] | None): A list of keywords to exclude in the search for files.
                                             Files containing these keywords in their filenames will be ignored.
                                             Defaults to None, which means no exclusions.

    Returns:
        str: The path to the most recent file matching the specified criteria. If no files match,
             this function will raise an IndexError
    """
    return get_paths(glob_pattern, exclude_keywords)[0]


def get_paths_dates(
    glob_pattern: str, exclude_keywords: list[str] | None = None
) -> dict[str, tuple[datetime.datetime] | tuple[datetime.datetime, datetime.datetime]]:
    """
    Retrieves a dictionary of dates to corresponding paths matching a glob pattern.

    This function aggregates dates associated with multiple files, typically used in scenarios where file 
    modifications or creation dates are tracked alongside file paths. It maps each file path that matches 
    a specified glob pattern to a date, extracted by the `get_path_dates` function. Files containing any 
    specified exclude keywords are omitted from the search.

    Args:
        glob_pattern (str): The glob pattern used to identify files. This can include paths on a local 
                            filesystem or within cloud storage, depending on the execution environment.
        exclude_keywords (list[str] | None, optional): A list of keywords that, if present in a file's path,
                                                      will cause that file to be excluded from the results. 
                                                      Defaults to None, meaning no exclusions are applied.

    Returns:
        dict[str, tuple[datetime.datetime] | tuple[datetime.datetime, datetime.datetime]]: A dictionary where each key is a file path and each value is the date associated
        with that file, as determined by the `get_path_dates` function. The date format and the exact nature of the date (e.g., modification, creation) depend on the 
        implementation of `get_path_dates`.

    Note:
        This function assumes that `get_path_dates` is capable of extracting a meaningful date string from 
        each path. The specific nature of the date retrieved (creation, modification, etc.) should be 
        documented in the `get_path_dates` function.
    """
    paths = get_paths(glob_pattern, exclude_keywords)
    result: dict[str, tuple[datetime.datetime] | tuple[datetime.datetime, datetime.datetime]] = {}
    for path in paths:
        result[path] = get_path_dates(path)
    return result


# the next two modules doesn't work properly.
def get_path_dates(
    path: str | Path | GSPath,
) -> tuple[datetime.datetime] | tuple[datetime.datetime, datetime.datetime]:
    """Extracts data information about file from path.

    Extracts date information from a given file path based on specific patterns in the filename. This function assumes
    that the filename includes date information encoded within parts of the filename, specifically formatted and
    separated by underscores. Dates are expected to be in segments prefixed by 'p' or directly as the second last part
    of the filename, following conventions like 'pYYYY-MM-DD'.

    Args:
        path (str): The full path to the file, from which the filename will be parsed for date information.

    Returns:
        tuple[datetime.datetime] | tuple[datetime.datetime, datetime.datetime]: A tuple containing the parsed datetime objects.
        The tuple will contain two datetime objects if the filename includes two date segments ('pYYYY-MM-DD_pYYYY-MM-DD');
        otherwise, it will contain only one datetime object if only one date segment is found.

    Note:
        The function utilizes the `dateutil.parser.parse` method to convert date strings into datetime objects, which
        allows for flexible parsing but also requires careful handling to avoid misinterpretation of non-standard date formats.
        It defaults to using a global DEFAULT_DATE as the base date if the date string is incomplete or partially specified.
    """
    path = str(path)
    filename_parts = path.split("/")[-1].split(".")[0].split("_")
    last_period = filename_parts[-2]
    last_period_datetime = dateutil.parser.parse(last_period[1:], default=DEFAULT_DATE)

    first_period = filename_parts[-3]
    if first_period.startswith("p") and first_period[1:].replace("-", "").isdigit():
        first_period_datetime = dateutil.parser.parse(
            first_period[1:], default=DEFAULT_DATE
        )
        return (first_period_datetime, last_period_datetime)
    return (last_period_datetime,)


def get_path_reference_date(
    reference_datetime: datetime.datetime | str,
    glob_pattern: str,
    exclude_keywords: list[str] | None = None,
) -> str:
    """Finds path from glob pattern and reference date.

    Finds and returns the file path for files identified by `glob_pattern` whose date or date range matches
    a specified reference date. The function ensures the reference date falls within the date range or on
    the specified date but not on the exact bounds of a date range.

    Args:
        reference_datetime (datetime.datetime | str): The reference date used for finding the file. If a string is provided,
                                                      it will be parsed into a datetime object.
        glob_pattern (str): The glob pattern to identify relevant files. This pattern should align with how files are
                            named or structured to contain date information.
        exclude_keywords (list[str] | None, optional): Keywords to exclude certain files from being considered. Files containing
                                                      any of these keywords in their path will be ignored.

    Returns:
        str: The path of the file that aligns with the reference datetime.

    Raises:
        ValueError: Raised in three cases:
                    1. If the reference datetime matches the boundary dates of a range exactly when two dates are provided.
                    2. If no files meet the criteria of being within the specified date range or on the date.
                    3. If the datetime string is malformed and cannot be parsed.

    Note:
        The function uses `get_paths_dates` which retrieves a mapping of file paths to their respective dates.
        Dates should be part of the filenames and parseable based on the structure expected by the `get_paths_dates`.
        The date comparison is inclusive of the start date but exclusive of the end date when a range is specified.
    """
    if isinstance(reference_datetime, str):
        reference_datetime_dt = dateutil.parser.parse(
            reference_datetime, default=DEFAULT_DATE
        )
    else:
        reference_datetime_dt = reference_datetime
    # paths_datetime = get_path_dates(glob_pattern)
    paths_datetime = get_paths_dates(glob_pattern, exclude_keywords)
    for path, check_dates in paths_datetime.items():
        if len(check_dates) == 2:
            if (
                check_dates[1] == reference_datetime_dt
                or check_dates[0] == reference_datetime_dt
            ):
                error_msg = "With two dates, please specify a date between the two periods, not on an overlapping day."
                raise ValueError(error_msg)
            if (
                check_dates[0] <= reference_datetime_dt
                and check_dates[1] > reference_datetime_dt
            ):
                return path
        else:
            if check_dates[0] <= reference_datetime_dt:
                return path
    error_msg = f"Cant find a valid version for {reference_datetime}, last datetime is {check_dates} for glob pattern {glob_pattern}."
    raise ValueError(error_msg)
