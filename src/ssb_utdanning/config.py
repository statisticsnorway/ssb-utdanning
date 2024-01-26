import os

TESTING = False
MOCKING = False

ENVIR = os.environ.get("DAPLA_ENVIRONMENT", "TEST")
SERVICE = os.environ.get("DAPLA_SERVICE", "JUPYTERLAB")
REGION = os.environ.get("DAPLA_REGION", "ON_PREM")

PROD_FORMATS_PATH = "/ssb/stamme01/utd/utd-felles/formater/"
DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
