import os
from pathlib import Path
import numpy as np
import pandas as pd

# np.random.seed(12345)


def create_mock_datasets() -> None:
    np.random.seed(12345)
    n = int(2 * 1e2)
    ident = np.random.randint(1000, 1200, n)
    height = np.round(np.random.normal(170, 30, n), 1)
    data = pd.DataFrame({"ident": ident, "height": height})
    data["ident"] = data["ident"].astype(str)
    template_dir = Path(os.getcwd())
    filenames = ["test_data", "test_katalog", "test_data_excludethiskeyword"]
    dates = [f"{i}-10" for i in range(2020, 2025)]
    versions = [i for i in range(1, 4)]
    for i in versions:
        for j in dates:
            for k in filenames:
                path = template_dir / "mock_data" / f"{k}_p{j}_v{i}.parquet"
                data.to_parquet(path)
    date_first = [f"{i}-10" for i in range(2019, 2024)]
    date_last = [f"{i}-10" for i in range(2020, 2025)]
    for i, v in enumerate(versions):
        path = (
            template_dir
            / "mock_data"
            / f"two_dates_p{date_first[i]}_p{date_last[i]}_v{v}.parquet"
        )
        data.to_parquet(path)
