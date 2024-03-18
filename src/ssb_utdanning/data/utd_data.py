import os, glob, json, enum
from io import StringIO
from string import digits
from pathlib import Path
from cloudpathlib import CloudPath
import pandas as pd

import dapla as dp
from fagfunksjoner import auto_dtype
from datadoc.backend.datadoc_metadata import DataDocMetadata
from datadoc.backend.statistic_subject_mapping import StatisticSubjectMapping

from ssb_utdanning import logger
from ssb_utdanning.config import REGION
from ssb_utdanning.paths import get_paths, versioning


class OverwriteMode(enum.Enum):
    """Enum for overwrite codes."""
    overwrite = "overwrite"
    filebump = "filebump"
    NONE = ""


class UtdData:    
    def __init__(self,
                 path: Path | CloudPath | str,
                 data: pd.DataFrame | None = None) -> str:
        
        self.path: Path | CloudPath
        if REGION == "ON_PREM" and isinstance(path, str):
            self.path = Path(path)
        elif REGION == "DAPLA" and isinstance(path, str):
            self.path = CloudPath(path)
        print(self.path, type(self.path))
        self._correct_check_path()
        
        if data is None:
            self.get_data()
        else:
            self.data = data
            
        self.metadata = DataDocMetadata(StatisticSubjectMapping(""), dataset_path=str(self.path))

    def __str__(self) -> str:
        """Print some of the content of the Data."""
        result = "UtdData content:\n"
        for key, attr in vars(self).items():
            if key != "data":
                result += f"\n{key}: {attr}"
        result += "\n\nColumn-info:\n"
        buf = StringIO()
        self.data.info(buf=buf)
        result += buf.getvalue()
        return result       

    def _correct_check_path(self) -> None:
        """Sas-people are used to not specifying file-extension, this method makes an effort looking for the file in storage."""
        if not self.path.suffix == ".parquet" or self.path.suffix  == ".sas7bdat":
            if self.path.with_suffix(".parquet").exists():
                self.path = self.path.with_suffix(".parquet")
            elif self.path.with_suffix(".sas7bdat").exists():
                self.path = self.path.with_suffix(".sas7bdat")
            else:
                logger.info(
                    "Cant find a sas7bdat or parquetfile at %s...", str(self.path)
                )
                return None

    def get_similar_paths(self) -> list[str]:
        """Find similarly named files, not including the version number."""
        return sorted(
            self.path.parent.glob(
                self.path.stem.rstrip(digits) + "*" + self.path.suffix
            )
        )
            
    def get_latest_version_path(self) -> str:
        """Figure out the most recent path/version for the current path."""
        return self.get_similar_paths()[-1]
        
    def get_data(self) -> None | tuple[pd.DataFrame, dict[str, str | bool]]:
        """Get the data and metadata for the catalogue, dependant on the environment we are in.

        Args:
            path (str): The path to the file to open. Defaults to "".

        Returns:
            None | tuple[pd.DataFrame, dict[str, str|bool]]: The dataframe and metadata for the catalogue. Returns None, if you're not sure.p

        Raises:
            OSError: If the file extension is not parquet or sas7bdat.
        """
        path = self.path
        
        # Warn user if not opening the latest version?
        if self.get_latest_version_path() != self.path:
            sure = input(
                f"You are not opening the latest version of the file: {self.get_latest_version_path()} \n Are you sure? Y/y: "
            )
            if not sure.lower() == "y":
                return None

        if REGION == "ON_PREM":            
            if path.suffix == ".parquet":
                df_get_data: pd.DataFrame = pd.read_parquet(path)
            elif path.suffix == ".sas7bdat":
                df_get_data = auto_dtype(pd.read_sas(path))
            else:
                raise OSError(
                    f"Can only open parquet and sas7bdat, you gave me {suffix}"
                )
        
        self.data = df_get_data
        return df_get_data
    
    def get_version(self, path: str | Path | CloudPath = "") -> int:
        if path:
            return versioning.get_version(path)
        if self.path:
            return versioning.get_version(self.path)
        return 0
        
    @staticmethod
    def bump_path(path: str| Path | CloudPath, num_bumps: int = 1) -> str:
        return versioning.bump_path(path, num_bumps)

    def save(
        self,
        path: str | Path | CloudPath = "",
        bump_version: bool = True,
        overwrite_mode: str | OverwriteMode = OverwriteMode.NONE
    ) -> None:
        """Stores class to disk in prod or dapla as parquet, also stores metadata as json?

        Args:
            path (str): Path to save the file to. Defaults to "".
            bump_version (bool): Whether or not to bump the version of the file. Defaults to True.
            existing_file (str): What to do if the file already exists on the path. Defaults to "". Can also be set to "overwrite" or "filebump".

        Raises:
            ValueError: If existing_file is not one of the valid options.
            OSError: If the file already exists on the path and existing_file is not set to "overwrite" or "filebump".

        Returns:
            None
        """
        # Replace string with enum attr
        if isinstance(overwrite_mode, str):
            overwrite_mode_enum = getattr(OverwriteMode, overwrite_mode)
        else:
            overwrite_mode_enum = overwrite_mode
        # Check that overwrite_mode now is in enum
        if overwrite_mode_enum not in OverwriteMode:
            raise ValueError(
                f"Set the existing_file parameter as one of: {[x.value for x in iter(OverwriteMode)]}"
            )
            
        
        if not path:
            path = self.path
        pathpath: Path | CloudPath
        if isinstance(path, str) and REGION == "DAPLA":
            pathpath = CloudPath(path)
        else:
            pathpath = Path(path)
        # Force path to be parquet before writing
        pathpath = pathpath.with_suffix(".parquet")
        # Automatic versioning
        if bump_version:
            pathpath = self.bump_path(pathpath)

        # Check that we are not writing to an existing file
        if overwrite_mode_enum == OverwriteMode.NONE and pathpath.is_file():
            error = f""""File already on path we are trying to write to: {path}
            If you want to overwrite, set the existing_file parameter to "overwrite",
            if you want to instead set this to the newest placement available on disk set it to "filebump"
            Be aware that this might indicate you have opened a file that is not the latest,
            and you might want to take further steps to avoid losing work or similar.
            """
            raise OSError(error)
        if overwrite_mode_enum == OverwriteMode.overwrite and pathpath.is_file():
            logger.warning(
                "Youve set overwrite, AND YOU ARE ACTUALLY OVERWRITING A FILE RIGHT NOW DUDE: %s",
                path,
            )
            sure = input("YOU SURE ABOUT THIS!?!?! Type Y/y if you are: ")
            if sure.lower() != "y":
                logger.info("aborting save")
                return None

        # If filebump is selected get current version from the filesystem instead
        if overwrite_mode_enum == OverwriteMode.filebump:
            latest_path = self.get_latest_version_path()
            latest_version = self.get_version(latest_path)
            current_version = self.get_version()  # Returns int
            target_version = latest_version + 1
            diff_version = target_version - current_version - 1
            if current_version != latest_version:
                logger.warning(
                    """Filebump actually changing the versioning number to %s,
                    this might indicate you opened an older file than the newest available...""",
                    str(target_version),
                )
                sure = input(
                    "You sure you dont want to check if you opened an older file? Y/y: "
                )
                if sure.lower() != "y":
                    logger.info("aborting save")
                    return None
                pathpath = self.bump_path(pathpath, diff_version)
                

        # Reset the classes path, as when we write somewhere, thats were we should open it from again...
        self.path = pathpath

        if REGION == "ON_PREM":
            self.data.to_parquet(pathpath)
        elif REGION == "DAPLA":
            dp.write_pandas(self.data, pathpath)
            
        self.metadata.dataset_path = pathpath
        metapath = self.metadata.metadata_document
        metapath = metapath.parent / (pathpath.stem + "__DOC.json")
        self.metadata.metadata_document = metapath
        self.metadata.write_metadata_document()
        
        logger.info(
            "Wrote file to %s. Wrote metadata to %s.", str(self.path), str(metapath)
        )
        return None