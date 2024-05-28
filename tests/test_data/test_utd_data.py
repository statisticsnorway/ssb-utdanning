import os
from ssb_utdanning import UtdData
from pathlib import Path
import unittest
import pandas as pd
from create_mock_data import create_mock_data
import shutil
import glob
import sys
from string import digits
from ssb_utdanning.config import REGION

os.environ["DAPLA_REGION"] = "ON_PREM"


class TestUtdData(unittest.TestCase):
    def setUp(self, filename: str = "data_p2024-10_v1.parquet") -> None:
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.path = template_dir / "mock_data"
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)
        self.path_to_file = self.path / filename
        # creating file containing mock data
        create_mock_data(self.path_to_file)
        self.data = pd.read_parquet(self.path_to_file)

    def test_init(self):
        # general checks
        data = UtdData(self.data, self.path_to_file)
        self.assertIsInstance(data, UtdData)
        self.assertIsInstance(data.data, pd.DataFrame)
        self.assertEqual(self.path_to_file, data.path)
        self.assertTrue(self.data.equals(data.data))
        # with Path
        data = UtdData(self.data, Path(self.path_to_file))
        self.assertIsInstance(data, UtdData)
        self.assertIsInstance(data.data, pd.DataFrame)
        self.assertEqual(self.path_to_file, data.path)
        self.assertTrue(self.data.equals(data.data))

        # if glob and path, path is prioritized
        data = UtdData(
            self.data, self.path_to_file, glob_pattern="ignored_glob_pattern*.parquet"
        )
        self.assertIsInstance(data, UtdData)
        self.assertIsInstance(data.data, pd.DataFrame)
        self.assertEqual(self.path_to_file, data.path)
        self.assertTrue(self.data.equals(data.data))
        # if not path and not glob
        with self.assertRaises(ValueError):
            data = UtdData(self.data)

        # if glob and not path
        # exclude keywords
        create_mock_data(self.path / "datatest_drop_keyword_p2024-10_v1.parquet")
        filename = "datatest_p2024-10_v1.parquet"
        path_to_file = self.path / filename
        create_mock_data(self.path / filename)
        data = UtdData(
            glob_pattern=str(self.path) + "/datatest*.parquet",
            exclude_keywords=["drop", "keyword"],
        )
        self.assertIsInstance(data, UtdData)
        self.assertIsInstance(data.data, pd.DataFrame)
        self.assertEqual(path_to_file, data.path)
        self.assertTrue(self.data.equals(data.data))

        # if data=None
        data = UtdData(path=self.path_to_file)
        self.assertIsInstance(data, UtdData)
        self.assertIsInstance(data.data, pd.DataFrame)
        self.assertEqual(self.path_to_file, data.path)
        self.assertTrue(self.data.equals(data.data))

        # send in glob pattern, get latest version
        file_v2 = self.path / "data_p2024-10_v2.parquet"
        create_mock_data(file_v2)
        data = UtdData(
            glob_pattern=str(self.path) + "/data_*.parquet",
            exclude_keywords=["drop", "keyword"],
        )
        self.assertEqual(file_v2, data.path)
        self.assertIsInstance(data, UtdData)
        self.assertIsInstance(data.data, pd.DataFrame)
        self.assertTrue(self.data.equals(data.data))

    def test_str(self):
        self.setUp()
        data = UtdData(path=self.path_to_file)
        self.assertEqual(data.path.__str__(), str(self.path_to_file))
        # print(data.path.__str__())

    def test_correct_check_path(self):
        self.setUp()
        # ON PREM
        data = UtdData(path=self.path_to_file)
        data.path = None
        data._correct_check_path(str(self.path_to_file))
        self.assertIsInstance(data.path, Path)
        data.path = None
        # send in path without .parquet suffix
        path_no_suffix = str(self.path_to_file).split(".")[0]
        data._correct_check_path(path_no_suffix)
        self.assertEqual(str(data.path).split(".")[-1], "parquet")
        # when file can't be found
        self.assertIsNone(
            data._correct_check_path(
                "/invalid_path/nonexistentfile_p2024-10_v1.parquet"
            )
        )

    def test_get_latest_version_path(self):
        self.setUp()
        # latest_file = file_v2 = self.path/"data_p2024-11_v1.parquet"
        path_bumped = UtdData.bump_path(self.path_to_file)
        # checking that bump path return vi+1
        self.assertTrue(
            int(str(path_bumped)[-9]) == int(str(self.path_to_file)[-9]) + 1
        )
        create_mock_data(path_bumped)
        data = UtdData(path=path_bumped)
        data.path = self.path_to_file
        self.assertTrue(str(data.get_latest_version_path()) == str(path_bumped))

    def test_save(self):
        self.setUp()
        data = UtdData(path=self.path_to_file)
        data.save(path=self.path_to_file)
        del data
        self.setUp()
        data = UtdData(path=self.path_to_file)
        data.save(path=self.path_to_file, overwrite_mode="filebump")
        del data
        self.setUp()
        data = UtdData(path=self.path_to_file)
        with self.assertRaises(AttributeError):
            data.save(path=self.path_to_file, overwrite_mode="non_existant_mode")

        del data
        self.setUp()
        data = UtdData(path=self.path_to_file)
        with self.assertRaises(OSError):
            data.save(path=self.path_to_file, bump_version=False)

    def tearDown(self) -> None:
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)

