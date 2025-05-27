import pandas as pd
from pathlib import Path
import datetime
import duckdb

from fagfunksjoner.paths.versions import get_latest_fileversions
from ssb_utdanning.utdanning_logger import logger

BASE_PATH = Path("/buckets/shared/vof/situttak/")
SITUTTAK_PATH = BASE_PATH / "vof-situasjonsuttak_data/klargjorte-data/parquet"
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

def bof_skole(reftime: datetime.datetime | None = None,
              bof_path: str | None = None) -> pd.DataFrame:
    check_bof_available(raise_error=True)
    
    if not bof_path:
        if reftime is None:
            bof_path = get_latest_bof_path()
        elif not isinstance(reftime, datetime.datetime):
            raise TypeError("Reftime must be a datetime.")
        else:
            paths = SITUTTAK_PATH.glob(f"vof-situasjonsuttak_p{reftid.strftime('%Y-%m')}_v1.parquet")
            if len(paths) == 0:
                raise ValueError("Found no vof situttak yo")
            bof_path = Path(get_latest_fileversions([str(paths[0])])[0])

    return load_bof_filtered(bof_path)

def get_latest_bof_path() -> Path:
    bof_files = sorted(list(SITUTTAK_PATH.glob("*.parquet")))
    if not bof_files:
        logger.error("Fant ingen BOF-filer i katalogen.")
        raise FileNotFoundError("Ingen BOF-filer funnet i katalogen.")
    
    selected_file = Path(get_latest_fileversions([str(bof_files[-1])])[0])
    logger.info(f"Valgt BOF-fil: {selected_file}")
    return selected_file

def load_bof_filtered(bof_path: Path) -> pd.DataFrame:
    logger.info(f"Leser BOF med DuckDB fra: {bof_path}")
    quoted_codes = ", ".join([f"'{code}'" for code in UTD_NACEKODER])
    utdfilter_sql = " OR ".join([f'nace{i}_sn07 IN ({quoted_codes})' for i in range(1, 4)])
    query = f"""
        SELECT {', '.join(KOLONNER)}
        FROM read_parquet('{bof_path}')
        WHERE {utdfilter_sql}
    """
    try:
        df_bof = duckdb.query(query).to_df()
        logger.info(f"Antall rader etter filter: {len(df_bof)}")
        return df_bof
    except Exception as e:
        logger.error(f"Feil ved lesing med DuckDB: {e}")
        return pd.DataFrame()
    