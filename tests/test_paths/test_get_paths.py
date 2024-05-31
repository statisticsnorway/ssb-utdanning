from ssb_utdanning.paths.get_paths import get_paths
from ssb_utdanning.paths.get_paths import get_path_dates
from ssb_utdanning.paths.get_paths import get_path_latest
from ssb_utdanning.paths.get_paths import get_path_reference_date
from ssb_utdanning.paths.get_paths import get_paths_dates
import unittest
from pathlib import Path
import os
import shutil
from create_mock_path_files import create_mock_datasets
from ssb_utdanning.config import DEFAULT_DATE
import dateutil.parser


class Test_get_paths(unittest.TestCase):
    def setUp(self):
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.folder_path = template_dir / "mock_data"
        self.tearDown()
        os.makedirs(self.folder_path, exist_ok=True)
        create_mock_datasets()

    def test_get_paths(self):
        result = get_paths(
            glob_pattern=str(self.folder_path) + os.sep + "test_data_p2023-10_v*.parquet"
        )
        self.assertEqual(len(result), 3)
        result = get_paths(
            glob_pattern=str(self.folder_path) + os.sep + "test_data*p2023-10_v*.parquet"
        )
        self.assertEqual(len(result), 6)

        w_keywords = get_paths(
            glob_pattern=str(self.folder_path) + os.sep + "test_data*.parquet"
        )
        wo_keywords = get_paths(
            glob_pattern=str(self.folder_path) + os.sep + "test_data*.parquet",
            exclude_keywords="excludethiskeyword",
        )
        self.assertTrue(len(w_keywords) - 15 == len(wo_keywords))

    def test_get_path_latest(self):
        result = get_path_latest(
            glob_pattern=str(self.folder_path) + os.sep + "test_data*.parquet",
            exclude_keywords="excludethiskeyword",
        )
        self.assertEqual(
            result, str(self.folder_path) + os.sep + "test_data_p2024-10_v3.parquet"
        )

    def test_get_paths_dates(self):
        result = get_paths_dates(
            glob_pattern=str(self.folder_path) + os.sep + "test_data*.parquet",
            exclude_keywords="excludethiskeyword",
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 15)
        # check that dates are sorted
        name, date = list(result.keys()), list(result.values())
        self.assertEqual(date, sorted(date, reverse=True))

    def test_get_path_reference_date(self):
        result = get_path_reference_date(
            reference_datetime="2022-09",
            glob_pattern=str(self.folder_path) + os.sep + "two_dates*.parquet",
        )
        self.assertEqual(
            result, str(self.folder_path) + os.sep + "two_dates_p2021-10_p2022-10_v3.parquet"
        )

        with self.assertRaises(ValueError):
            result = get_path_reference_date(
                reference_datetime="2022-10",
                glob_pattern=str(self.folder_path) + os.sep + "two_dates*.parquet",
            )

    def tearDown(self):
        # Clean up test files and folders after tests
        shutil.rmtree(self.folder_path, ignore_errors=True)
