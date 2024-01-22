"""
NB! TESTED ON IGANG_2022_MINIREG. IT APPEARS TO PROVIDE THE CORRECT BEHAVIOUR. KEEP IN MIND THAT THE ORDER OF THE CONDITIONS IS CRUCIAL. FURTHER TESTING ADVICED.
"""

import pandas as pd

def grupper_ktrinn(df: pd.DataFrame, col_name: str = "ktrinn", rename_cols: dict = None, default: pd._libs.missing.NAType = pd.NA) -> pd.DataFrame:
    """
    Groups educational levels based on specified conditions.

    Arg(s):
        df (pd.DataFrame): Input DataFrame containing education data.
        col_name (str, optional): Name of the column to store the grouped educational levels. Defaults to "ktrinn".
        rename_cols (dict, optional): Dictionary to rename columns. Defaults to None.
        default (pd._libs.missing.NAType, optional): Default value for missing or ungrouped entries. Defaults to pd.NA.

    Return(s):
        pd.DataFrame: DataFrame with added column containing grouped educational levels.
    """
    df = df.copy()
    
    req_cols = ["kurstrin", "kltrinn", "fagskoleutd"]
    if rename_cols is not None:
        df = df.rename(columns=rename_cols)
        
    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}.")
    
    conditions = {
        "1": (df["kurstrin"].isin(["A", "B", "C", "K", "R", "D"]) & (df["kltrinn"] == "11")),
        "2": (df["kurstrin"].isin(["H", "J", "K", "R", "I", "D"]) & (df["kltrinn"] == "12")),
        "3": (df["kurstrin"].isin(["P", "Q", "K", "R", "I", "D"]) & (df["kltrinn"] == "13")),
        "5": (df["fagskoleutd"] == "10") | ((df["kurstrin"] == "U") & (df["kltrinn"].isin(["14", "15"]))),
        "4": (df["kurstrin"].notna())
    }
    reversed_conditions = {k: conditions[k] for k in reversed(list(conditions.keys()))}
    for key, cond in reversed_conditions.items():
        df.loc[cond, col_name] = key
    df[col_name] = df[col_name].fillna(default)
    return df

def grupper_skobo(df: pd.DataFrame, col_name: str = "skobo", rename_cols: dict = None, default: pd._libs.missing.NAType = pd.NA) -> pd.DataFrame:
    """
    Groups school boards based on specified conditions.

    Arg(s):
        df (pd.DataFrame): Input DataFrame containing school board data.
        col_name (str, optional): Name of the column to store the grouped school board categories. Defaults to "skobo".
        rename_cols (dict, optional): Dictionary to rename columns. Defaults to None.
        default (pd._libs.missing.NAType, optional): Default value for missing or ungrouped entries. Defaults to pd.NA.

    Return(s):
        pd.DataFrame: DataFrame with added column containing grouped school board categories.
    """
    df = df.copy()
    
    req_cols = ["kommnr", "skolekom"]
    if rename_cols is not None:
        df = df.rename(columns=rename_cols)
    
    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}.")
    
    conditions = {
        "1": (df["kommnr"] == df["skolekom"]),
        "2": (df["kommnr"].str[:2] == df["skolekom"].str[:2]),
        "3": (df["kommnr"].str[:2] != df["skolekom"].str[:2])
    }
    reversed_conditions = {k: conditions[k] for k in reversed(list(conditions.keys()))}
    for key, cond in reversed_conditions.items():
        df.loc[cond, col_name] = key
    df[col_name] = df[col_name].fillna(default)
    return df

def grupper_utd(df: pd.DataFrame, col_name: str = "utd", rename_cols: dict = None, default: pd._libs.missing.NAType = pd.NA) -> pd.DataFrame:
    """
    Groups education data based on specified conditions.

    Arg(s):
        df (pd.DataFrame): Input DataFrame containing education data.
        col_name (str, optional): Name of the column to store the grouped education categories. Defaults to "utd".
        default (pd._libs.missing.NAType, optional): Default value for missing or ungrouped entries. Defaults to pd.NA.
        rename_cols (dict, optional): Dictionary to rename columns. Defaults to None.

    Return(s):
        pd.DataFrame: DataFrame with added column containing grouped education categories.
    """
    df = df.copy()
    
    req_cols = ["kilde", "sn07", "nus2000", "skolekom", "studretn", "fagskoleutd", "komp"]
    if rename_cols is not None:
        df = df.rename(columns=rename_cols)

    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}.")
    
    # Explanations.
    utland_komm = "2580"
    gsk_nacer = ("85.100", "85.201", "85.202", "85.203")
    avsl_gsk_kilde = "10"
        
    conditions = {
        # Grunnskoler
        "100": ((df["kilde"] == avsl_gsk_kilde) | ((df["sn07"].isin(gsk_nacer)) & (df["nus2000"].str[0].isin(["0", "1", "2"])))),
        # Annen universitets- og høgskoleutdanning
        "320": ((df["sn07"].str[:5] != "85.42") & (df["skolekom"] != utland_komm) & (df["nus2000"].str[0].isin(["6", "7", "8"]))),
        # Folkehøgskoler
        "510": ((df["sn07"] == "85.591") & (df["studretn"].isna())),
        # Arbeidsmarkedskurs
        "520": (df["sn07"] == "85.592"),
        # Fagskoler
        "710": ((df["studretn"] == "50") | (df["fagskoleutd"] == avsl_gsk_kilde)),
        # Høyere utdanning i utlandet
        "620": ((df["skolekom"] == utland_komm) & (df["nus2000"].str[0] > "5")),
        # Statlige høgskoler
        "311": ((df["sn07"] == "85.423") & (df["studretn"].isna()) & (df["nus2000"].str[0] > "4")),
        # Militære høgskoler
        "312": (df["sn07"] == "85.424"),
        # Andre høgskoler
        "313": ((df["sn07"] == "85.429") & (df["studretn"].isna()) & (df["nus2000"].str[0] > "4")),
        # Universiteter
        "401": ((df["sn07"] == "85.421") & (df["nus2000"].str[0] > "4")),
        # Vitenskapelige høgskoler
        "402": ((df["sn07"] == "85.422") & (df["nus2000"].str[0] > "4")),
        # Lærlinger i vgo i Norge
        "212": ((df["kilde"].isin(["21", "30", "31", "51"])) & (df["komp"].isin(["2", "5"])) & (df["skolekom"] != utland_komm)),
        # Annen videregående utdanning - kilde 23
        "220": (df["kilde"] == "23"),        
        # Elever i vgo i Norge
        "211": (((df["studretn"].notna() & (df["kilde"] != "31")) | (df["studretn"].notna() & (df["kilde"] == "31") & (df["skolekom"] != utland_komm)))),
        # Videregående utdanning i utlandet
        "610": ((df["skolekom"] == utland_komm) & (df["nus2000"].str[0] < "6")),
    }
    reversed_conditions = {k: conditions[k] for k in reversed(list(conditions.keys()))}
    for key, cond in reversed_conditions.items():
        df.loc[cond, col_name] = key
    df[col_name] = df[col_name].fillna(default)
    return df