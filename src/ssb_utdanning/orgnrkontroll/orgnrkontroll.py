import os

import pandas as pd

from ssb_utdanning import logger
from ssb_utdanning.config import PROD_SKOLEREG_PATH
from ssb_utdanning.config import PROD_VIGO_PATH

# # Notes
#
# * Må bestemme hvordan vi skal håndtere 'skolereg' og 'vigo'
#     * Versjonering, filtype og path
# if __name__ == "__main__":
#    innfil_path = "/ssb/stamme01/utd/utd-vg-vgu/data-produkt/vigo-elev/"
#    innfil_filename = "vigo_elev_g2023_nus_v1.sas7bdat"
#    data = saspy_df_from_path(innfil_path + innfil_filename)


def get_skolereg(aar: str | int = "latest") -> pd.DataFrame:
    """Get skolereg by year from prodsone path, with option to get the latest version as default."""
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
        skolereg_filename = [file for file in skolereg_files if file[1:5] == str(aar)]
        assert len(skolereg_filename) == 1
        skolereg_filename = skolereg_filename[0]
        logger.info("Henter skoleregfil %s", skolereg_filename)

    skolereg_filename = "testskolereg_" + skolereg_filename
    skolereg = pd.read_parquet(PROD_SKOLEREG_PATH + skolereg_filename)
    return skolereg


def get_vigo_skole(aar: str | int = "latest") -> pd.DataFrame:
    """Get vigo skole-file by year from prodsone path, with option to get the latest version as default."""
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
        vigo_filename = [file for file in vigo_files if file[1:5] == str(aar)]
        assert len(vigo_filename) == 1
        vigo_filename = vigo_filename[0]
        logger.info("Henter vigo skolefil %s", vigo_filename)

    vigo_filename = "testvigoskole_" + vigo_filename
    vigo = pd.read_parquet(PROD_VIGO_PATH + vigo_filename)
    return vigo


def evaluate_skolereg_merge(
    innfil: pd.DataFrame,
    skolereg: pd.DataFrame,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Find how many will merge on the two 'orgnr' variables."""
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
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Evaluate the potential merge between vigo skole for the rows that did not match against skolereg."""
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
    """Merge skolereg on orgnr and orgnrbed, returning a concated dataframe of both merges."""
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


def merge_vigo(
    kobler_fskolenr: pd.DataFrame,
    fskolenr_innfil: str = "fskolenr",
    vigo_keep_cols: set[str] | str = "all",
    vigo: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Merge vigo skole-file onto the file resulting from the earlier run merge from skolereg."""
    # optional import of vigo
    if not isinstance(vigo, pd.DataFrame):
        vigo = get_vigo_skole()

    keep_cols_default = "SKOLENR"
    if vigo_keep_cols == "all":
        vigo_keep_cols = set(vigo.columns)
    vigo_keep_cols.add(keep_cols_default)

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
    vigo_keep_cols: str | list[str] = "all",
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    fskolenr_innfil: str = "fskolenr",
    aar: str | int = "latest",
    concat_return: bool = False,
) -> pd.DataFrame | tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Combines functions in the common pipeline for upper-secondary schools (VGU)."""
    if skolereg_keep_cols is None:
        skolereg_keep_cols = ["orgnr", "orgnrbed"]
    if len(str(aar)) != 4:
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

    merged_w_vigo = merge_vigo(kobler_fskolenr, fskolenr_innfil, vigo_keep_cols, vigo)

    if concat_return:
        logger.info(
            "Returnerer sammenslått objekt med alle rader fra innfilen som kobler på de ulike filene, og de som ikke kobler."
        )
        return pd.concat([merged_w_skolereg, merged_w_vigo, kobler_ikke_fskolenr])
    logger.info(
        "Returnerer 3 objekter: de som merger med skolereg, de som merger med vigo, de som ikke merger."
    )
    return merged_w_skolereg, merged_w_vigo, kobler_ikke_fskolenr


# if __name__ == "__main__":
#    merged_w_skolereg, merged_w_vigo, kobler_ikke_fskolenr = orgnrkontroll(
#        data,
#        orgnr_col_innfil="orgnr_inn",
#        orgnrbed_col_innfil="forgnr",
#        skolereg_keep_cols=["nace1_sn07"],
#        aar=2023,
#    )
#    assert len(merged_w_skolereg) + len(merged_w_vigo) + len(
#        kobler_ikke_fskolenr
#    ) == len(data)
