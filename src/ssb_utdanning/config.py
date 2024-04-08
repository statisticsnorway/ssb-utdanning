"""The config for the ssb-utdanning package contains values the user might want to change.

Attributes:
    MILJO (str): The environment the application is running in.
    TESTING (bool): Whether the application is running in testing mode.
    MOCKING (bool): Whether the application is running in mocking mode.
    PROD_FORMATS_PATH (str): The path to the production formats.
"""
import os

TESTING = False
MOCKING = False

ENVIR = os.environ.get("DAPLA_ENVIRONMENT", "TEST")
SERVICE = os.environ.get("DAPLA_SERVICE", "JUPYTERLAB")
REGION = os.environ.get("DAPLA_REGION", "ON_PREM")

PROD_FORMATS_PATH = "/ssb/stamme01/utd/utd-felles/formater/"
DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
