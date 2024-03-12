import os

import pandas as pd

from ssb_utdanning import UtdKatalog
from ssb_utdanning import logger
from ssb_utdanning.config import PROD_SKOLEREG_PATH
from ssb_utdanning.config import PROD_VIGO_PATH


def get_skolereg(aar: str | int = "latest") -> pd.DataFrame:
    """Get skolereg by year from prodsone path, with option to get the latest version as default.

    Args:
        aar (str | int): The year you want to get the skolereg from.

    Returns:
        pd.DataFrame: The opened dataframe of the available skolereg.

    Raises:
        ValueError: If a single skolereg for opening, cant be determined.
    """
    # denne delen må kanskje  oppdateres når det er bestemt hvordan vi skal håndtere skolereg
    files = os.listdir(PROD_SKOLEREG_PATH)
    files = [
        file.split("_")[-1] for file in files if file.split("_")[0] == "testskolereg"
    ]

    skolereg_files = [
        file for file in files if file.endswith(".parquet") and file.startswith("g")
    ]

    skolereg_files.sort(reverse=True)
    if aar == "latest":
        skolereg_filename = skolereg_files[0]
        logger.info("Henter nyeste skoleregfil %s", skolereg_filename)
    else:
        skolereg_files_filtered = [
            file for file in skolereg_files if file[1:5] == str(aar)
        ]
        if len(skolereg_files_filtered) != 1:
            raise ValueError("Cant pick a single skolereg-file.")
        skolereg_filename = skolereg_files_filtered[0]
        logger.info("Henter skoleregfil %s", skolereg_filename)

    skolereg_filename = "testskolereg_" + skolereg_filename
    return UtdKatalog(PROD_SKOLEREG_PATH + skolereg_filename)


def get_vigo_skole(aar: str | int = "latest") -> pd.DataFrame:
    """Get vigo skole-file by year from prodsone path, with option to get the latest version as default.

    Args:
        aar (str | int): The year you want to get the vigo-skole file from.

    Returns:
        pd.DataFrame: The opened dataframe of the available vigo-skole-file.

    Raises:
        ValueError: If a single vigo-skole-file for opening, cant be determined.
    """
    # denne delen må oppdateres når det er bestemt hvordan vi skal håndtere vigo
    files = os.listdir(PROD_VIGO_PATH)
    files = [
        file.split("_")[-1] for file in files if file.split("_")[0] == "testvigoskole"
    ]
    vigo_files = [
        file for file in files if file.endswith(".parquet") and file.startswith("g")
    ]

    vigo_files.sort(reverse=True)
    if aar == "latest":
        vigo_filename = vigo_files[0]
        logger.info("Henter nyeste vigo skolefil %s", vigo_filename)
    else:
        vigo_files_filtered = [file for file in vigo_files if file[1:5] == str(aar)]
        if len(vigo_files_filtered) != 1:
            raise ValueError("Cant pick a single vigo-skole file.")
        vigo_filename = vigo_files_filtered[0]
        logger.info("Henter vigo skolefil %s", vigo_filename)

    vigo_filename = "testvigoskole_" + vigo_filename
    return pd.read_parquet(PROD_VIGO_PATH + vigo_filename)


