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
from pathlib import Path
import shutil
import ssb_utdanning
from unittest import mock
import pandas as pd


@mock.patch(
    "ssb_utdanning.orgnrkontroll.orgnrkontroll.VIGO_PATH",
    new=os.getcwd() + "/mock_data/",
)
@mock.patch(
    "ssb_utdanning.orgnrkontroll.orgnrkontroll.SKOLEREG_PATH",
    new=os.getcwd() + "/mock_data/",
)
class Test_orgnrkontroll(unittest.TestCase):
    # @mock.patch('ssb_utdanning.orgnrkontroll.orgnrkontroll.SKOLEREG_PATH', new=str(os.getcwd() + '/mock_data'))
    def setUp(self) -> None:
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.path = template_dir / "mock_data/"
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)
        create_mock_skolereg()
        create_mock_vigo()
        create_mock_data()

    def get_data_year(self, year):
        return UtdData(glob_pattern=str(self.path) + f"/data_p{year}*.parquet")

    def test_get_skolereg(self):
        year = 2022
        result = orgnrkontroll_module.get_skolereg(year=year)
        self.assertIsInstance(result, UtdKatalog)
        self.assertTrue(len(result.data.columns), 4)
        del result
        result = orgnrkontroll_module.get_skolereg()
        self.assertTrue(
            str(result.path).split("/")[-1] == "skolereg_p2023-10_v1.parquet"
        )
        del result
        result = orgnrkontroll_module.get_skolereg(year=2022, sub_category="vgskoler")
        self.assertTrue(
            str(result.path).split("/")[-1] == "skolereg_vgskoler_p2022-10_v1.parquet"
        )

    def test_get_vigo_skole(self):
        year = 2022
        result = orgnrkontroll_module.get_vigo_skole(year=2022)
        self.assertIsInstance(result, UtdKatalog)
        self.assertTrue(len(result.data.columns), 3)
        del result
        result = orgnrkontroll_module.get_vigo_skole()
        self.assertTrue(
            str(result.path).split("/")[-1], "vigo_skole_testfil_slett_p2023_v1.parquet"
        )

    def test_orgnrkontroll_func(self):
        year = 2022
        data = self.get_data_year(year=year)
        # testing different input parameters

        # orgnr cols parameters are equal
        with self.assertRaises(ValueError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr",
                orgnrbed_col_innfil="orgnr",
            )
        # inn-data does not contain orgnr-cols and fskolenrcol
        # for inn-data of type UtdData
        with self.assertRaises(ValueError):
            self.assertIsInstance(data, UtdData)
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr_non",
                orgnrbed_col_innfil="orgnrbed",
                fskolenr_col_innfil="fskolenr",
            )
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr",
                orgnrbed_col_innfil="orgnrbed_non",
                fskolenr_col_innfil="fskolenr",
            )
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr",
                orgnrbed_col_innfil="orgnrbed",
                fskolenr_col_innfil="fskolenr_non",
            )
        # for inn-data of type pd.DataFrame
        data = data.data
        with self.assertRaises(ValueError):
            self.assertIsInstance(data, pd.DataFrame)
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr_non",
                orgnrbed_col_innfil="orgnrbed",
                fskolenr_col_innfil="fskolenr",
            )
        with self.assertRaises(ValueError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr",
                orgnrbed_col_innfil="orgnrbed_non",
                fskolenr_col_innfil="fskolenr",
            )
        with self.assertRaises(ValueError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                orgnr_col_innfil="orgnr",
                orgnrbed_col_innfil="orgnrbed",
                fskolenr_col_innfil="fskolenr_non",
            )
        del data
        data = self.get_data_year(year=year)

        # verify that keep cols variables are list or set
        with self.assertRaises(TypeError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data,
                year=year,
                skolereg_keep_cols="not set or list",
            )
        with self.assertRaises(TypeError):
            result = orgnrkontroll_module.orgnrkontroll_func(
                data=data, year=year, vigo_keep_cols="not set or list"
            )
        # merge on specific columns from skolereg and vigo
        skolereg_keep_cols = ["skoletype"]
        vigo_keep_cols = ["vigo_var2"]
        result = orgnrkontroll_module.orgnrkontroll_func(
            data=data,
            year=year,
            skolereg_keep_cols=skolereg_keep_cols,
            vigo_keep_cols=vigo_keep_cols,
        )
        self.assertTrue(skolereg_keep_cols[0] in list(result.data.columns))
        self.assertTrue(vigo_keep_cols[0] in list(result.data.columns))

        # general test
        result = orgnrkontroll_module.orgnrkontroll_func(data=data, year=year)
        self.assertTrue("_merge" in list(result.data.columns))
        self.assertTrue(len(data.data.columns) < len(result.data.columns))

    def tearDown(self):
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)


# +
# test = Test_orgnrkontroll()
# test.setUp()
# test.test_get_skolereg()
# test.test_get_vigo_skole()
# test.test_orgnrkontroll_func()

# +
# path = '/ssb/stamme01/utd_pii/grskavsl/wk16/MOD/ssb-prod-gro-grunnskole-produkt/klargjorte-data/'
# filename = 'kag_nudb_p2022_p2023_v1.parquet'
# data = UtdData(path=path+filename)
# data.data = data.data[['orgnr', 'orgnrbed', 'orgnrforetak', 'fskolenr']]

# +
# test = orgnrkontroll_module.orgnrkontroll_func(data,
#               year=2023,
#               orgnr_col_innfil= 'orgnr',
#               orgnrbed_col_innfil = 'orgnrbed',
#               skolereg_keep_cols=['nace1_sn07', 'nace2_sn07', 'nace3_sn07'])
# -
