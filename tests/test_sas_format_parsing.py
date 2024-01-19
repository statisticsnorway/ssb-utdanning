import unittest
from unittest import mock
import shutil
from pathlib import Path
import os
import json
from create_folder_w_sasfiles import create_folder_w_sasfiles
from ssb_utdanning.format.formats import UtdFormat
from ssb_utdanning.format.sas_format_parsing import process_single_sasfile
from ssb_utdanning.format.sas_format_parsing import batch_process_folder_sasfiles
from ssb_utdanning.format.sas_format_parsing import parse_sas_script
import ssb_utdanning


def local_get_format(path: Path, frmtname: str) -> UtdFormat:
    dir_files = os.listdir(path)
    shortnames = [file.split("_")[0] for file in dir_files]
    idx = []
    for i in range(len(shortnames)):
        if frmtname == shortnames[i]:
            idx.append(i)
    files_to_read = [dir_files[i] for i in idx]
    to_read = sorted(files_to_read)[0]

    with open(path / to_read) as format_json:
        ord_dict = json.load(format_json)
    return UtdFormat(ord_dict)


def mock_is_different_from_last_time(
    format_name: str, format_content: UtdFormat
) -> bool:
    return True


class TestSasFormatParsing(unittest.TestCase):
    def setUp(self) -> None:
        template_dir = Path(os.getcwd())
        self.path = template_dir / "test_formats"
        # making sure testformat folder does not exist
        self.tearDown()

        # creating sas test files containing sas-style formats
        self.filenames, self.formats = create_folder_w_sasfiles(self.path)
        self.frmt_shortnames = [f"frmt{i}" for i in range(1, 5)]

    @mock.patch(
        "ssb_utdanning.format.formats.is_different_from_last_time",
        side_effect=mock_is_different_from_last_time,
    )
    def test_process_single_sasfile(self, mock_get: mock.MagicMock) -> None:
        dir_files = os.listdir(self.path)
        shortnames = [file.split("_")[0] for file in dir_files]
        assert self.frmt_shortnames[0] not in shortnames
        assert self.frmt_shortnames[1] not in shortnames

        # filename = str(self.path / self.filenames[0])
        filename = self.path / self.filenames[0]
        # process_single_sasfile(file=filename, output_path=str(self.path))
        process_single_sasfile(file=filename, output_path=self.path)

        dir_files = os.listdir(self.path)
        shortnames = [file.split("_")[0] for file in dir_files]

        # the two formats contained in testfrmt1 should exist
        assert self.frmt_shortnames[0] in shortnames
        assert self.frmt_shortnames[1] in shortnames

        # checking content of formats
        frmt1 = local_get_format(self.path, self.frmt_shortnames[0])
        assert frmt1 == UtdFormat(self.formats[0])

        frmt2 = local_get_format(self.path, self.frmt_shortnames[1])
        assert frmt2 == UtdFormat(self.formats[1])

    @mock.patch(
        "ssb_utdanning.format.formats.is_different_from_last_time",
        side_effect=mock_is_different_from_last_time,
    )
    def test_batch_process_folder_sasfiles(self, mock_get: mock.MagicMock) -> None:
        # delete file in test_format folder and build sas files again
        self.tearDown()
        self.setUp()

        # making sure the formats are not in test_format folder
        dir_files = os.listdir(self.path)
        shortnames = [file.split("_")[0] for file in dir_files]
        assert self.frmt_shortnames[0] not in shortnames
        assert self.frmt_shortnames[1] not in shortnames

        # parsing sas files as batch and converting to json
        # batch_process_folder_sasfiles(sas_files_path = str(self.path),
        #                               output_path = str(self.path))
        batch_process_folder_sasfiles(sas_files_path=self.path, output_path=self.path)

        # checking that json files with correct names are created
        dir_files = os.listdir(self.path)
        shortnames = [file.split("_")[0] for file in dir_files]

        for i in range(len(self.frmt_shortnames)):
            assert self.frmt_shortnames[i] in shortnames

        # reading json files and checking content
        for j in range(len(self.frmt_shortnames)):
            frmt_j = local_get_format(self.path, self.frmt_shortnames[j])
            assert frmt_j == UtdFormat(self.formats[j])

    def tearDown(self) -> None:
        # Clean up test files and folders after tests
        shutil.rmtree(self.path, ignore_errors=True)
