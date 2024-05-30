from unittest import mock
import pandas as pd
import datetime
from ssb_utdanning.config import DATETIME_FORMAT
from ssb_utdanning.format.formats import get_path


def mocked_info_stored_formats(var: str) -> pd.DataFrame:
    df_info = pd.DataFrame(
        {
            "test_name": ["newest_format", "oldes_format"],
            "date_original": ["2024-01-15T12-00-00", "2023-01-15T12-00-00"],
            "date_datetime": [
                datetime.datetime.strptime("2024-01-15T12-00-00", DATETIME_FORMAT),
                datetime.datetime.strptime("2023-01-15T12-00-00", DATETIME_FORMAT),
            ],
            "path": ["newest_path", "oldest_path"],
        }
    )
    return df_info


@mock.patch(
    "ssb_utdanning.format.formats.info_stored_formats",
    side_effect=mocked_info_stored_formats,
)
def test_get_path(mock_get: mock.MagicMock) -> None:
    path = get_path("test")
    assert path == "newest_path"

    path = get_path("test", date="2023-01-16")
    assert path == "oldest_path"
