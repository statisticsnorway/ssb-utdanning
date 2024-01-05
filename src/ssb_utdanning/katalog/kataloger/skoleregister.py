import pandas as pd
import dapla as dp
from pathlib import Path
import glob
from functools import lru_cache

from utd_felles.utd_felles_config import UtdFellesConfig
from utd_felles.katalog.katalog import UtdKatalog
from utd_felles.data.dtypes import auto_dtype


@lru_cache(50)
def get_skoleregister(from_date: str = "") -> UtdKatalog:
    skolereg_dates = skoleregister_dates()
    if not from_date:
        from_date = sorted(skolereg_dates.keys())[-1]

    if UtdFellesConfig().MILJO == "PROD":
        df = auto_dtype(pd.read_sas(skolereg_dates[from_date]))
    elif UtdFellesConfig().MILJO == "DAPLA":
        return  # Write later
    
    return UtdKatalog(df, key_col="orgnr", year=year, path=skolereg_dates[from_date])


def skoleregister_dates() -> dict:
    if UtdFellesConfig().MILJO == "PROD":
        base_path = "/ssb/stamme01/utd/kat/skolereg/"
        paths = [Path(x) for x in glob.glob(base_path + "*.sas7bdat")]
        date_paths = sorted([x for x in paths if x.stem[1:].isdigit()])
        date_paths_dict = {x.stem[1:5]: x for x in date_paths}
        #print(year_paths_dict.keys())
        return date_paths_dict
    elif UtdFellesConfig().MILJO == "DAPLA":
        return  # Write later