def evaluate_skolereg_merge(
    innfil: pd.DataFrame,
    skolereg: pd.DataFrame,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Find how many will merge on the two 'orgnr' variables.

    Args:
        innfil (pd.DataFrame): The dataframe to evaluate.
        skolereg (pd.DataFrame): The dataframe to evaluate against.
        orgnr_col_innfil (str): The column name of the 'orgnr' variable in the innfil. Defaults to 'orgnr'.
        orgnrbed_col_innfil (str): The column name of the 'orgnrbed' variable in the innfil. Defaults to 'orgnrbed'.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Three dataframes, one for the orgnr-merge, one for the orgnrbed-merge, and one for the innfil-merge.
    """
    kobler_orgnr = innfil.loc[innfil[orgnr_col_innfil].isin(skolereg["orgnr"])]

    logger.info(
        "%s/%s rader fra innfila koblet mot skolereg med %s",
        str(len(kobler_orgnr)),
        str(len(innfil)),
        orgnr_col_innfil,
    )

    koblet_ikke_orgnr = innfil.loc[~innfil[orgnr_col_innfil].isin(skolereg["orgnr"])]

    kobler_orgnrbed = koblet_ikke_orgnr.loc[
        koblet_ikke_orgnr[orgnrbed_col_innfil].isin(skolereg["orgnrbed"])
    ]
    logger.info(
        "Av radene som ikke koblet på %s var det %s/%s rader som koblet på %s",
        orgnr_col_innfil,
        str(len(kobler_orgnrbed)),
        str(len(koblet_ikke_orgnr)),
        orgnrbed_col_innfil,
    )

    koblet_ikke = koblet_ikke_orgnr.loc[
        ~koblet_ikke_orgnr[orgnrbed_col_innfil].isin(skolereg["orgnrbed"])
    ]
    logger.info(
        "Totalt var det %s/%s rader fra innfila som ikke koblet på hverken %s eller %s",
        str(len(koblet_ikke)),
        str(len(innfil)),
        orgnr_col_innfil,
        orgnrbed_col_innfil,
    )
    return kobler_orgnr, kobler_orgnrbed, koblet_ikke


def evaluate_vigo_skole_merge(
    koblet_ikke_skolereg: pd.DataFrame,
    vigo: pd.DataFrame,
    fskolenr_innfil: str = "fskolenr",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Evaluate the potential merge between vigo skole for the rows that did not match against skolereg.

    Args:
        koblet_ikke_skolereg (pd.DataFrame): The dataframe to evaluate.
        vigo (pd.DataFrame): The dataframe to evaluate against.
        fskolenr_innfil (str): The column name of the 'fskolenr' variable in the innfil. Defaults to 'fskolenr'.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Two dataframes, one for the fskolenr-merge, and one for the ones who did not merge.
    """
    logger.info(
        "Evaluerer kobling mot vigo skoleverk for de %s radene på innfila som ikke koblet mot skolereg på orgnr/orgnrbed",
        str(len(koblet_ikke_skolereg)),
    )
    kobler_fskolenr = koblet_ikke_skolereg.loc[
        koblet_ikke_skolereg[fskolenr_innfil].isin(vigo["SKOLENR"])
    ]
    kobler_ikke_fskolenr = koblet_ikke_skolereg.loc[
        ~koblet_ikke_skolereg[fskolenr_innfil].isin(vigo["SKOLENR"])
    ]
    logger.info(
        "%s/%s koblet på 'fskolenr' mot vigo skoleverk.",
        str(len(kobler_fskolenr)),
        str(len(koblet_ikke_skolereg)),
    )
    return kobler_fskolenr, kobler_ikke_fskolenr


def merge_skolereg(
    kobler_orgnr: pd.DataFrame,
    kobler_orgnrbed: pd.DataFrame,
    skolereg_keep_cols: set[str] | None = None,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    skolereg: pd.DataFrame | None = None,
    aar: str | int = "latest",
) -> pd.DataFrame:
    """Merge skolereg on orgnr and orgnrbed, returning a concated dataframe of both merges.

    Args:
        kobler_orgnr (pd.DataFrame): The dataframe to merge on orgnr.
        kobler_orgnrbed (pd.DataFrame): The dataframe to merge on orgnrbed?
        skolereg_keep_cols (set[str] | None): The columns to keep from skolereg. Defaults to None.
        orgnr_col_innfil (str): The column name of the 'orgnr' variable in the innfil. Defaults to 'orgnr'.
        orgnrbed_col_innfil (str): The column name of the 'orgnrbed' variable in the innfil. Defaults to 'orgnrbed'.
        skolereg (pd.DataFrame | None): The dataframe to merge on. Defaults to None.
        aar (str | int): The year to use for the skolereg-file. Defaults to 'latest'.

    Returns:
        pd.DataFrame: The merged dataframe.
    """
    # optional import of skolereg
    if not isinstance(skolereg, pd.DataFrame):
        skolereg = get_skolereg(aar)

    keep_cols_default = {"orgnr", "orgnrbed"}
    if skolereg_keep_cols is None:
        skolereg_keep_cols = keep_cols_default
    # making sure 'orgnr'-variables are added to the list of variables to be merged from skolereg
    skolereg_keep_cols.update(keep_cols_default)

    # performing the merge
    logger.info(
        "Følgende variabler blir koblet på fra 'skolereg': %s", str(skolereg_keep_cols)
    )
    merged_orgnr = kobler_orgnr.merge(
        skolereg[skolereg_keep_cols],
        how="left",
        left_on=orgnr_col_innfil,
        right_on="orgnr",
    )
    merged_orgnrbed = kobler_orgnrbed.merge(
        skolereg[skolereg_keep_cols],
        how="left",
        left_on=orgnrbed_col_innfil,
        right_on="orgnrbed",
    )
    return pd.concat([merged_orgnr, merged_orgnrbed])


def merge_vigo_skole(
    kobler_fskolenr: pd.DataFrame,
    fskolenr_innfil: str = "fskolenr",
    vigo_keep_cols: set[str] | str = "all",
    vigo: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Merge vigo skole-file onto the file resulting from the earlier run merge from skolereg.

    Args:
        kobler_fskolenr (pd.DataFrame): The dataframe to merge on.
        fskolenr_innfil (str): The column name of the 'fskolenr' variable in the innfil. Defaults to 'fskolenr'.
        vigo_keep_cols (set[str] | str): The columns to keep from the vigo file. Defaults to 'all'.
        vigo (pd.DataFrame | None): The vigo file to merge on. Defaults to None.

    Returns:
        pd.DataFrame: The merged dataframe.

    Raises:
        TypeError: If vigo_keep_cols is not a set or a string.
    """
    # optional import of vigo
    if not isinstance(vigo, pd.DataFrame):
        vigo = get_vigo_skole()

    # Making sure vigo_keep_cols is a set of unique column names, including the default
    keep_cols_default = "SKOLENR"
    if vigo_keep_cols == "all":
        vigo_keep_cols_set = set(vigo.columns)
    elif isinstance(vigo_keep_cols, str):
        vigo_keep_cols_set = {vigo_keep_cols}
    else:
        vigo_keep_cols_set = vigo_keep_cols
    if not isinstance(vigo_keep_cols_set, set):
        raise TypeError(
            "vigo_keep_cols må være en set eller en str. Dette er ikke en set."
        )
    vigo_keep_cols_set.add(keep_cols_default)

    logger.info(
        "Følgende variabler blir koblet på fra 'skolereg': %s", str(vigo_keep_cols)
    )
    return kobler_fskolenr.merge(
        vigo, how="left", left_on=fskolenr_innfil, right_on=keep_cols_default
    )


# legge inn default lsite for skolereg_keep_cols, evt sett den til None, og sleng inn alle kolonnen?
def orgnrkontroll(
    innfil: pd.DataFrame,
    skolereg_keep_cols: set[str] | None = None,
    vigo_keep_cols: str | set[str] = "all",
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    fskolenr_innfil: str = "fskolenr",
    aar: str | int = "latest",
    concat_return: bool = False,
) -> pd.DataFrame | tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Combines functions in the common pipeline for upper-secondary schools (VGU) to add info on orgnr.

    Args:
        innfil (pd.DataFrame): The dataframe to merge on.
        skolereg_keep_cols (set[str] | None): The columns to keep from skolereg. Defaults to None.
        vigo_keep_cols (str | list[str]): The columns to keep from the vigo file. Defaults to 'all'.
        orgnr_col_innfil (str): The column name of the 'orgnr' variable in the innfil. Defaults to 'orgnr'.
        orgnrbed_col_innfil (str): The column name of the 'orgnrbed' variable in the innfil. Defaults to 'orgnrbed'.
        fskolenr_innfil (str): The column name of the 'fskolenr' variable in the innfil. Defaults to 'fskolenr'.
        aar (str | int): The year to use for the skolereg-file. Defaults to 'latest'.
        concat_return (bool): Whether to return a concatenated dataframe. Defaults to False.

    Returns:
        pd.DataFrame | tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: The merged dataframe, or a tuple of the merged dataframe, the merged dataframe from skolereg, and the merged dataframe from vigo.
    """
    if skolereg_keep_cols is None:
        skolereg_keep_cols = {"orgnr", "orgnrbed"}

    if aar == "latest":
        pass
    elif len(str(aar)) == 4 and str(aar).isdigit():
        pass
    else:
        aar = input("Formatet på aargangsvariabel er feil. Vi trenger YYYY:")

    skolereg = get_skolereg(aar)
    vigo = get_vigo_skole(aar)

    kobler_orgnr, kobler_orgnrbed, koblet_ikke = evaluate_skolereg_merge(
        innfil, skolereg, orgnr_col_innfil, orgnrbed_col_innfil
    )

    kobler_fskolenr, kobler_ikke_fskolenr = evaluate_vigo_skole_merge(koblet_ikke, vigo)

    merged_w_skolereg = merge_skolereg(
        kobler_orgnr,
        kobler_orgnrbed,
        skolereg_keep_cols,
        orgnr_col_innfil,
        orgnrbed_col_innfil,
        skolereg,
        aar,
    )

    merged_w_vigo = merge_vigo_skole(
        kobler_fskolenr, fskolenr_innfil, vigo_keep_cols, vigo
    )

    if concat_return:
        logger.info(
            "Returnerer sammenslått objekt med alle rader fra innfilen som kobler på de ulike filene, og de som ikke kobler."
        )
        return pd.concat([merged_w_skolereg, merged_w_vigo, kobler_ikke_fskolenr])
    logger.info(
        "Returnerer 3 objekter: de som merger med skolereg, de som merger med vigo, de som ikke merger."
    )
    return merged_w_skolereg, merged_w_vigo, kobler_ikke_fskolenr
