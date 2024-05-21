import os
from pathlib import Path
import numpy as np
import pandas as pd

# np.random.seed(12345)


def create_mock_katalog() -> Path:
    np.random.seed(12345)
    template_dir = Path(os.getcwd())
    path = template_dir / "mock_data" / "test_katalog_p2024_v1.parquet"
    n = int(1e4)
    ident = np.random.randint(1100, 1500, n)
    age = np.random.randint(18, 69, n)
    sex = np.random.randint(1, 2, n)
    katalog = pd.DataFrame({"ident": ident, "age": age, "sex": sex})
    katalog["ident"] = katalog["ident"].astype(str)
    katalog.drop_duplicates(subset="ident", inplace=True)
    katalog.to_parquet(path)
    return path


def create_mock_dataset() -> Path:
    np.random.seed(12345)
    template_dir = Path(os.getcwd())
    path = template_dir / "mock_data" / "test_data_p2024_v1.parquet"
    n = int(2 * 1e2)
    ident = np.random.randint(1000, 1200, n)
    height = np.round(np.random.normal(170, 30, n), 1)
    data = pd.DataFrame({"ident": ident, "height": height})
    data["ident"] = data["ident"].astype(str)
    data.to_parquet(path)
    return path
