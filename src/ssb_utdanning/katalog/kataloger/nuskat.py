from functools import lru_cache

import dapla as dp
import pandas as pd
from fagfunksjoner import auto_dtype

from ssb_utdanning.config import REGION
from ssb_utdanning.katalog.katalog import UtdKatalog


@lru_cache(1)
def get_nuskat(path: str = "", from_date: str = "") -> UtdKatalog:
    """Nuskat is a catlogue maintained by 360 that connects more data to each nus2000-code.

    Args:
        path (str): The path as a string where the nus-katalog is located.
        from_date (str): If you do not want the latest nuskat, specify a date here.

    Returns:
        UtdKatalog: A UtdKatalog object with the nuskat-data.
    """
    if REGION == "ON_PREM":
        if not path:
            path = "/ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
        nuskat = auto_dtype(pd.read_sas(path))
    elif REGION == "DAPLA":
        if not path:
            path = ""  # Fix later,use from_date if versioned
        nuskat = dp.read_pandas(path)

    return UtdKatalog(nuskat, key_col="nus2000", path=path)
