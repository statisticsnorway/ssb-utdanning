import json
import pandas as pd
from .katalog import UtdKatalog, REQUIRED_COLS



def create_new_utd_katalog(path: str,
                           key_col_name: str,
                           extra_cols: list = None) -> UtdKatalog:
    # Workaround empty-list-parameter-mutability-issue
    if extra_cols is None:
        extra_cols = []

    # Make empty dataset with recommended columns
    cols = [key_col_name, *extra_cols, *REQUIRED_COLS]
    df = pd.DataFrame({col: [] for col in cols})

    # Ask for metadata / Recommend not making katalog
    metadata = {}
    metadata["team"] = input("Ansvarlig team for katalogen: ")
    # Hva mer?

    print("Add more metadata to the catalogue.metadata before saving if you want. ")

    result = UtdKatalog(path, key_col_name, **metadata)
    result.data = df
    return result

def open_utd_katalog_from_metadata(meta_path: str) -> UtdKatalog:
    with open(meta_path, "r") as jsonmeta:
        metadata = json.load(jsonmeta)
    file_path = meta_path.replace("__META.json", "")
    return UtdKatalog(file_path,
                      metadata.pop("key_col"),
                      metadata.pop("versioned"),
                      **metadata)