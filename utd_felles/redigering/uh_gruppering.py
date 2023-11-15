"""
NB! NOT TESTED PROPERLY ON REAL DATA. SHOULD IDEALLY RUN ON THE SAME SOURCE DATA IN PYTHON AND IN SAS IN ORDER TO ENSURE THAT THE BEHAVIOUR IS AS EXPECTED. 
    PARTICULARLY BECAUSE THE ORDER OF THE CONDITIONS IS CRUCIAL: LATER CONDITIONS OVERWRITE EARLINER ONES. 
"""

import pandas as pd


def grupper_ktrinn(df: pd.DataFrame, col_name: str = "ktrinn", req_cols: list = ["kurstrin", "kltrinn", "fagskoleutd"], default: pd._libs.missing.NAType = pd.NA) -> pd.DataFrame:
    """
    Group a DataFrame based on conditions related to 'kurstrin', 'kltrinn', and 'fagskoleutd'.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame with "kurstrin", "kltrinn, and fagskoleutd" columns.
    col_name : str
        Name of the column to store grouping information. Defaults to 'ktrinn'.
    req_cols : list, optional
        List of column names that must be present in the DataFrame. Defaults to [kurstrin", "kltrinn", "fagskoleutd"].
    default : optional
        Default value for rows not meeting any conditions. Defaults to pd.NA.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column ('col_name') indicating the group based on conditions.

    Raises
    ------
    ValueError
        Checks if the required columns are in the DataFrame. Raises an ValueError if not.

    Notes
    -----
    The order of conditions is crucial. Later conditions overwrite earlier ones.
    """
    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}.")
    df = df.copy()
    conditions = {
        "4": (df["kurstrin"].notna()),
        "5": (df["fagskoleutd"] == "10"),
        "5": ((df["kurstrin"] == "U") & (df["kltrinn"].isin(["14", "15"]))),
        "3": (df["kurstrin"].isin(["P", "Q", "K", "R", "I", "D"]) & (df["kltrinn"] == "13")),
        "2": (df["kurstrin"].isin(["H", "J", "K", "R", "I", "D"]) & (df["kltrinn"] == "12")),
        "1": (df["kurstrin"].isin(["A", "B", "C", "K", "R", "D"]) & (df["kltrinn"] == "11"))
    }
    for key, cond in conditions.items():
        df.loc[cond, col_name] = key
    df[col_name] = df[col_name].fillna(default)
    return df

def grupper_skobo(df: pd.DataFrame, col_name: str = "skobo", req_cols: list = ["kommnr", "skolekom"], default: pd._libs.missing.NAType = pd.NA) -> pd.DataFrame:
    """
    Group a DataFrame based on conditions related to 'kommnr' and 'skolekom'.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame with 'kommnr' and 'skolekom' columns.
    col_name : str
        Name of the column to store grouping information.
    req_cols : list, optional
        List of column names that must be present in the DataFrame. Defaults to ["kommnr", "skolekom"].
    default : optional
        Default value for rows not meeting any conditions. Defaults to pd.NA.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column ('col_name') indicating the group based on conditions.

    Raises
    ------
    ValueError
        Checks if the required columns are in the DataFrame. Raises an ValueError if not.

    Notes
    -----
    The order of conditions is crucial. Later conditions overwrite earlier ones.
    """
    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}.")
    df = df.copy()
    conditions = {
        "1": (df["kommnr"] == df["skolekom"]),
        "2": (df["kommnr"].str[:2] == df["skolekom"].str[:2]),
        "3": (df["kommnr"].str[:2] != df["skolekom"].str[:2])
    }
    for key, cond in conditions.items():
        df.loc[cond, col_name] = key
    df[col_name] = df[col_name].fillna(default)
    return df

def grupper_utd(df: pd.DataFrame, col_name: str = "utd", req_cols: list = ["kilde", "naering", "nus2000", "skolekom", "studretn", "fagskoleutd", "komp"], default: pd._libs.missing.NAType = pd.NA) -> pd.DataFrame:
    """
    Group a DataFrame based on conditions related to "kilde", "naering", "nus2000", "skolekom", "studretn", "fagskoleutd", and "komp".

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame with "kilde", "naering", "nus2000", "skolekom", "studretn", "fagskoleutd", and "komp" columns.
    col_name : str
        Name of the column to store grouping information.
    req_cols : list, optional
        List of column names that must be present in the DataFrame. Defaults to ["kilde", "naering", "nus2000", "skolekom", "studretn", "fagskoleutd", "komp"].
    default : optional
        Default value for rows not meeting any conditions. Defaults to pd.NA.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional column ('col_name') indicating the group based on conditions.
        
    Raises
    ------
    ValueError
        Checks if the required columns are in the DataFrame. Raises an ValueError if not.

    Notes
    -----
    The order of conditions is crucial. Later conditions overwrite earlier ones.
    """
    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}.")
    df = df.copy()
    conditions = {
        # Grunnskoler
        "100": ((df["kilde"] == "10") | ((df["naering"].isin(["85.100", "85.201", "85.202", "85.203"])) & (df["nus2000"].str[0].isin(["0", "1", "2"])))),
        # Annen universitets- og høgskoleutdanning
        "320": ((df["naering"].str[:5] != "85.42") & (df["skolekom"] != "2580") & (df["nus2000"].str[0].isin(["6", "7", "8"]))),
        # Folkehøgskoler
        "510": ((df["naering"] == "85.591") & (df["studretn"].isna())),
        # Arbeidsmarkedskurs
        "520": (df["naering"] == "85.592"),
        # Fagskoler
        "710": ((df["studretn"] == "50") | (df["fagskoleutd"] == "10")),
        # Høyere utdanning i utlandet
        "620": ((df["skolekom"] == "2580") & (df["nus2000"].str[0] > "5")),
        # Statlige høgskoler
        "311": ((df["naering"] == "85.423") & (df["studretn"].isna()) & (df["nus2000"].str[0] > "4")),
        # Militære høgskoler
        "312": (df["naering"] == "85.424"),
        # Andre høgskoler
        "313": ((df["naering"] == "85.429") & (df["studretn"].isna()) & (df["nus2000"].str[0] > "4")),
        # Universiteter
        "401": ((df["naering"] == "85.421") & (df["nus2000"].str[0] > "4")),
        # Vitenskapelige høgskoler
        "402": ((df["naering"] == "85.422") & (df["nus2000"].str[0] > "4")),
        # Lærlinger i vgo i Norge
        "212": ((df["kilde"].isin(["21", "30", "31", "51"])) & (df["komp"].isin(["2", "5"])) & (df["skolekom"] != "2580")),
        # Annen videregående utdanning - kilde 23
        "220": (df["kilde"] == "23"),        
        # Elever i vgo i Norge
        "211": (((df["studretn"].notna() & (df["kilde"] != "31")) | (df["studretn"].notna() & (df["kilde"] == "31") & (df["skolekom"] != "2580")))),
        # Videregående utdanning i utlandet
        "610": ((df["skolekom"] == "2580") & (df["nus2000"].str[0] < "6")),
    }
    for key, cond in conditions.items():
        df.loc[cond, col_name] = key
    df[col_name] = df[col_name].fillna(default)
    return df