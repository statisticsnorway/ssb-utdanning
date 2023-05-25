import pandas as pd
import dapla as dp
from pathlib import Path
import glob
from functools import lru_cache

from utd_felles.utd_felles_config import UtdFellesConfig
from utd_felles.katalog.katalog import UtdKatalog
from utd_felles.data.dtypes import auto_dtype


@lru_cache(50)
def get_skoleregister(year: str = "") -> pd.DataFrame:
    skolereg_years = skoleregister_years()
    if not year:
        year = sorted(skolereg_years.keys())[-1]

    if UtdFellesConfig().MILJO == "PROD":
        df = auto_dtype(pd.read_sas(skolereg_years[year]))
    elif UtdFellesConfig().MILJO == "DAPLA":
        return  # Write later

    return UtdKatalog(df, key_col="orgnr", year=year, path=skolereg_years[year])


def skoleregister_years() -> dict:
    if UtdFellesConfig().MILJO == "PROD":
        PATH = "/ssb/stamme01/utd/kat/skolereg/"
        paths = [Path(x) for x in glob.glob(PATH + "*.sas7bdat")]
        year_paths = sorted([x for x in paths if x.stem[1:].isdigit()])
        year_paths_dict = {x.stem[1:5]: x for x in year_paths}
        #print(year_paths_dict.keys())
        return year_paths_dict
    elif UtdFellesConfig().MILJO == "DAPLA":
        return  # Write later