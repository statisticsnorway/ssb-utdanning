# AUTOGENERATED! DO NOT EDIT! File to edit: 01_klass.ipynb (unless otherwise specified).

__all__ = ['get_pandas']

# Cell
import requests, json, pandas as pd

# Cell
# Med "exports"-kommentaren over så blir koden med i både modulen som eksporteres og dokumentasjonen.
# Med "export"- kommentaren blir ikke kildekoden med i docsene
def get_pandas(URL, level):
    """
    Get pandas dataframe from the KLASS-API

    Parameters
    ----------
    URL : str \n
        url to the API-endpoint you are interested in
    level : str \n
        level of the json to convert, for example 'classificationItems' or 'correspondenceMaps'

    Returns
    -------
    pandas.DataFrame() \n
        The returned json at the level requested, converted to a pandas dataframe

    Further Development
    -------
    Error catching when "level" is not found in the returned json, show the top level json-keys then?

    """

    r = requests.get(URL)
    r = r.content.decode('utf8').replace("\'", '')
    r = json.loads(r)
    r = pd.json_normalize(r[level])
    return r