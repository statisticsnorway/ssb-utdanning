import enum
from io import StringIO
from pathlib import Path
from string import digits

import dapla as dp
import pandas as pd
from cloudpathlib import GSPath
from datadoc.backend.datadoc_metadata import DataDocMetadata
from datadoc.backend.statistic_subject_mapping import StatisticSubjectMapping
from fagfunksjoner import auto_dtype

from ssb_utdanning.config import REGION
from ssb_utdanning.paths import versioning
from ssb_utdanning.paths.get_paths import get_path_dates
from ssb_utdanning.paths.get_paths import get_path_latest
from ssb_utdanning.utdanning_logger import logger

class OverwriteMode(enum.Enum):
    """Enum for specifying overwrite behaviors in file operations.

    Attributes:
        overwrite (str): Allows overwriting of existing files.
        filebump (str): Bumps the file version if a file already exists, preventing overwriting.
        NONE (str): Does not allow overwriting; if the file exists, an error is raised.
    """

    overwrite = "overwrite"
    filebump = "filebump"
    NONE = ""


class UtdData:
    """Manages loading, saving and access to metadata.

    Manages the loading, storage, and access of structured data, providing robust methods for handling data
    retrieval, path validation, and metadata management based on specified paths or patterns. This class
    integrates functionality to dynamically load data from local or cloud storage based on specified file
    paths or glob patterns, manage data versions, and ensure that file paths meet specified criteria before
    data loading occurs.

    The class also supports optional keyword exclusions for file searches and integrates metadata handling
    capabilities, making it suitable for applications where data integrity, version control, and comprehensive
    data management are critical.

    Attributes:
        data (pd.DataFrame | None): The DataFrame loaded into the instance, either provided at initialization or loaded from the specified path.
        path (Union[Path, GSPath, str]): The primary file path associated with the data.
        metadata (DataDocMetadata): Metadata associated with the data, automatically managed based on file path changes or data updates.

    Methods:
        __init__: Constructor for initializing a new UtdData instance with optional data and path specifications.
        get_data: Loads data from the specified path if not already loaded.
        save: Saves the current data and metadata to a specified path, managing file versioning and overwrite behavior.
        _metadata_from_path: Updates metadata based on the current data path, extracting relevant details as needed.

    This class is designed to be versatile, supporting various data storage formats and environments, and
    is easily extendable for additional data handling and processing needs.
    """

    def __init__(
        self,
        data: pd.DataFrame | None = None,
        path: Path | GSPath | str = "",
        glob_pattern: str = "",
        exclude_keywords: list[str] | None = None,
    ) -> None:
        """Initializes the UtdData class with data and path parameters. If glob_pattern is used, it will use the latest file matching the pattern.

        Args:
            data (pd.DataFrame | None): Initial dataframe to be used. If None, data will be loaded from the specified path.
            path (Union[Path, GSPath, str]): Path to the file or directory from which the data should be loaded.
            glob_pattern (str): Glob pattern to find files if no direct path is given.
            exclude_keywords (List[str] | None): List of keywords to exclude while searching for files using glob pattern.

        Raises:
            ValueError: If neither path nor glob_pattern are provided.
        """
        if glob_pattern and path:
            logger.info("You set both glob pattern and path, will prioritize path.")
        elif not path and not glob_pattern:
            error_msg = "You must set either path, or glob_pattern."
            raise ValueError(error_msg)

        # Gets a path using glob-pattern
        if glob_pattern and not path:
            path = self._find_last_glob(glob_pattern, exclude_keywords)
        self._correct_check_path(path)
        if data is None:
            self.get_data()
        else:
            self.data = data
        if self.path.is_file():
            self._metadata_from_path()

    def __str__(self) -> str:
        """Provides a string representation of the UtdData object, excluding the data itself for brevity.

        Returns:
            str: A string representation of the UtdData object's metadata and column info.
        """
        result = "UtdData content:\n"
        for key, attr in vars(self).items():
            if key != "data":
                result += f"\n{key}: {attr}"
        result += "\n\nColumn-info:\n"
        buf = StringIO()
        self.data.info(buf=buf)
        result += buf.getvalue()
        return result

    def __len__(self) -> int:
        """Returns the number of entries in the data.

        Returns:
            int: Number of entries.
        """
        return len(self.data)

    def _correct_check_path(self, path: Path | GSPath | str) -> None:
        """Checks and corrects path.

        Checks and corrects the file path by ensuring it has a supported file extension (.parquet or .sas7bdat)
        based on the operating region and available file types. Converts string paths to appropriate Path or
        GSPath objects depending on the operating environment.

        Args:
            path (Union[Path, GSPath, str]): The file path to check and potentially correct. If a string is
                provided, it will be converted to a Path or GSPath object depending on the REGION.

        Returns:
            None: This method does not explicitly raise any exceptions, but may log information if file paths
                  are not found or are incompatible.

        Side Effects:
            - Sets the `self.path` attribute to the corrected Path or GSPath object.
            - Updates `self.periods` with the dates from the file paths using a helper function `get_path_dates`.
            - Logs a message if neither a .parquet nor a .sas7bdat file can be found at the specified path.
        """
        self.path: Path | GSPath
        if REGION == "ON_PREM" and isinstance(path, str):
            self.path = Path(path)
        elif REGION == "BIP" and isinstance(path, str):
            self.path = GSPath(path)
        else:
            self.path = Path(path)
        self.periods = get_path_dates(self.path)

        if not self.path.suffix == ".parquet" or self.path.suffix == ".sas7bdat":
            if self.path.with_suffix(".parquet").exists():
                self.path = self.path.with_suffix(".parquet")
            elif self.path.with_suffix(".sas7bdat").exists():
                self.path = self.path.with_suffix(".sas7bdat")
            else:
                logger.info(
                    "Cant find a sas7bdat or parquetfile at %s...", str(self.path)
                )
                return None

    def _find_last_glob(
        self, glob_pattern: str = "", exclude_keywords: list[str] | None = None
    ) -> str:
        """Finds the last modified file that matches the glob pattern and does not include the excluded keywords.

        Args:
            glob_pattern (str): The glob pattern to search for.
            exclude_keywords (List[str] | None): Keywords to exclude from the search.

        Returns:
            str: The path to the last modified file matching the criteria.
        """
        return get_path_latest(glob_pattern, exclude_keywords)

    def get_similar_paths(self) -> list[str]:
        """Finds paths that are similar to the current path, excluding versions.

        Returns:
            List[str]: A sorted list of similar file paths.
        """
        return sorted(
            [
                str(x)
                for x in self.path.parent.glob(
                    self.path.stem.rstrip(digits) + "*" + self.path.suffix
                )
            ]
        )

    def get_latest_version_path(self) -> str:
        """Determines the most recent version path for the current file.

        Returns:
            str: Path of the most recent file version.
        """
        return self.get_similar_paths()[-1]

    def get_data(
        self,
    ) -> None | pd.DataFrame | tuple[pd.DataFrame, dict[str, str | bool]]:
        """Loads the data from the specified path, or the most recent file version if the specified path is outdated.

        Returns:
            None | tuple[pd.DataFrame, dict[str, str|bool]]: The loaded data and metadata if successful, None otherwise.

        Raises:
            OSError: If the file extension is not parquet or sas7bdat.
        """
        path = self.path

        # Warn user if not opening the latest version?
        if str(self.get_latest_version_path()) != str(self.path):
            sure = input(
                f"You are opening {self.path}, not opening the latest version of the file: {self.get_latest_version_path()} \n Are you sure? Y/y: "
            )
            if not sure.lower() == "y":
                return None
        logger.info("Opening data from %s", str(self.path))
        df_get_data: pd.DataFrame
        if REGION == "ON_PREM":
            if path.suffix == ".parquet":
                df_get_data = pd.read_parquet(path)
            elif path.suffix == ".sas7bdat":
                df_get_data = auto_dtype(pd.read_sas(path))
            else:
                raise OSError(
                    f"Can only open parquet and sas7bdat, you gave me {path.suffix}"
                )
        if REGION == "BIP":
            if path.suffix == ".sas7bdat":
                with dp.FileClient().gcs_open(str(path), "r") as sasfile:
                    df_get_data = auto_dtype(pd.read_sas(str(sasfile)))
            else:
                df_get_data = pd.DataFrame(dp.read_pandas(str(path)))

        self.data = df_get_data
        return df_get_data

    def get_version(self, path: str | Path | GSPath = "") -> int:
        """Gets the version number of the file at the specified path.

        Args:
            path (Union[str, Path, GSPath]): The path to check for versioning.

        Returns:
            int: The version number.
        """
        if path:
            return versioning.get_version(path)
        if self.path:
            return versioning.get_version(self.path)
        return 0

    @staticmethod
    def bump_path(path: Path | GSPath, num_bumps: int = 1) -> Path | GSPath:
        """Increments the version number in the path.

        Args:
            path (Union[str, Path, GSPath]): The file path to increment.
            num_bumps (int): Number of version increments.

        Returns:
            str: Updated path with the incremented version number.

        Raises:
            TypeError: if type returned by version.bump_path is unrecognized
        """
        new_path = versioning.bump_path(path, num_bumps)
        if REGION == "ON_PREM" and isinstance(new_path, str):
            return Path(new_path)
        elif REGION == "BIP" and isinstance(new_path, str):
            return GSPath(new_path)
        elif not isinstance(new_path, str):
            return new_path
        error_msg = "Dont know how to handle a str-path if we dont know where we are."
        raise TypeError(error_msg)

    def save(
        self,
        path: str | Path | GSPath = "",
        bump_version: bool = True,
        overwrite_mode: str | OverwriteMode = OverwriteMode.NONE,
        save_metadata: bool = True,
    ) -> None:
        """Saves data to path.

        Saves the data to a specified path, manages file versioning, and handles file overwriting based on the provided
        parameters. The method also offers the option to save associated metadata alongside the data.

        Args:
            path (Union[str, Path, GSPath]): The file path where the data should be saved.
                                                Defaults to the current object path.
            bump_version (bool): Whether to automatically increment the file version. Defaults to True.
            overwrite_mode (Union[str, OverwriteMode]): Specifies how to handle existing files at the target path.
                                                        Can be 'none', 'overwrite', or 'filebump'. Defaults to OverwriteMode.NONE.
            save_metadata (bool): Whether to save metadata along with the data. Defaults to True.

        Returns:
            None

        Raises:
            OSError: If the file already exists and the conditions for overwriting are not met as per the `overwrite_mode`.

        Notes:
            The method converts string paths to Path or GSPath based on the runtime environment. The path is also forced
            to have a '.parquet' suffix. If `bump_version` is enabled, the file path will be adjusted to accommodate a new
            version number according to existing files in the target directory.

            Interactive prompts are used to confirm overwriting actions when necessary, providing a safety mechanism to prevent
            accidental data loss.
        """
        if isinstance(overwrite_mode, str):
            overwrite_mode_enum = getattr(OverwriteMode, overwrite_mode)
            try:
                overwrite_mode_enum = getattr(OverwriteMode, overwrite_mode)
            except ValueError:
                overwrite_mode_enum = OverwriteMode.NONE
                logger.warning(
                    f"Set the existing_file parameter as one of: {[x.value for x in iter(OverwriteMode)]}"
                )
        else:
            overwrite_mode_enum = overwrite_mode

        if not path:
            path = self.path

        pathpath: Path | GSPath
        if isinstance(path, str) and REGION == "BIP":
            pathpath = GSPath(path)
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
        elif REGION == "BIP":
            dp.write_pandas(self.data, str(pathpath))

        # Update path in metadata before saving
        self.metadata.dataset_path = pathpath
        metapath = self.metadata.metadata_document
        if metapath:
            metapath = metapath.parent / (pathpath.stem + "__DOC.json")
        self.metadata.metadata_document = metapath
        # Actuall save the metadata
        if save_metadata:
            self.metadata.write_metadata_document()

        logger.info(
            "Wrote file to %s. Wrote metadata to %s.", str(self.path), str(metapath)
        )
        return None

    def _metadata_from_path(self) -> None:
        """Extracts metadata from the file path, intended for internal use."""
        self.metadata = DataDocMetadata(
            StatisticSubjectMapping(""), dataset_path=str(self.path)
        )
