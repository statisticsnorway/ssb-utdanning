"""Attributes:
    ENVIR (str): The environment the application is running in.
    SERVICE (str): The service the application is running in.
    REGION (str): The region the application is running in.

    TESTING (bool): Whether the application is running in testing mode.
    MOCKING (bool): Whether the application is running in mocking mode.

    DATETIME_FORMAT (str): The datetime format used in filenames.

    PROD_FORMATS_PATH (str): The path to the production formats.
"""

import os


ENVIR = os.environ.get("DAPLA_ENVIRONMENT", "TEST")
SERVICE = os.environ.get("DAPLA_SERVICE", "JUPYTERLAB")
REGION = os.environ.get("DAPLA_REGION", "ON_PREM")

TESTING = False
MOCKING = False

DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"

PROD_FORMATS_PATH = "/ssb/stamme01/utd/utd-felles/formater/"
PROD_SKOLEREG_PATH = "/ssb/stamme01/utd/kat/skolereg/"
PROD_VIGO_PATH = "/ssb/stamme01/utd/katalog/vigo/"
