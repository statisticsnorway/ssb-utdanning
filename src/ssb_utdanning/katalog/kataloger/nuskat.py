from functools import lru_cache

import dapla as dp
import pandas as pd
from utd_felles.data.dtypes import auto_dtype
from utd_felles.katalog.katalog import UtdKatalog
from utd_felles.utd_felles_config import UtdFellesConfig


@lru_cache(1)
def get_nuskat(path: str = "", from_date: str = "") -> UtdKatalog:
    if UtdFellesConfig().MILJO == "PROD":
        if not path:
            path = "/ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
        nuskat = auto_dtype(pd.read_sas(path))
    elif UtdFellesConfig().MILJO == "DAPLA":
        if not path:
            path = ""  # Fix later,use from_date if versioned
        nuskat = dp.read_pandas(path)

    return UtdKatalog(nuskat, key_col="nus2000", path=path)
