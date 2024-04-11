from importlib import reload
import ssb_utdanning
#from ssb_utdanning import UtdData
from pathlib import Path
import unittest
import os
import pandas as pd
from create_mock_data import create_mock_data
import shutil
import glob
import sys

os.environ['DAPLA_REGION'] = 'DAPLA'
# del os.environ['DAPLA_REGION']
os.environ.get("DAPLA_REGION", "ON_PREM")


class TestUtdData(unittest.TestCase):
    def setUp(self, filename: str = "data_p2024-10_v1.parquet") -> None:
        # setting up folder to store formats
        template_dir = Path(os.getcwd())
        self.path = template_dir / "mock_data"
        self.tearDown()
        os.makedirs(self.path, exist_ok=True)
        self.path_to_file = self.path/filename
        # creating file containing mock data
        create_mock_data(self.path_to_file)
        self.data = pd.read_parquet(self.path_to_file)
        
    def test_init(self):
        
    def test_correct_check_path(self):
        # DAPLA
        os.environ['DAPLA_REGION'] = 'DAPLA'
        #ssb_utdanning.config.REGION = 'DAPLA'
        #del UtdData
        #reload(sys.modules['ssb_utdanning.data.utd_data'])
        #reload(sys.modules['ssb_utdanning'])
        # data = UtdData(path=self.path_to_file)
        data = ssb_utdanning.UtdData(path=self.path_to_file)
        # print(os.environ.get("DAPLA_REGION", "ON_PREM"))
        # data.path = None
        # data._correct_check_path(str(self.path_to_file))
        # print(type(data.path))
