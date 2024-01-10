import json
import os
import shutil
import unittest
from pathlib import Path

import pandas as pd
import pytest

from ssb_utdanning.format.formats import info_stored_formats


class TestInfoStoredFormats(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initdir(self, tmp_path):
        # Create a temporary folder and add test JSON files for testing

        # Create test files with different names and date patterns
        # Set up a test directory structure and add some test JSON files
        self.test_folder_path = tmp_path / "test_formats"
        print(self.test_folder_path)
        os.makedirs(self.test_folder_path, exist_ok=True)

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
        for k, file_name in enumerate(self.test_files):
            with open(os.path.join(self.test_folder_path, file_name), "w") as json_file:
                json.dump(dictionaries[k], json_file)

    def test_folder_not_found(self):
        with self.assertRaises(OSError):
            # Test when folder does not exist
            info_stored_formats(path_prod=Path("not-here-yo"))

    def test_extract_information(self):
        # Test extracting information from file paths
        # display(info_stored_formats(path_prod=self.test_folder_path))
        for i, filename in enumerate(self.test_files):
            shortname = filename.split("_")[0]
            df_info = info_stored_formats(shortname, path_prod=self.test_folder_path)
            # Check if the returned object is a DataFrame
            assert isinstance(df_info, pd.DataFrame)
            assert list(df_info["date_original"])[0] == self.dates[i]
            assert list(df_info["name"])[0] == shortname
            assert list(df_info["path"])[0] == str(self.test_folder_path / filename)
        # Add more specific assertions based on the expected behavior

    def test_select_specific_name(self):
        # Test selecting a specific name
        for i, filename in enumerate(self.test_files):
            shortname = filename.split("_")[0]
            df_info = info_stored_formats(shortname, path_prod=self.test_folder_path)
            # Check if the returned object is a DataFrame
            assert isinstance(df_info, pd.DataFrame)
            assert list(df_info["date_original"])[0] == self.dates[i]
            assert list(df_info["name"])[0] == shortname
            assert list(df_info["path"])[0] == str(self.test_folder_path / filename)

        # Add assertions to check if the returned DataFrame contains expected data based on the selected name
        # assert df_info == "test content"

    # Add more test methods for different scenarios within info_stored_formats function

    def tearDown(self):
        # Clean up test files and folders after tests
        shutil.rmtree(self.test_folder_path, ignore_errors=True)
