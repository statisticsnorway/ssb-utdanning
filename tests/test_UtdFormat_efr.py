import unittest

import numpy as np

# Import the UtdFormat class here or include the class definition
from ssb_utdanning.format.formats import UtdFormat


class TestUtdFormat(unittest.TestCase):
    def setUp(self) -> None:
        # Initialize common objects or variables needed for tests
        self.test_dict = {"key1": "value1", "key2": "value2"}
        self.range_dict = {
            "low-10": "barn",
            "11-20": "ungdommer",
            "21-30": "unge_voksne",
            "31-high": "voksne",
        }
        # pass

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
        # Add assertions to test look_in_ranges method
        self.assertEqual(utd_format.look_in_ranges("0"), "barn")
        self.assertEqual(utd_format.look_in_ranges("5"), "barn")
        self.assertEqual(utd_format.look_in_ranges("18"), "ungdommer")
        self.assertEqual(utd_format.look_in_ranges("110"), "voksne")
        self.assertIsNone(utd_format.look_in_ranges("."))

    def test_int_str_confuse(self) -> None:
        utd_format = UtdFormat()
        utd_format["1"] = "value1"
        utd_format[2] = "value2"
        assert utd_format[1] == "value1"
        assert utd_format["2"] == "value2"

    def test_nan_values(self) -> None:
        utd_format = UtdFormat(self.test_dict)
        utd_format[np.nan] = "NaN"
        assert utd_format[np.nan] == "NaN"

        utd_format["OtHer"] = "rest"

        # the dictionary should still recognize other NaN-values than the one specifically saved above, even with an "other" category
        assert utd_format["."] == "NaN"
        assert utd_format["nonexistent_key"] == "rest"

    # Add more test methods to cover other functionalities of the UtdFormat class


if __name__ == "__main__":
    # unittest.main()
    # test = TestUtdFormat()
    # test.setUp()
    # test.test_initialization()
    # test.test_setitem_method()
    # test.test_missing_method()
    # test.test_store_ranges_method()
    # test.test_look_in_ranges_method()
    # test.test_int_str_confuse()
    # test.test_nan_values()
    ...
