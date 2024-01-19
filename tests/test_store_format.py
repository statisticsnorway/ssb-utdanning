import time
import json
import os
import shutil
import unittest
from pathlib import Path
from unittest import mock
import numpy as np
import ssb_utdanning
from ssb_utdanning.format.formats import UtdFormat
from ssb_utdanning.format.formats import store_format_prod
from write_test_formats import write_test_formats


def mock_is_different_from_last_time(format_name: str, format_content: UtdFormat) -> bool:
    path = Path(os.getcwd()) / 'test_formats'
    files = os.listdir(path)
    if not len(files):
        return True
    split_files = [files[i].split('_') for i in range(len(files))]
    shortnames = np.array((split_files))[:,0]
    if format_name in shortnames:
        #path = get_path(format_name, date="latest")
        if path:
            # find the file to compare with
            idx = []
            for i in range(len(shortnames)):
                if format_name == shortnames[i]:
                    idx.append(i)
            files_to_read = [files[i] for i in idx]
            to_read = sorted(files_to_read)[0]
            path = path / to_read
            with open(path) as format_json:
                content = json.load(format_json)
            if content != format_content:
                return True
    # No previous format found
    else:
        return True
    # print("Content of format looks the same as previous version, not saving.")
    return False


class TestStoreFormat(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary folder and add test JSON files for testing
        # Create test files with different names and date patterns
        # Set up a test directory structure and add some test JSON files
        template_dir = Path(os.getcwd())
        self.path = template_dir / 'test_formats'
        # make sure the tree is clean
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)
        # Create test JSON files
        self.test_files, self.dates, self.dictionaries= write_test_formats(self.path, store=False)
        
    def shortname_files_in_path(self) -> list[str]:
        files = os.listdir(self.path)
        split_files = [files[i].split('_') for i in range(len(files))]
        if len(files):
            shortnames = list(np.array((split_files))[:,0])
            return shortnames
        return []
    
    @mock.patch('ssb_utdanning.format.formats.is_different_from_last_time', side_effect=mock_is_different_from_last_time)
    def test_store_format_prod(self, mock_get: mock.MagicMock) -> None:
        # checking for file in folder, write file, then check again
        for i, file in enumerate(self.test_files):
            shortnames = self.shortname_files_in_path()
            assert self.test_files[i].split('_')[0] not in shortnames
            store_format_prod({list(self.dictionaries[i].keys())[0]: UtdFormat(self.dictionaries[i][list(self.dictionaries[i].keys())[0]])}, output_path = str(self.path))
            shortnames = self.shortname_files_in_path()
            assert self.test_files[i].split('_')[0] in shortnames
        # try and write file again, sohuld not be possible because content is the same
        shortnames = self.shortname_files_in_path()
        n_file_files = len(shortnames)
        assert n_file_files == 2
        store_format_prod({list(self.dictionaries[0].keys())[0]: UtdFormat(self.dictionaries[0][list(self.dictionaries[0].keys())[0]])}, output_path = str(self.path))
        shortnames = self.shortname_files_in_path()
        n_file_files = len(shortnames)
        assert n_file_files == 2
        
        # change dictionary slightly and write again. check that new file is written to folder
        frmt = self.dictionaries[0]
        self.dictionaries[0]['file']['testkey'] = 'testvalue'
        # timedelay to not overwrite file with same timestamp as previous file
        time.sleep(3)
        store_format_prod({list(self.dictionaries[0].keys())[0]: UtdFormat(self.dictionaries[0][list(self.dictionaries[0].keys())[0]])}, output_path = str(self.path))
        shortnames = self.shortname_files_in_path()
        n_file_files = len(shortnames)
        assert n_file_files == 3
        
    def tearDown(self) -> None:
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)

