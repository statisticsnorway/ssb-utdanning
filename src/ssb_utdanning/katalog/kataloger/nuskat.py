from functools import lru_cache

from ssb_utdanning.katalog.katalog import UtdKatalog


@lru_cache(1)
def get_nuskat(path: str = "") -> UtdKatalog:
    """Nuskat is a catlogue maintained by 360 that connects more data to each nus2000-code.

    Args:
        path (str): The path as a string where the nus-katalog is located.
        from_date (str): If you do not want the latest nuskat, specify a date here.

    Returns:
        UtdKatalog: A UtdKatalog object with the nuskat-data.
    """
    if not path:
        path = "/ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
    return UtdKatalog(path, key_col="nus2000")
