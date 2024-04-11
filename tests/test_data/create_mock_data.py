import pandas as pd
import os
from pathlib import Path
import numpy as np


def create_mock_data(path: Path | str
                    ):
    
    np.random.seed(12345)

    cols = ["kjoenn", "alder", "hoyde", "BU"]
    data = pd.DataFrame(dict(zip(cols, [list(np.random.randint(1, 2, 100)),
                                        list(np.random.randint(18, 69, 100)),
                                        list(np.round(np.random.normal(174, 1, 100),1)),
                                        list(np.random.randint(0, 8, 100))]
                       )))
    data.to_parquet(path)


