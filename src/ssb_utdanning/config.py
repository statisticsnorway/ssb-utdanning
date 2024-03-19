"""The config holds attributes/constants that the user should be allowed to change before running code, that we do not want as parameters to functions.

Attributes:
ENVIR (str): The environment the application is running in.
SERVICE (str): The service the application is running in.
REGION (str): The region the application is running in.

TESTING (bool): Whether the application is running in testing mode.
MOCKING (bool): Whether the application is running in mocking mode.

DATETIME_FORMAT (str): The datetime format used in filenames.

PROD_FORMATS_PATH (str): The path to the production formats.
"""


import os
import datetime

ENVIR = os.environ.get("DAPLA_ENVIRONMENT", "TEST")
SERVICE = os.environ.get("DAPLA_SERVICE", "JUPYTERLAB")
REGION = os.environ.get("DAPLA_REGION", "ON_PREM")

TESTING = False
MOCKING = False

DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
DEFAULT_DATE = datetime.datetime(2020, 1, 1)

FOUR_DIGITS = ("[0-9]")*4
TWO_DIGITS = ("[0-9]")*2


if REGION == "DAPLA":
    FORMATS_PATH = ""
    SKOLEREG_PATH = ""
    VIGO_PATH = ""
    
    KATALOGER = {}

else:
    FORMATS_PATH = "/ssb/stamme01/utd/utd-felles/formater/"
    SKOLEREG_PATH = "/ssb/stamme01/utd/kat/skolereg/"
    VIGO_PATH = "/ssb/stamme01/utd/katalog/vigo/"
    
    KATALOGER = {
        "skolereg": {
            "glob": f"/ssb/stamme01/utd/kat/skolereg/skolereg_p{FOUR_DIGITS}-{TWO_DIGITS}_v*.parquet",
            "key_cols": ["orgnr", "orgnrbed"],
        }

    }