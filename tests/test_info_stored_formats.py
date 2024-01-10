import unittest
import pandas as pd
import os
import dateutil.parser
import json
from ssb_utdanning.format.formats import info_stored_formats, get_format
from ssb_utdanning.config import PROD_FORMATS_PATH

PROD_FORMATS_PATH



get_format('eierf')


# Assuming PROD_FORMATS_PATH is defined somewhere accessible or you can define it in the test script

# +
# def info_stored_formats(select_name: str = "", path_prod: str = PROD_FORMATS_PATH) -> pd.DataFrame:
#     # Function definition remains the same
# -

class TestInfoStoredFormats(unittest.TestCase):
    def setUp(self):
        # Create a temporary folder and add test JSON files for testing

        # Create test files with different names and date patterns
        # Set up a test directory structure and add some test JSON files

        # self.test_folder_path = "/path/to/test/folder"
        self.test_folder_path = os.getcwd() + '/'
        if 'test_formats' not in os.listdir():
            os.mkdir(self.test_folder_path + 'test_formats')
        self.test_folder_path += 'test_formats/'

        # Create test JSON files
        self.test_files = [
            "file_2023-05-10.json",
            "anotherfile_2024-01-09.json"
        ]
        self.dates = [self.test_files[0][-15:-5], self.test_files[1][-15:-5]]
        frmt1 = {'file': dict(zip([f"key{i}" for i in range(1,6)], [f"value{j}" for j in range(1, 6)]))}
        frmt2 = {'anotherfile': dict(zip([f"{i}" for i in range(1,6)], [f"category{j}" for j in range(1, 6)]))}
        dictionaries = [frmt1, frmt2]
        for k, file_name in enumerate(self.test_files):
            with open(os.path.join(self.test_folder_path, file_name), "w") as json_file:
                json.dump(dictionaries[k], json_file)

    def test_folder_not_found(self):
        with self.assertRaises(OSError):
            # Test when folder does not exist
            info_stored_formats(path_prod="/nonexistent/path/")

    def test_extract_information(self):
        # Test extracting information from file paths
        display(info_stored_formats(path_prod=self.test_folder_path))
        for i, filename in enumerate(self.test_files):
            shortname = filename.split('_')[0]
            df_info = info_stored_formats(shortname, path_prod=self.test_folder_path)
            # Check if the returned object is a DataFrame
            assert isinstance(df_info, pd.DataFrame)
            assert list(df_info['date_original'])[0] == self.dates[i]
            assert list(df_info['name'])[0] == shortname
            assert list(df_info['path'])[0] == self.test_folder_path + filename
        # Add more specific assertions based on the expected behavior

    def test_select_specific_name(self):
        # Test selecting a specific name
        for i, filename in enumerate(self.test_files):
            shortname = filename.split('_')[0]
            df_info = info_stored_formats(shortname, path_prod=self.test_folder_path)
            # Check if the returned object is a DataFrame
            assert isinstance(df_info, pd.DataFrame)
            assert list(df_info['date_original'])[0] == self.dates[i]
            assert list(df_info['name'])[0] == shortname
            assert list(df_info['path'])[0] == self.test_folder_path + filename

        # Add assertions to check if the returned DataFrame contains expected data based on the selected name
        #assert df_info == "test content"
    # Add more test methods for different scenarios within info_stored_formats function
    
    def tearDown(self):
        # Clean up test files and folders after tests
        if os.path.exists(self.test_folder_path):
            for file_name in self.test_files:
                os.remove(self.test_folder_path + file_name)
            if '.ipynb_checkpoints' in os.listdir(self.test_folder_path):
                os.rmdir(self.test_folder_path + '.ipynb_checkpoints')
            os.rmdir(self.test_folder_path)

test = TestInfoStoredFormats()
test.setUp()
test.test_folder_not_found()
test.test_extract_information()
# test.test_select_specific_name()
test.tearDown()

if __name__ == '__main__':
    # unittest.main()

info_stored_formats('file', path_prod = os.getcwd() + '/test_formats/')


