# Standard library
from pathlib import Path
import os
from datetime import datetime
import json
from io import StringIO
# External packages
import pandas as pd
import dapla as dp
# Local imports
from utd_felles.utd_felles_config import UtdFellesConfig


class UtdKatalog:
    def __init__(self,
                 path: str,
                 key_col: str,
                 versioned: bool = True,
                 **metadata,
                ):
        self.path = path
        self.key_col = key_col
        self.versioned = versioned
        self.data, self.metadata = self.get_data(self.path)
        self.metadata = self.metadata | metadata
        # Make metadata available directly below object
        #for key, value in self.metadata.items():
        #    setattr(self, key, value)

    def __str__(self):
        result = "En Katalog fra utdannings-fellesfunksjonene."
        for key, attr in vars(self).items():
            if key != "data":
                result += f"\n{key}: {attr}"
        result += "\n\nKolonne-info:\n"
        buf = StringIO()
        self.data.info(buf=buf)
        result += buf.getvalue()
        return result

    
    def get_data(self, path: str = "") -> tuple[pd.DataFrame, dict]:
        """Get the data and metadata for the catalogue, dependant on the environment we are in"""
        if not path:
            path = self.path
        if UtdFellesConfig().MILJO == "PROD":
            path_kat = Path(path)
            path_metadata = (path_kat.parent / (str(path_kat.stem) + "__META")).with_suffix(".json")
            metadata = {}
            if os.path.isfile(path_metadata):
                with open(path_metadata, "r") as metafile:
                    metadata = json.load(metafile)
            if path_kat.suffix == ".parquet":
                df = pd.read_parquet(path_kat)
            elif path_kat.suffix == ".sas7bdat":
                df = pd.read_sas(path_kat)
            else:
                raise OSError(f"Can only open parquet and sas7bdat, you gave me {path_kat.suffix}")
            return df, metadata
        elif UtdFellesConfig().MILJO == "DAPLA":
            path_metadata = path.replace(".parquet", "_META.json")
            try:
                with dp.FileClient.gcs_open(path_metadata, "r") as metafile:
                    metadata = json.load(metafile)
            except:
                metadata = {}
            return dp.read_pandas(path), metadata
    
    def save(self, path: str = "") -> None:
        """Stores class to disk in prod or dapla as parquet, also stores metadata as json?"""
        if not path:
            path = self.path
        
        # Force path to be parquet before writing
        file, ext = os.path.splitext(os.path.basename(path))
        if ext != ".parquet":
            ext = ".parquet"
            path = os.path.join(os.path.split(path)[0], "".join([file, ext]))
        
        # Automatic versioning
        if self.versioned:
            filename_parts = file.split("_")
            last_part = filename_parts[-1]
            # Check if path already versioned
            if last_part.startswith("v") and last_part[1:].isnumeric():
                current_version = int(last_part[1:])
                # Remove existing version from parts
                filename_parts = filename_parts[:-1]
            else:
                print("Class set to versioned, but read file does not contain correctly placed version-number.")
                print("The read file should end in _v1 or similar.")
                current_version = 0
            new_version = current_version + 1
            filename_parts += [f"v{new_version}"]
            # Add extensions back to filename
            filename = "".join(["_".join(filename_parts), ext])
            path = os.path.join(os.path.split(path)[0], filename)
            print(f"Versioning up to {new_version}! New path: {path}")
            
        # Reset the classes path, as when we write somewhere, thats were we should open it from again...
        self.path = path
        
        if UtdFellesConfig().MILJO == "PROD":
            self.data.to_parquet(path)
            path_kat = Path(path)
            if self.metadata:
                path_metadata = (path_kat.parent / (str(path_kat.stem) + "__META")).with_suffix(".json")
                with open(path_metadata, "w") as metafile:
                    metafile.write(json.dumps(self.metadata))
        elif UtdFellesConfig().MILJO == "DAPLA":
            dp.write_pandas(self.data, path)
            if self.metadata:
                path_metadata = path.replace(".parquet", "_META.json")
                with dp.FileClient.gcs_open(path_metadata, "w") as metafile:
                    metafile.write(self.metadata)
        return None
    
    def to_dict(self, 
                col: str = "", 
                level: int = 0,
                key_col: str = "",) -> dict:
        if not key_col:  # If not passed in to function
            key_col = self.key_col
        if not key_col:  # If not registred in class-instance
            key_col = self.data.columns[0]  # Just pick the first column
        if not col:
            col = self.data.columns[1]  # Just pick the second column
        if level:
            mask = self.data[key_col].str.len() == level
            return dict(zip(self.data[mask][key_col], self.data[col]))
        return dict(zip(self.data[key_col], self.data[col]))

    def apply_format(self,
                     df: pd.DataFrame,
                     catalog_col_name: str = "",
                     data_key_col_name: str = "",
                     catalog_key_col_name: str = "",
                     new_col_data_name: str = "",
                     level: int = 0,
                     ordered: bool = False,
                     remove_unused: bool = False) -> pd.DataFrame:
        # Guessing on key column name
        if not data_key_col_name:
            data_key_col_name = catalog_key_col_name
        if not data_key_col_name:
            data_key_col_name = self.key_col
        if not data_key_col_name:
            self.data.columns[0]
        if not catalog_key_col_name:
            catalog_key_col_name = data_key_col_name

        # Guessing on col name
        if not catalog_col_name:
            catalog_col_name = self.data.columns[1]
        if not new_col_data_name:
            new_col_data_name = catalog_col_name

        print(f"""
        {new_col_data_name=}
        {data_key_col_name=}
        {catalog_col_name=}
        {catalog_key_col_name=}""")

        mapping = self.to_dict(col=catalog_col_name,
                               level=level,
                               key_col=catalog_key_col_name)
        mapping_unique_vals = list(pd.unique(list(mapping.values())))
        df[new_col_data_name] = (df[data_key_col_name]
                                 .map(mapping))
        try:
            series = df[new_col_data_name].copy()
            series = (series.astype(
                pd.CategoricalDtype(
                    categories=mapping_unique_vals,
                    ordered=ordered)
                        )
                     )
            if remove_unused:
                series = series.cat.remove_unused_categories()
            df[new_col_data_name] = series
        except ValueError as e:
            print(f"Couldnt convert column {new_col_data_name} to categorical because of error: {e}")
        
        return df

def create_utd_katalog(key_col_name: str, extra_cols: list = None) -> UtdKatalog:
    # Workaround empty-list-parameter-mutability-issue
    if extra_cols is None:
        extra_cols = []

    # Make empty dataset with recommended columns
    df = pd.DataFrame()
    df.columns = [key_col_name, "username", "edited_time", "expiry_date", "validity"]
    
    # Ask for metadata / Recommend not making katalog
    metadata = {}
    metadata["team"] = input("Ansvarlig team for katalogen: ")
    # Hva mer?
    
    print("Add more metadata to the catalogue.metadata before saving if you want. ")
    
    return UtdKatalog(df, key_col_name, **metadata)