import numpy as np
import pandas as pd
from pathlib import Path
import os


def create_mock_skolereg() -> None:
    template_dir = Path(os.getcwd())
    path = template_dir / "mock_data"
    filename = "vigo_skole_testfil_slett*.parquet"
    years = [i for i in range(2022, 2024)]
    n = int(1e5)
    np.random.seed(12345)
    orgnr = np.random.randint(1000, 2000, n)
    orgnrbed = np.random.randint(2000, 3000, n)
    skolekomm = np.random.randint(1000, 4000, n)
    skoletype = np.random.randint(1, 4, n)
    skolereg = pd.DataFrame(
        {
            "orgnr": orgnr,
            "orgnrbed": orgnrbed,
            "skolekomm": skolekomm,
            "skoletype": skoletype,
        }
    )
    skolereg["orgnr"] = skolereg["orgnr"].astype(str)
    skolereg["orgnrbed"] = skolereg["orgnrbed"].astype(str)
    skolereg.drop_duplicates(subset="orgnr", inplace=True)
    skolereg.drop_duplicates(subset="orgnrbed", inplace=True)
    subcats = ["barnehage", "vgskoler", "test", "grunnskoler", ""]
    for year in years:
        for cat in subcats:
            if cat == "":
                skolereg.to_parquet(path / f"skolereg_p{year}-10_v1.parquet")
            else:
                skolereg.to_parquet(path / f"skolereg_{cat}_p{year}-10_v1.parquet")


def create_mock_vigo() -> None:
    template_dir = Path(os.getcwd())
    path = template_dir / "mock_data"
    filename = "vigo_skole_testfil_slett*.parquet"
    years = [i for i in range(2022, 2024)]
    n = int(1e5)
    np.random.seed(12345)
    SKOLENR = np.random.randint(1000, 2000, n)
    var1 = np.random.randint(1000, 4000, n)
    var2 = np.random.randint(1, 2, n)
    vigo = pd.DataFrame({"SKOLENR": SKOLENR, "vigo_var1": var1, "vigo_var2": var2})
    vigo["SKOLENR"] = vigo["SKOLENR"].astype(str)
    vigo.drop_duplicates(subset="SKOLENR", inplace=True)
    for year in years:
        vigo.to_parquet(path / f"vigo_skole_testfil_slett_p{year}_v1.parquet")


def create_mock_data() -> None:
    template_dir = Path(os.getcwd())
    path = template_dir / "mock_data"
    filename = "vigo_skole_testfil_slett*.parquet"
    years = [i for i in range(2022, 2024)]
    n = int(1e4)
    np.random.seed(12345)
    orgnr = np.random.randint(1000, 2000, n)
    orgnrbed = np.random.randint(2000, 3000, n)
    fskolenr = np.random.randint(1000, 2000, n)
    var1 = np.random.randint(1000, 4000, n)
    var2 = np.random.randint(1, 2, n)
    skolereg = pd.DataFrame(
        {
            "orgnr": orgnr,
            "orgnrbed": orgnrbed,
            "fskolenr": fskolenr,
            "data_var1": var1,
            "data_var2": var2,
        }
    )
    skolereg["orgnr"] = skolereg["orgnr"].astype(str)
    skolereg["orgnrbed"] = skolereg["orgnrbed"].astype(str)
    skolereg["fskolenr"] = skolereg["fskolenr"].astype(str)
    skolereg.drop_duplicates(subset="orgnr", inplace=True)
    skolereg.drop_duplicates(subset="orgnrbed", inplace=True)
    skolereg.drop_duplicates(subset="fskolenr", inplace=True)
    for year in years:
        skolereg.to_parquet(path / f"data_p{year}_v1.parquet")
