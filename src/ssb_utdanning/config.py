"""Attributes:
    ENVIR (str): The environment the application is running in.
    SERVICE (str): The service the application is running in.
    REGION (str): The region the application is running in.

    TESTING (bool): Whether the application is running in testing mode.
    MOCKING (bool): Whether the application is running in mocking mode.

    PROD_FORMATS_PATH (str): The path to the production formats.
    DATETIME_FORMAT (str): The datetime format used in filenames.
"""


import fagfunksjoner

MILJO = fagfunksjoner.check_env()
TESTING = False
MOCKING = False
PROD_FORMATS_PATH = "/ssb/stamme01/utd/utd-felles/formater/"
PROD_SKOLEREG_PATH = "/ssb/stamme01/utd/kat/skolereg/"
PROD_VIGO_PATH = "/ssb/stamme01/utd/katalog/vigo/"
