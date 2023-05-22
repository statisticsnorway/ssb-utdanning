import pandas as pd
import dapla as dp
from utd_felles import UtdFellesConfig
from utd_felles.data.auto_dtype import auto_dtype


if UtdFellesConfig().MILJO == "PROD":
    PATH = "ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
    NUSKAT = auto_dtype(pd.read_sas(path)
elif UtdFellesConfig().MILJO == "DAPLA":
    PATH = "ssb-prod-utd-felles-data-produkt/nuskat/nuskat.parquet"
    NUSKAT = dp.read_pandas(PATH)

def nuskat_dict(col: str, level: int = 6) -> dict:
    nuskat_cp = NUSKAT.copy()
    if level > 0:
        nuskat_cp = nuskat_cp[nuskat_cp["nus2000"].str.len() == level] 
    return dict(zip(nuskat_cp["nus2000"], nuskat_cp[col.lower()]))