from functools import lru_cache

from ssb_utdanning.katalog.katalog import UtdKatalog


@lru_cache(1)
def get_nuskat(path: str = "") -> UtdKatalog:
    """Retrieves nuskat.
    
    Retrieves a UtdKatalog object representing the Nuskat catalog, which is maintained by 360
    and connects additional data to each nus2000 code. This catalog is typically stored in a
    SAS7BDAT file format and provides detailed classifications.

    Args:
        path (str): The path to the Nuskat catalog file. If not specified, a default
            path is used which points to the latest known version of the Nuskat catalog.

    Returns:
        UtdKatalog: An instance of UtdKatalog loaded with data from the specified Nuskat catalog file.
                    The instance is specifically configured to use 'nus2000' as the key column.

    Notes:
        The function assumes that the file at the specified path is in SAS7BDAT format and that
        the key column named 'nus2000' exists within that file. If the file or the column does
        not exist, an error might be raised when attempting to load the data.
    """
    if not path:
        path = "/ssb/stamme01/utd/nuskat/wk16/nus2000/nus2000.sas7bdat"
    return UtdKatalog(path, key_col="nus2000")
