import glob
from functools import lru_cache
from pathlib import Path

from ssb_utdanning.config import REGION
from ssb_utdanning.katalog.katalog import UtdKatalog


@lru_cache(50)
def get_skoleregister(from_date: str = "") -> UtdKatalog:
    """Get the skoleregister as an UtdKatalog from a specific date.

    Args:
        from_date (str): The date to get the skoleregister from. Defaults to "".

    Returns:
        UtdKatalog: The skoleregister as an UtdKatalog.
    """
    skolereg_dates = skoleregister_dates()
    if not from_date:
        from_date = sorted(skolereg_dates.keys())[-1]
    return UtdKatalog(
        skolereg_dates[from_date],
        key_col="orgnr",
        from_date=from_date,
    )


def skoleregister_dates() -> dict[str, Path]:
    """Gets the dates from the skoleregisterfiles, has the date as the key.

    Returns:
        dict[str, str]: The dates as the key and the path as the value of the skoleregisterfiles.
    """
    date_paths_dict = dict()
    if REGION == "ON_PREM":
        base_path = "/ssb/stamme01/utd/kat/skolereg/"
        paths = [Path(x) for x in glob.glob(base_path + "*.parquet")]
        date_paths = sorted([x for x in paths if x.stem[1:].isdigit()])
        date_paths_dict = {x.stem[1:5]: x for x in date_paths}
        # print(year_paths_dict.keys())
        return date_paths_dict
    elif REGION == "DAPLA":
        raise NotImplementedError("Not written for Dapla yet")
    return date_paths_dict
