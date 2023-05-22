from functools import lru_cache
import pandas as pd
import dapla as dp
from utd_felles import UtdFellesConfig
from utd_felles.data.auto_dtype import auto_dtype


@lru_cache(1)
def nuskat_get():
    if UtdFellesConfig().MILJO == "PROD":
        PATH = "/ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
        NUSKAT = auto_dtype(pd.read_sas(PATH))
    elif UtdFellesConfig().MILJO == "DAPLA":
        NUSKAT = dp.read_pandas(PATH)
    return NUSKAT


def nuskat_dict(col: str, level: int = 6) -> dict:
    nuskat_cp = nuskat_get().copy()
    if level > 0:
        nuskat_cp = nuskat_cp[nuskat_cp["nus2000"].str.len() == level] 
    return dict(zip(nuskat_cp["nus2000"], nuskat_cp[col.lower()]))
