from functools import lru_cache
import pandas as pd
import dapla as dp

from utd_felles.utd_felles_config import UtdFellesConfig
from utd_felles.katalog.katalog import UtdKatalog
from utd_felles.data.dtypes import auto_dtype


@lru_cache(1)
def get_nuskat():
    if UtdFellesConfig().MILJO == "PROD":
        path = "/ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
        nuskat = auto_dtype(pd.read_sas(path))
    elif UtdFellesConfig().MILJO == "DAPLA":
        path = ""  # Fix later
        nuskat = dp.read_pandas(path)
    return UtdKatalog(nuskat, key_col="nus2000", path=path)
