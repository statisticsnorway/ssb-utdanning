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
    """Retrieves a dictionary of skolereg versions according to date.

    Retrieves a dictionary mapping each year extracted from the filenames in the skoleregister directory
    to the corresponding file path. The filenames are expected to contain year information as four digits
    following an underscore.

    Returns:
        dict[str, Path]: A dictionary where each key is a four-digit year string extracted from the filename,
                         and each value is the Path object pointing to the corresponding file.

    Raises:
        NotImplementedError: If the function is called within the DAPLA environment, where it is not yet implemented.
    """
    date_paths_dict = dict()
    if REGION == "ON_PREM":
        base_path = "/ssb/stamme01/utd/kat/skolereg/"
        paths = [Path(x) for x in glob.glob(base_path + "*.parquet")]
        date_paths = sorted([x for x in paths if x.stem[1:].isdigit()])
        date_paths_dict = {x.stem[1:5]: x for x in date_paths}
        # print(year_paths_dict.keys())
        return date_paths_dict
    elif REGION == "BIP":
        raise NotImplementedError("Not written for Dapla yet")
    return date_paths_dict
