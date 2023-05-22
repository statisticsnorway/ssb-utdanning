import pandas as pd
import dapla as dp
from pathlib import Path
import glob
from functools import lru_cache
from utd_felles import UtdFellesConfig
from utd_felles.data.auto_dtype import auto_dtype


if UtdFellesConfig().MILJO == "PROD":
    PATH = "/ssb/stamme01/utd/kat/skolereg/"
    paths = [Path(x) for x in glob.glob(PATH + "*.sas7bdat")]
    year_paths = sorted([x for x in paths if x.stem[1:].isdigit()])
    SKOLEREG_YEARS = {x.stem[1:5]: x for x in year_paths}
elif UtdFellesConfig().MILJO == "DAPLA":
    pass


@lru_cache(len(SKOLEREG_YEARS))
def skolereg_get(year: str = "") -> pd.DataFrame:
    if not year:
        year = sorted(SKOLEREG_YEARS.keys())[-1]
    df = auto_dtype(pd.read_sas(SKOLEREG_YEARS[year]))
    return df


def skolereg_dict(col: str, year: str = "") -> dict:
    skolereg_cp = skolereg_get(year).copy()
    return dict(zip(skolereg_cp["orgnr"], skolereg_cp[col.lower()]))
