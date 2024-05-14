from ssb_utdanning import UtdKatalog
from ssb_utdanning import UtdData
import numpy as np
import pandas as pd
import os
import unittest
from pathlib import Path
import shutil
from create_mock_katalogs import create_mock_katalog, create_mock_dataset

os.environ["DAPLA_REGION"] = "ON_PREM"


class TestUtdKatalog(unittest.TestCase):
    def setUp(self) -> None:
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.path = template_dir / "mock_data"
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)
        self.katalog_path = create_mock_katalog()
        self.data_path = create_mock_dataset()

    def test_init(self):
        katalog = UtdKatalog(key_cols="ident", path=self.katalog_path)
        self.assertIsInstance(katalog, UtdKatalog)
        self.assertIsInstance(katalog.key_cols, list)

        with self.assertRaises(TypeError):
            katalog = UtdKatalog(key_cols=["ident", 123], path=self.katalog_path)

        del katalog
        katalog = UtdKatalog(key_cols=["ident"], path=self.katalog_path)
        self.assertIsInstance(katalog, UtdKatalog)
        self.assertIsInstance(katalog.key_cols, list)

    def test_merge_on(self):
        katalog = UtdKatalog(key_cols=["ident"], path=self.katalog_path)
        data = UtdData(path=self.data_path)
        result = katalog.merge_on(dataset=data, key_col_in_data="ident")
        self.assertTrue("height" in result.columns)
        self.assertTrue("age" in result.columns)
        self.assertTrue("sex" in result.columns)
        self.assertTrue("_merge" in result.columns)
        self.assertEqual(len(result), len(data.data))

    def test_to_dict(self):
        katalog = UtdKatalog(key_cols=["ident"], path=self.katalog_path)
        test_dict = katalog.to_dict(col="age")
        self.assertIsInstance(test_dict, dict)
        self.assertEqual(len(test_dict), len(katalog.data))
        self.assertEqual(list(test_dict.keys()), katalog.data["ident"].to_list())
        self.assertEqual(list(test_dict.values()), katalog.data["age"].to_list())

    def test_apply_format(self):
        katalog = UtdKatalog(key_cols=["ident"], path=self.katalog_path)
        data = UtdData(path=self.data_path)
        data_n_col = len(data.data.columns)

        result = katalog.apply_format(data.data)
        self.assertEqual(data_n_col + 1, len(result.columns))

        del data, result
        data = UtdData(path=self.data_path)
        data_n = len(data.data)
        katalog.apply_format(
            data.data,
            catalog_col_name="sex",
            data_key_col_name="ident",
            catalog_key_col_name="ident",
            new_col_data_name="data_sex",
        )
        self.assertTrue("data_sex" in data.data.columns)
        self.assertEqual(len(data.data), data_n)

    def tearDown(self):
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)
