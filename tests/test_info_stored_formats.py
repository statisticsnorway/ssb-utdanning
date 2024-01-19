import json
import os
import shutil
import unittest
from pathlib import Path
import pandas as pd

from ssb_utdanning.format.formats import info_stored_formats


class TestInfoStoredFormats(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary folder and add test JSON files for testing
        template_dir = Path(os.getcwd())
        self.path = template_dir / "test_formats"
        os.makedirs(self.path, exist_ok=True)

        # Create test JSON files
        self.test_files = ["file_2023-05-10.json", "anotherfile_2024-01-09.json"]
        self.dates = [self.test_files[0][-15:-5], self.test_files[1][-15:-5]]
        frmt1 = {
            "file": dict(
                zip(
                    [f"key{i}" for i in range(1, 6)], [f"value{j}" for j in range(1, 6)]
                )
            )
        }
        frmt2 = {
            "anotherfile": dict(
                zip(
                    [f"{i}" for i in range(1, 6)], [f"category{j}" for j in range(1, 6)]
                )
            )
        }
        dictionaries = [frmt1, frmt2]
        # print(frmt1)
        for k, file_name in enumerate(self.test_files):
            with open(os.path.join(self.path, file_name), "w") as json_file:
                json.dump(dictionaries[k], json_file)

    def test_folder_not_found(self) -> None:
        with self.assertRaises(OSError):
            # Test when folder does not exist
            info_stored_formats(path_prod=Path("not/here/yo"))

    def test_extract_information(self) -> None:
        # df_info = info_stored_formats(path_prod=str(self.path) + "/")
        df_info = info_stored_formats(path_prod=self.path)
        assert isinstance(df_info, pd.DataFrame)
        for i, filename in enumerate(self.test_files):
            assert df_info["name"][i] == filename.split("_")[0]
            assert df_info["date_original"][i] == filename.split("_")[1][:-5]
            assert df_info["path"][i] == str(self.path / filename)

    def test_select_specific_name(self) -> None:
        # Test selecting a specific name
        for i, filename in enumerate(self.test_files):
            shortname = filename.split("_")[0]
            # df_info = info_stored_formats(shortname, path_prod=str(self.path) + "/")
            df_info = info_stored_formats(shortname, path_prod=self.path)
            # Check if the returned object is a DataFrame
            assert isinstance(df_info, pd.DataFrame)
            assert list(df_info["date_original"])[0] == self.dates[i]
            assert list(df_info["name"])[0] == shortname
            assert list(df_info["path"])[0] == str(self.path / filename)

    def tearDown(self) -> None:
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)
