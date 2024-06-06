from ssb_utdanning.orgnrkontroll.orgnrkontroll import get_skolereg, get_vigo_skole
import ssb_utdanning.orgnrkontroll.orgnrkontroll as orgnrkontroll_module
import ssb_utdanning
import os
from ssb_utdanning import orgnrkontroll_func
from ssb_utdanning import UtdData, UtdKatalog
from create_mock_orgnr_files import (
    create_mock_skolereg,
    create_mock_vigo,
    create_mock_data,
)
import unittest
from typeguard import suppress_type_checks
from pathlib import Path
import shutil
import ssb_utdanning
from unittest import mock
import pandas as pd
from typeguard import suppress_type_checks


@mock.patch(
    "ssb_utdanning.orgnrkontroll.orgnrkontroll.VIGO_PATH",
    new=str(Path(os.getcwd()) / "mock_data"),
)
@mock.patch(
    "ssb_utdanning.orgnrkontroll.orgnrkontroll.SKOLEREG_PATH",
    new=str(Path(os.getcwd()) / "mock_data"),
)
class Test_orgnrkontroll(unittest.TestCase):
    # @mock.patch('ssb_utdanning.orgnrkontroll.orgnrkontroll.SKOLEREG_PATH', new=str(os.getcwd() + '/mock_data'))
    def setUp(self) -> None:
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.path = template_dir / "mock_data"
        self.year = 2022
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)
        create_mock_skolereg()
        create_mock_vigo()
        create_mock_data()
        self.data = self.get_data_year(year=self.year)

    def get_data_year(self, year) -> UtdData:
        return UtdData(glob_pattern_latest=str(self.path / f"data_p{year}*.parquet"))

    def test_get_skolereg(self):
        result = orgnrkontroll_module.get_skolereg(year=self.year)
        self.assertIsInstance(result, UtdKatalog)
        self.assertTrue(len(result.data.columns), 4)

    def test_get_skolereg_latest(self):
        result = orgnrkontroll_module.get_skolereg()
        self.assertEqual(
            str(result.path).split(os.sep)[-1], "skolereg_p2023-10_v1.parquet"
        )

    def test_get_skolereg_subcategory(self):
        result = orgnrkontroll_module.get_skolereg(year=self.year, sub_category="vgskoler")
        self.assertEqual(
            str(result.path).split(os.sep)[-1], "skolereg_vgskoler_pself.year-10_v1.parquet"
        )

    def test_get_vigo_skole(self):
        result = orgnrkontroll_module.get_vigo_skole(year=self.year)
        self.assertIsInstance(result, UtdKatalog)
        self.assertTrue(len(result.data.columns), 3)

    def test_get_vigo_latest(self):
        result = orgnrkontroll_module.get_vigo_skole()
        self.assertTrue(
            str(result.path).split(os.sep)[-1],
            "vigo_skole_testfil_slett_p2023_v1.parquet",
        )

    def test_missing_orgnr_col_in_data(self):
        data = self.get_data_year(year=self.year)
        # inn-data does not contain orgnr-cols and fskolenrcol
        # for inn-data of type UtdData
        with self.assertRaises(ValueError):
            self.assertIsInstance(self.data, UtdData)
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=self.data,
                year=self.year,
                orgnr_col_innfil="orgnr_non",
                fskolenr_col_innfil="fskolenr",
            )

    def test_missing_fskolnr_col_in_data(self):
        data = self.get_data_year(year=self.year)
        with self.assertRaises(ValueError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=self.data,
                year=self.year,
                orgnr_col_innfil="orgnr",
                fskolenr_col_innfil="fskolenr_non",
            )

    def test_missing_orgnr_col_data_is_DataFrame(self):
        # for inn-data of type pd.DataFrame
        data = self.get_data_year(year=self.year)
        data = data.data
        with self.assertRaises(ValueError):
            self.assertIsInstance(data, pd.DataFrame)
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=self.data,
                year=self.year,
                orgnr_col_innfil="orgnr_non",
                fskolenr_col_innfil="fskolenr",
            )

    def test_missing_fskolenr_col_data_is_DataFrame(self):
        data = self.get_data_year(year=self.year)
        data = data.data
        with self.assertRaises(ValueError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=self.data,
                year=self.year,
                orgnr_col_innfil="orgnr",
                fskolenr_col_innfil="fskolenr_non",
            )

    @suppress_type_checks
    def test_keep_col_is_list_or_set(self):
        data = self.get_data_year(year=self.year)
        with self.assertRaises(TypeError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=self.data,
                year=self.year,
                skolereg_keep_cols="not set or list",  #
            )

    @suppress_type_checks
    def test_merge_on_specific_columns(self):
        with self.assertRaises(TypeError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=self.data, year=self.year, vigo_keep_cols="not set or list"
            )

    def test_merge_on_specific_column(self):
        data = self.get_data_year(year=self.year)
        # merge on specific columns from skolereg and vigo
        skolereg_keep_cols = ["skoletype"]
        vigo_keep_cols = ["vigo_var2"]
        result = orgnrkontroll_module.orgnrkontroll_func(
            data=self.data,
            year=self.year,
            skolereg_keep_cols=skolereg_keep_cols,
            vigo_keep_cols=vigo_keep_cols,
        )
        self.assertIn(skolereg_keep_cols[0], list(result.data.columns))
        self.assertIn(vigo_keep_cols[0], list(result.data.columns))

    def test_verify_merge_result(self):
        data = self.get_data_year(year=self.year)
        # general test
        result = orgnrkontroll_module.orgnrkontroll_func(data=data, year=self.year)
        self.assertIn("_merge", list(result.data.columns))
        self.assertTrue(len(self.data.data.columns) < len(result.data.columns))

    def tearDown(self):
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)
