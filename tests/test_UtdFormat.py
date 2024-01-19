import unittest
import numpy as np
import pandas as pd
from pathlib import Path
import os
import shutil
from ssb_utdanning.format.formats import UtdFormat


class TestUtdFormat(unittest.TestCase):
    def setUp(self) -> None:
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.path = template_dir / "test_formats"
        # ensuring test folder does not exist
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)

        # Initialize common objects or variables needed for tests
        self.test_dict = {"key1": "value1", "key2": "value2"}
        self.range_dict = {
            "low-10": "barn",
            "11-20": "ungdommer",
            "21-30": "unge_voksne",
            "31-high": "voksne",
        }
        self.str_nan = [".", "none", "None", "", "NA", "<NA>", "<NaN>", "nan", "NaN"]

    def test_initialization(self) -> None:
        utd_format = UtdFormat(self.test_dict)
        # Add assertions to verify the initialization of the UtdFormat instance
        self.assertTrue(isinstance(utd_format, UtdFormat))
        self.assertTrue(isinstance(utd_format, dict))
        # Add more specific assertions as needed

    def test_setitem_method(self) -> None:
        utd_format = UtdFormat()
        utd_format["test_key"] = "test_value"
        # Add assertions to verify the behavior of __setitem__ method
        self.assertEqual(utd_format["test_key"], "test_value")
        # Add more specific assertions as needed

    def test_missing_method(self) -> None:
        utd_format = UtdFormat()
        # Add assertions to verify the behavior of __missing__ method
        with self.assertRaises(ValueError):
            utd_format["nonexistent_key"]
        utd_format["other"] = "other_value"
        assert utd_format["nonexistent_key"] == "other_value"
        # Add more specific assertions as needed

    def test_store_ranges_method(self) -> None:
        utd_format = UtdFormat()
        # Add test cases to check if ranges are stored properly
        utd_format["0 - 10"] = "range_1"
        utd_format["15 - 20"] = "range_2"
        # Assert for correct storage of ranges
        self.assertIsNone(utd_format.look_in_ranges("-1"))
        for i in range(0, 11):
            assert utd_format[str(i)] == "range_1", f"{i}"
        for j in range(15, 21):
            assert utd_format[str(j)] == "range_2", f"{j}"
        self.assertIsNone(utd_format.look_in_ranges("21"))

    def test_look_in_ranges_method(self) -> None:
        utd_format = UtdFormat(self.range_dict)
        utd_format["other"] = "rest"
        utd_format["."] = "NaN"
        assert utd_format.look_in_ranges("0") == "barn"
        assert utd_format.look_in_ranges("5") == "barn"
        assert utd_format.look_in_ranges("18") == "ungdommer"
        assert utd_format.look_in_ranges("110") == "voksne"

    def test_int_str_confuse(self) -> None:
        utd_format = UtdFormat()
        utd_format["1"] = "value1"
        utd_format[2] = "value2"
        assert utd_format[1] == "value1"
        assert utd_format["2"] == "value2"

    def test_check_if_na(self) -> None:
        utd_format = UtdFormat()
        for nan in self.str_nan:
            assert utd_format.check_if_na(nan)
        assert utd_format.check_if_na(np.nan)
        assert utd_format.check_if_na(pd.NA)
        assert utd_format.check_if_na(None)

    def test_allround(self) -> None:
        utd_format = UtdFormat(self.range_dict)
        utd_format[np.nan] = "NaN"
        assert utd_format[np.nan] == "NaN"

        utd_format["OtHer"] = "rest"
        assert utd_format["other"] == "rest"

        # the dictionary should still recognize other NaN-values than the one specifically saved above, even with an "other" category
        for nan in self.str_nan:
            assert utd_format[nan] == "NaN"

        # also checking non-string nan values
        assert utd_format[np.nan] == "NaN"
        assert utd_format[pd.NA] == "NaN"
        assert utd_format[None] == "NaN"

        assert utd_format["nonexistent_key"] == "rest"

    def test_store(self) -> None:
        utd_format = UtdFormat(self.range_dict)
        assert len(os.listdir(self.path)) == 0
        print(os.listdir(self.path))
        utd_format.store(format_name="test", output_path=str(self.path), force=True)
        assert len(os.listdir(self.path)) == 1
        print(os.listdir(self.path))

    def tearDown(self) -> None:
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)
