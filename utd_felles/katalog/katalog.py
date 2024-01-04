# Standard library
from pathlib import Path
import os
import glob
import json
from io import StringIO
import getpass
from datetime import datetime
# External packages
import pandas as pd
import dapla as dp
# Local imports
from utd_felles.utd_felles_config import UtdFellesConfig
from utd_felles.data.dtypes import auto_dtype


REQUIRED_COLS = ["username", "edited_time", "expiry_date", "validity"]


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
        self.metadata = metadata
        self._correct_path()
        #self.get_data(self.path)
        
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

    def _update_metadata(self, metadata: dict = None):
        new_metadata = {}
        if hasattr(self, "metadata"):
            new_metadata = new_metadata | self.metadata
        if metadata:
            new_metadata = new_metadata | metadata
        new_metadata = new_metadata | {
                                       #"path": self.path,  # Should this always be guessed from placement? Not included in metadata?
                                       "key_col": self.key_col,
                                       "versioned": self.versioned}
        #print(f"updating metadata {new_metadata}")
        self.metadata = new_metadata
        return new_metadata
    
    def _correct_path(self) -> None:
        """Sas-people are used to not specifying file-extension, 
        this method makes an effort looking for the file in storage"""
        
        # If the katalog is versioned, 
        # and the path contains no version, 
        # and the user has not specified full path (depends on extension present), pick the newest one.
        # Meaning if the user specifies the version number, they should get that instead
        #print(self.path)
        version = self._extract_version()
        _, _, _, ext = self._split_path(self.path)
        has_no_ext = not ext
        if self.versioned and not version and has_no_ext:
            self._path_to_newest_version()
            print(f"Swapping path to {self.path}, since the katalog is versioned, but the provided path isnt, and you have given no file extension")
        
        if not (self.path.endswith(".parquet") or self.path.endswith(".sas7bdat")):
            if os.path.isfile(self.path + ".parquet"):
                self.path = self.path.rstrip(".") + ".parquet"
            elif os.path.isfile(self.path + ".sas7bdat"):
                self.path = self.path.rstrip(".") + ".sas7bdat"
            else:
                print(f"Cant find a sas7bdat or parquetfile at {self.path}...")
                return None
        # If we find a file on disk, and the dataframe is still unpopulated
        if not hasattr(self, "data"):
            self.get_data()
            return None
        if not isinstance(self.data, pd.DataFrame):
            self.get_data()
        
                
                
    def _path_to_newest_version(self):
        self.path = self.get_latest_version_path()
        
    def get_latest_version_path(self):
        parent, first_part, last_part, ext = self._split_path(self.path)
        #print(f"{parent=}, {first_part=}, {last_part=}, {ext=}")
        if not self._extract_version():
            first_part = "_".join([first_part, last_part])
        pattern = os.path.join(parent, first_part) + f"*"
        fileversions = glob.glob(pattern)
        fileversions = [file for file in fileversions 
                        if "__" not in file and 
                        (file.endswith(".sas7bdat") or file.endswith(".parquet"))]
        #print(f"{pattern=}, {fileversions=}")
        if fileversions:
            lastversion = sorted(fileversions)[-1]
            _, _, latest_version, ext = self._split_path(lastversion)
            if latest_version.startswith("v") and latest_version[1:].isnumeric():
                latest_path = os.path.join(parent, first_part) + f"_{latest_version}{ext}"
            else:
                latest_path = os.path.join(parent, first_part) + ext
            return latest_path
        print("Cant find any files on disk, assuming the current path is the latest one.")
        return self.path
        
    
    def get_data(self, path: str = "") -> tuple[pd.DataFrame, dict]:
        """Get the data and metadata for the catalogue, dependant on the environment we are in"""
        if not path:
            path = self.path
        # Warn user if not opening the latest version?
        if self.get_latest_version_path() != self.path:
            sure = input(f"You are not opening the latest version of the file: {self.get_latest_version_path()} \n Are you sure? Y/y: ")
            if not sure.lower() == "y":
                return None
            
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
                df = auto_dtype(pd.read_sas(path_kat))
            else:
                raise OSError(f"Can only open parquet and sas7bdat, you gave me {path_kat.suffix}")
        elif UtdFellesConfig().MILJO == "DAPLA":
            path_metadata = path.replace(".parquet", "_META.json")
            try:
                with dp.FileClient.gcs_open(path_metadata, "r") as metafile:
                    metadata = json.load(metafile)
            except:
                metadata = {}
            df = dp.read_pandas(path)
        
        # Insert missing columns into dataframe?
        for col in REQUIRED_COLS:
            if col not in df.columns:
                df[col] = ""
                df[col] = df[col].astype("string[pyarrow]")
                
        self._update_metadata(metadata)
        self.data = df



    def _split_path(self, path:str = "") -> tuple[str, str, str, str]:
        if not path:
            path = self.path
        parent = os.path.split(path)[0]
        file, ext = os.path.splitext(os.path.basename(path))
        filename_parts = file.split("_")
        last_part = filename_parts[-1]
        return parent, "_".join(filename_parts[:-1]), last_part, ext
    
    def _extract_version(self, path: str = "") -> int:
        if not path:
            path = self.path
        _, _, path_version, _ = self._split_path(path)
        if path_version.startswith("v") and path_version[1:].isnumeric():
            return int(path_version[1:])
        else:
            return 0
        
    
    def _bump_path(self, path: str, version: int = 0) -> str:
        path_version = self._extract_version()
        parent, first_part, last_part, ext = self._split_path(path)
        # Didnt send the parameter
        if not version:
            # Take the version from the path
            version = path_version + 1
        # If last part wasnt a version-number, add the last part back (we dont like v0)
        if not path_version:
            first_part = "_".join([first_part, last_part])
        if not version:
            print("Class set to versioned, but read file does not contain correctly placed version-number.")
            print("The read file should end in _v1 or similar.")
            version = 1
        first_part += f"_v{version}"
        # Add extensions back to filename
        filename = "".join([first_part, ext])
        path =  os.path.join(os.path.split(path)[0], filename)
        return path
    
    def save(self, 
             path: str = "",
             bump_version: bool = True,
             existing_file: str = "") -> None:
        """Stores class to disk in prod or dapla as parquet, also stores metadata as json?"""
        if not path:
            path = self.path
        
        valid_existing_file_args = ["", "overwrite", "filebump"]
        if existing_file not in valid_existing_file_args:
            raise ValueError(f"Set the existing_file parameter as one of: {valid_existing_file_args}")
        
        # Force path to be parquet before writing
        file, ext = os.path.splitext(os.path.basename(path))
        if ext != ".parquet":
            ext = ".parquet"
            path = os.path.join(os.path.split(path)[0], "".join([file, ext]))
        
        # Automatic versioning
        if self.versioned and bump_version:
            path = self._bump_path(path)
        
        
        
        # Check that we are not writing to an existing file
        if existing_file == "" and os.path.isfile(path):
            error = f""""File already on path we are trying to write to: {path}
            If you want to overwrite, set the existing_file parameter to "overwrite",
            if you want to instead set this to the newest placement available on disk set it to "filebump"
            Be aware that this might indicate you have opened a file that is not the latest,
            and you might want to take further steps to avoid losing work or similar.
            """
            raise OSError(error)
        if existing_file == "overwrite" and os.path.isfile(path):
            print(f"Youve set overwrite, AND YOU ARE ACTUALLY OVERWRITING A FILE RIGHT NOW DUDE: {path}")
            sure = input("YOU SURE ABOUT THIS!?!?! Type Y/y if you are: ")
            if sure.lower() != "y":
                print("aborting save")
                return None
            
        # If filebump is selected get current version from the filesystem instead'
        if existing_file == "filebump":
            latest_path = self.get_latest_version_path()
            latest_version = self._extract_version(latest_path)
            current_version = self._extract_version() # Returns int
            target_version = latest_version + 1
            if current_version != latest_version:
                print(f"""Filebump actually changing the versioning number to {target_version}, 
                    this might indicate you opened an older file than the newest available...""")
                sure = input("You sure you dont want to check if you opened an older file? Y/y: ")
                if sure.lower() != "y":
                    print("aborting save")
                    return None
                path = self._bump_path(path, target_version)


        # Reset the classes path, as when we write somewhere, thats were we should open it from again...
        self.path = path
        
        # Make sure metadata attr is updated
        self._update_metadata()
        
        # Fill empty cells in required columns with data
        self.data["username"] = getpass.getuser()
        self.data["edited_time"] = datetime.now().isoformat("T", "seconds")
        # Expiry?
        # Validity?
        
        path_metadata = ""
        if UtdFellesConfig().MILJO == "PROD":
            self.data.to_parquet(path)
            path_kat = Path(path)
            if self.metadata:
                #print("storing metadata in prod")
                path_metadata = (path_kat.parent / (str(path_kat.stem) + "__META")).with_suffix(".json")
                #print(path_metadata)
                with open(path_metadata, "w") as metafile:
                    metafile.write(json.dumps(self.metadata))
        elif UtdFellesConfig().MILJO == "DAPLA":
            dp.write_pandas(self.data, path)
            if self.metadata:
                path_metadata = path.replace(".parquet", "_META.json")
                with dp.FileClient.gcs_open(path_metadata, "w") as metafile:
                    metafile.write(self.metadata)
        print(f"Wrote file to {path}")
        print(f"Wrote metadata to {path_metadata}")
        return None
    
    def diff_against_dataset(self,
                             dataset: pd.DataFrame,
                             key_col_data: str = "", 
                             merge_both: bool = False) -> dict[str, pd.DataFrame]:
        if not key_col_data:
            key_col_data = self.key_col
        ids_in_kat = list(self.data[self.key_col].unique())
        ids_in_dataset = list(dataset[ket_col_data].unique())
        both_ids = [ident for ident in [ids_in_dataset] if ident in ids_in_kat]
        in_both_df = self.data[self.data[self.key_col].isin(both_ids)].copy()
        if merge_both:
            in_both_df = (dataset[dataset[key_col_data].isin(both_ids)]
                          .merge(
                              (in_both_df.drop(columns=REQUIRED_COLS)),
                              how="left",
                              left_on=key_col_data,
                              right_on=self.key_col
                      ))
        return {"only_in_dataset": dataset[dataset[~key_col_data].isin(both_ids)].copy(),
                "in_both": in_both_df,
                "only_in_katalog": self.data[~self.data[self.key_col].isin(both_ids)].copy()}
    
    
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

