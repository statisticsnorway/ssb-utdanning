import pandas as pd
from pathlib import Path
import datetime

BASE_PATH = Path("/buckets/shared/vof/situttak/")
SITUTTAK_PATH = BASE_PATH / "vof-situasjonsuttak_data/klargjorte-data/parquet")
UTD_NACEKODER = [
    '88.911', '85.100', '85.201', '85.202', '85.203', '85.601',
    '85.310', '85.320', '85.609', '85.510', '85.521', '85.522', '85.529',
    '85.530', '85.592', '85.593', '85.594', '85.595', '85.596', '85.599',
    '85.410', '85.591', '85.421', '85.422', '85.423', '85.424', '85.429'
]
KOLONNER = [
    'rectype', 'org_nr', 'fnr', 'bnr', 'orgnrbed', 'flv', 'fkommune',
    'status_foretak', 'aktivitetskode', 'org_form', 'navn',
    'off_nav1', 'off_nav2', 'karakt', 'status', 'nace1_sn07',
    'nace2_sn07', 'nace3_sn07', 'sektor_2014', 'undersektor_2014',
    'delreg_merke'
]

def check_bof_available(raise_error: bool = False) -> bool:
    if BASE_PATH.exists():
        return True
    if raise_error:
        raise FileNotFoundError("Cant find bof, apply for acces through LDA and mount vof + situttak as shared bucket, so it mounts locally in dapla lab.")
    return False

def bof_skole(reftime: datetime.datetime | None = None) -> pd.DataFrame:
    check_bof_available(raise_error=True)
    
    if reftid is None:
        reftid = datetime.datetime.now()
    if not isinstance(reftid, datetime.datetime):
        raise TypeError("Reftime must be a datetime.")
    reftid.strftime("%Y-%m")
    SITUTTAK_PATH.glob()
    
    
    