import os
from datetime import datetime

import pandas as pd
from saspy_session import saspy_df_from_path

# # Notes
#
# - Hvordan burde vi håndtere næring?
# - Hvordan håndtere orgnr i koblingen?

if __name__ == "__main__":
    innfil_path = "/ssb/stamme01/utd/utd-vg-vgu/data-produkt/vigo-elev/"
    innfil_filename = "vigo_elev_g2023_nus_v1.sas7bdat"
    data = saspy_df_from_path(innfil_path + innfil_filename)


def get_skolereg(skolereg_aar: str | int = "latest") -> pd.DataFrame:
    skolereg_path = "/ssb/stamme01/utd/kat/skolereg/"
    # this block needs to be updated if we choose to convert skolereg to parquet
    files = os.listdir(skolereg_path)
    skolereg_files = [files[i] for i in range(len(files)) if len(files[i]) == 16]
    skolereg_files.sort(reverse=True)
    if skolereg_aar == "latest":
        skolereg_filename = skolereg_files[0]
        print(f"Henter nyeste skoleregfil '{skolereg_filename}'\n")
    else:
        assert (
            len(str(skolereg_aar)) == 4
        ), "året du oppga for skoleregfila er på feil format. vi ønsker YYYY."  # assert year format
        skolereg_filename = [
            file for file in skolereg_files if file[1:5] == str(skolereg_aar)
        ]
        assert len(skolereg_filename) == 1
        skolereg_filename = skolereg_filename[0]
        print(f"Henter skoleregfil '{skolereg_filename}'\n")

    # temporary setting of the 'skolereg' filename
    skolereg_filename = "testskolereg_g202310.parquet"
    # skolereg = saspy_df_from_path(skolereg_path + skolereg_filename)
    skolereg = pd.read_parquet(skolereg_path + skolereg_filename)
    return skolereg


def get_omk_kat(omk_kat_aar: str | int = "latest") -> pd.DataFrame:
    # should this import function include some quality checks on the secondary catalogue?

    omk_path = "/ssb/stamme01/utd/vgselev/kat/elev/omkodkat/"
    # omk_filename = 'testomkkat.parquet'
    omk_files = os.listdir(omk_path)
    omk_files = [
        file for file in omk_files if file.split("_")[0] == "testomkkat"
    ]  # this needs to be updated for use outside test-scope
    omk_files.sort(reverse=True)

    if omk_kat_aar == "latest":
        omk_filename = omk_files[0]
        print(f"Henter nyeste sekundærkatalog for omkoding '{omk_filename}'\n")
    else:
        omk_filename = [
            file for file in omk_files if file.split("_")[1][:4] == str(omk_kat_aar)
        ]
        omk_filename = omk_filename[
            0
        ]  # retrieving the newest secondary catalogue from the year asked for
        print(f"Henter sekundærkatalog for omkoding '{omk_filename}'\n")
    omk_kat = pd.read_parquet(omk_path + omk_filename)
    return omk_kat


def evaluate_skolereg_merge(
    innfil: pd.DataFrame,
    skolereg: pd.DataFrame,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # finding how many will merge on the two 'orgnr' variables
    kobler_orgnr = innfil.loc[innfil[orgnr_col_innfil].isin(skolereg["orgnr"])]
    print(
        f"{len(kobler_orgnr)}/{len(innfil)} koblet mot skolereg på '{orgnr_col_innfil}'"
    )

    koblet_ikke_orgnr = innfil.loc[~innfil[orgnr_col_innfil].isin(skolereg["orgnr"])]

    kobler_orgnrbed = koblet_ikke_orgnr.loc[
        koblet_ikke_orgnr[orgnrbed_col_innfil].isin(skolereg["orgnrbed"])
    ]
    print(
        f"Av de som ikke koblet på '{orgnr_col_innfil}' var det {len(kobler_orgnrbed)}/{len(koblet_ikke_orgnr)} som koblet på '{orgnrbed_col_innfil}'"
    )

    koblet_ikke = koblet_ikke_orgnr.loc[
        ~koblet_ikke_orgnr[orgnrbed_col_innfil].isin(skolereg["orgnrbed"])
    ]
    print(
        f"Totalt var det {len(koblet_ikke)}/{len(innfil)} som ikke koblet på hverken '{orgnr_col_innfil}' eller '{orgnrbed_col_innfil}' \n"
    )

    return kobler_orgnr, kobler_orgnrbed, koblet_ikke


def evaluate_omk_kat_merge(
    koblet_ikke: pd.DataFrame,
    omk_kat: pd.DataFrame,
    skolereg: pd.DataFrame,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not isinstance(omk_kat, pd.DataFrame):
        omk_kat = get_omk_kat()
    koblet_omk = koblet_ikke.loc[koblet_ikke["fskolenr"].isin(omk_kat["fskolenr"])]
    print(
        f"Med utgangspunkt i de {len(koblet_ikke)} som ikke koblet, sjekker vi kobling mot sekundærkatalog på nøkkel 'fskolenr'"
    )
    print(
        f"Finner {len(koblet_omk)}/{len(koblet_ikke)} på 'fskolenr' i omkodingskatalogen"
    )

    koblet_ikke_omk = koblet_ikke.loc[
        ~koblet_ikke["fskolenr"].isin(omk_kat["fskolenr"])
    ]
    # isolating the information in the secondary catalogue relevant for the people not found in the 'skolereg' so far
    omk_kat_eval = omk_kat.loc[
        omk_kat["fskolenr"].isin(koblet_omk["fskolenr"].unique())
    ]

    # trying to see if the 'orgnr' in the secondary catalogue exists in 'skolereg'
    print(
        f"De {len(koblet_omk)} som kobler mot sekundærkatalog er representert av {len(omk_kat_eval)} 'fskolenr'"
    )
    omk_orgnr_skolereg = omk_kat_eval.loc[
        omk_kat_eval["orgnr_omk"].isin(skolereg["orgnr"])
    ]
    omk_orgnrbed_skolereg = omk_kat_eval.loc[
        omk_kat_eval["orgnrbed_omk"].isin(skolereg["orgnrbed"])
    ]
    print(
        f"Av disse {len(omk_kat_eval)} får vi {len(omk_orgnr_skolereg)} treff mot skolereg på 'orgnr' og {len(omk_orgnrbed_skolereg)} treff mot 'orgnrbed' \n"
    )

    # finding those who can merge with 'skolereg' after updating their 'orgnr' from the secondary catalogue
    kobl_omk_skolereg_orgnr = koblet_omk.loc[
        koblet_omk["fskolenr"].isin(omk_orgnr_skolereg["fskolenr"])
    ]
    kobl_omk_skolereg_orgnrbed = koblet_omk.loc[
        koblet_omk["fskolenr"].isin(omk_orgnrbed_skolereg["fskolenr"])
    ]

    # finding those who were found in the secondary catalogue, but did not
    kobl_omk_not_skolereg = koblet_omk.loc[
        (
            ~koblet_omk["fskolenr"].isin(omk_orgnr_skolereg["fskolenr"])
            & (~koblet_omk["fskolenr"].isin(omk_orgnrbed_skolereg["fskolenr"]))
        )
    ]

    # verifying that all are accounted for
    assert len(kobl_omk_not_skolereg) + len(kobl_omk_skolereg_orgnr) + len(
        kobl_omk_skolereg_orgnrbed
    ) + len(koblet_ikke_omk) == len(koblet_ikke)
    return (
        kobl_omk_not_skolereg,
        kobl_omk_skolereg_orgnr,
        kobl_omk_skolereg_orgnrbed,
        koblet_ikke_omk,
    )


def merge_skolereg(
    innfil: pd.DataFrame,
    skolereg_keep_cols: list[str] = ["orgnr", "orgnrbed"],
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    kobler_orgnr: pd.DataFrame | None = None,
    kobler_orgnrbed: pd.DataFrame | None = None,
    skolereg: pd.DataFrame | None = None,
    skolereg_aar: str | int = "latest",
    include_kobler_ikke: bool = False,
) -> pd.DataFrame:
    # optional import of skolereg
    if not isinstance(skolereg, pd.DataFrame):
        skolereg = get_skolereg(skolereg_aar)

    # optional separation of what merges on different 'orgnr' column
    if not isinstance(kobler_orgnr, pd.DataFrame) or not isinstance(
        kobler_orgnrbed, pd.DataFrame
    ):
        kobler_orgnr, kobler_orgnrbed, koblet_ikke = evaluate_skolereg_merge(
            innfil, skolereg, orgnr_col_innfil, orgnrbed_col_innfil
        )
    # performing the merge
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
    if include_kobler_ikke:
        return pd.concat([merged_orgnr, merged_orgnrbed, koblet_ikke])
    return pd.concat([merged_orgnr, merged_orgnrbed])


def merge_omk(
    koblet_ikke: pd.DataFrame,
    skolereg_keep_cols: list[str] = "",
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    kobl_omk_not_skolereg: pd.DataFrame | None = None,
    kobl_omk_skolereg_orgnr: pd.DataFrame | None = None,
    kobl_omk_skolereg_orgnrbed: pd.DataFrame | None = None,
    skolereg: pd.DataFrame | None = None,
    omk_kat: pd.DataFrame | None = None,
    skolereg_aar: str | int = "latest",
    include_kobler_ikke: bool = False,
) -> pd.DataFrame:
    assert "fskolenr" in list(
        koblet_ikke.columns
    ), "fskolenr ligger ikke som kolonne på DataFramen som skal kobles mot sekundærkatalogen"

    # making sure 'orgnr'-variables are added to the list of variables to be merged from skolereg
    orgnr_cols = ["orgnr", "orgnrbed"]
    if skolereg_keep_cols == "":
        skolereg_keep_cols = orgnr_cols
    elif isinstance(skolereg_keep_cols, str) and skolereg_keep_cols not in orgnr_cols:
        skolereg_keep_cols = orgnr_cols + [skolereg_keep_cols]
    elif isinstance(skolereg_keep_cols, list):
        if orgnr_cols[1] not in skolereg_keep_cols:
            skolereg_keep_cols = orgnr_cols[1] + skolereg_keep_cols
        if orgnr_cols[0] not in skolereg_keep_cols:
            skolereg_keep_cols = orgnr_cols[0] + skolereg_keep_cols

        # optional import of skolereg
    if not isinstance(skolereg, pd.DataFrame):
        skolereg = get_skolereg(skolereg_aar)
    # optional import of secondary catalogue
    if not isinstance(omk_kat, pd.DataFrame):
        omk_kat = get_omk_kat(skolereg_aar)

    # optional separation of what merges on different 'orgnr' column
    if (
        not isinstance(kobl_omk_not_skolereg, pd.DataFrame)
        or not isinstance(kobl_omk_skolereg_orgnr, pd.DataFrame)
        or not isinstance(kobl_omk_skolereg_orgnrbed, pd.DataFrame)
    ):
        (
            kobl_omk_not_skolereg,
            kobl_omk_skolereg_orgnr,
            kobl_omk_skolereg_orgnrbed,
            koblet_ikke_omk,
        ) = evaluate_omk_kat_merge(
            koblet_ikke, omk_kat, skolereg, orgnr_col_innfil, orgnrbed_col_innfil
        )
    # merging orgnr fro secondary catalogue to use as merge key for merge with skolereg
    kobl_omk_skolereg_orgnr = kobl_omk_skolereg_orgnr.merge(
        omk_kat[["fskolenr", "orgnr_omk"]], how="left", on="fskolenr"
    )
    kobl_omk_skolereg_orgnrbed = kobl_omk_skolereg_orgnrbed.merge(
        omk_kat[["fskolenr", "orgnrbed_omk"]], how="left", on="fskolenr"
    )

    # merging with those found in skolereg
    merged_omk_skolereg_orgnr = kobl_omk_skolereg_orgnr.merge(
        skolereg[skolereg_keep_cols], how="left", left_on="orgnr_omk", right_on="orgnr"
    )
    merged_omk_skolereg_orgnrbed = kobl_omk_skolereg_orgnrbed.merge(
        skolereg[skolereg_keep_cols],
        how="left",
        left_on="orgnrbed_omk",
        right_on="orgnrbed",
    )

    # merging with secondary catalogue for those who didn't merge with skolereg
    merged_omk_not_skolereg = kobl_omk_not_skolereg.merge(
        omk_kat, how="left", on="fskolenr"
    )
    if include_kobler_ikke:
        return pd.concat(
            [
                merged_omk_skolereg_orgnr,
                merged_omk_skolereg_orgnrbed,
                merged_omk_not_skolereg,
                koblet_ikke_omk,
            ]
        )
    return pd.concat(
        [
            merged_omk_skolereg_orgnr,
            merged_omk_skolereg_orgnrbed,
            merged_omk_not_skolereg,
        ]
    )


def iterate_edit(to_omk_nodup: pd.DataFrame, skolereg: pd.DataFrame) -> pd.DataFrame:
    print(
        f"Nå vil vi iterete over de {len(to_omk_nodup)} skolene som ikke ble funnet i skoleregisteret. Finn riktig orgnr og fyll inn."
    )
    orgnr_list = []
    varlist = list(to_omk_nodup.columns)
    yeslist = ["y", "ye", "yes"]
    for i, row in to_omk_nodup.iterrows():
        in_skolereg = "No"
        display(pd.DataFrame(row).T)
        orgnr_omk = input("Hva er riktig orgnr for denne skolen?")
        if (
            orgnr_omk not in skolereg["orgnr"].to_list()
            and orgnr_omk not in skolereg["orgnrbed"].to_list()
        ):
            print(
                "Orgnummeret du oppga ble ikke funnet i skoleregisteret og editeringen vil derfor ikke lagres i sekundærkatalogen."
            )
            again = input("Vil ha muligheten til å oppgi orgnr på nytt? y/n: ")
            if again.lower() not in yeslist:
                in_skolereg = "y"
        else:
            in_skolereg = "y"
        # loop that allows to perform iterative check against skolereg
        while in_skolereg.lower() not in yeslist:
            display(pd.DataFrame(row).T)
            orgnr_omk = input(
                "Skriv inn riktig orgnr for skolen, for stopp, skriv 'stopp': "
            )
            if orgnr_omk.lower() == "stopp":
                print("\n Da går vi videre")
                in_skolereg = "y"
            if (
                orgnr_omk in skolereg["orgnr"].to_list()
                or orgnr_omk in skolereg["orgnrbed"].to_list()
            ):
                in_skolereg = "y"
                print("Dette orgnr ble funnet i skolereg. Vi går videre")
        orgnr_list.append(orgnr_omk)
    from_omk_nodup = to_omk_nodup.copy()
    assert len(from_omk_nodup) == len(orgnr_list)
    from_omk_nodup["orgnr_omk"] = orgnr_list

    # display(from_omk_nodup)
    return from_omk_nodup


def write_omk_kat(to_write: pd.DataFrame):
    path = "/ssb/stamme01/utd/vgselev/kat/elev/omkodkat/"
    files = os.listdir(path)
    # denne må endres
    omk_files = [file for file in files if file.split("_")[0] == "testomkkat"]
    dates = [file.split("_")[1].split(".")[0] for file in omk_files]
    # print(dates)
    date_to_file = dict(zip(dates, omk_files))
    dates.sort(reverse=True)
    newest = date_to_file[dates[0]]
    omk_kat = pd.read_parquet(path + newest)
    # display(omk_kat)
    # display(to_write)
    if omk_kat.equals(to_write):
        print(
            "Sekundærkatalogen du forsøker å skrive til fil er identisk med nyeste versjon på disk. Skriver ikke duplikat"
        )
    else:
        # sorterer på dato og gjør duplikatsjekk
        to_write.sort_values("dato", ascending=True, inplace=True)
        to_write.drop_duplicates(subset="fskolenr", keep="first", inplace=True)
        display(to_write)
        now = datetime.now().isoformat("T", "seconds").replace(":", "-")
        filename_out = f"testomkkat_{now}.parquet"
        print("Writing to file")
        to_write.to_parquet(path + filename_out)


def manual_omk(
    to_manuel_omk: pd.DataFrame,
    skolereg: pd.DataFrame,
    omk_kat: pd.DataFrame,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
) -> pd.DataFrame:
    skolenavn = "snavn"
    if skolenavn not in to_manuel_omk.columns:
        skolenavn = input(
            "Hva heter kolonnen som inneholder skolenavn (feks. 'snavn') på datafilen? "
        )
    skolenr = "fskolenr"
    if skolenr not in to_manuel_omk.columns:
        skolenr = input(
            "Hva heter kolonnen som inneholder skolenr (feks. 'fskolenr') på datafilen? "
        )
    cols_to_omk = [orgnr_col_innfil, orgnrbed_col_innfil, skolenavn, skolenr]

    to_omk = to_manuel_omk[cols_to_omk].copy()
    to_omk_nodup = to_omk.drop_duplicates(
        subset=[orgnr_col_innfil, orgnrbed_col_innfil, skolenr]
    )

    from_omk_nodup = iterate_edit(to_omk_nodup, skolereg)
    mask_kobler = (from_omk_nodup["orgnr_omk"].isin(skolereg["orgnr"])) | (
        from_omk_nodup["orgnr_omk"].isin(skolereg["orgnrbed"])
    )
    to_write = from_omk_nodup.loc[mask_kobler]
    # to_write.drop(columns=[orgnr_col_innfil, orgnrbed_col_innfil], inplace=True)

    rename_dict = {skolenavn: "fskolenavn", skolenr: "fskolenr"}
    to_write = to_write.rename(columns=rename_dict).copy()
    to_write = to_write[["fskolenr", "fskolenavn", "orgnr_omk"]].copy()
    # display(pd.concat([omk_kat, to_write]))
    if len(to_write) > 0:
        now = datetime.now().isoformat("T", "seconds")
        to_write["dato"] = now
        now = now.replace(":", "-")
        final_write = pd.concat([omk_kat, to_write])
        print(
            f"Totalt {len(to_write)}/{len(to_omk_nodup)} fikk oppdatert orgnr med ett som kobler mot skolereg. \n \
        disse skrives til fil"
        )
        write_omk_kat(final_write)
    else:
        print("Ingen orgnr ble oppdatert, og sekundærkatalogen vil ikke bli oppdatert")


# legge inn default lsite for skolereg_keep_cols
def orgnrkontroll(
    innfil: pd.DataFrame,
    skolereg_keep_cols: str | list[str] = "",
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    skolereg_aar: str | int = "latest",
    omk_kat_aar: str | int = "latest",
) -> pd.DataFrame:
    # making sure 'orgnr'-variables are added to the list of variables to be merged from skolereg
    orgnr_cols = ["orgnr", "orgnrbed"]
    if skolereg_keep_cols == "":
        skolereg_keep_cols = orgnr_cols
    elif isinstance(skolereg_keep_cols, str) and skolereg_keep_cols not in orgnr_cols:
        skolereg_keep_cols = orgnr_cols + [skolereg_keep_cols]
    elif isinstance(skolereg_keep_cols, list):
        if orgnr_cols[1] not in skolereg_keep_cols:
            skolereg_keep_cols = orgnr_cols[1] + skolereg_keep_cols
        if orgnr_cols[0] not in skolereg_keep_cols:
            skolereg_keep_cols = orgnr_cols[0] + skolereg_keep_cols

    skolereg = get_skolereg(skolereg_aar)
    omk_kat = get_omk_kat(omk_kat_aar)
    # display(omk_kat)
    kobler_orgnr, kobler_orgnrbed, koblet_ikke = evaluate_skolereg_merge(
        innfil, skolereg, orgnr_col_innfil, orgnrbed_col_innfil
    )

    (
        kobl_omk_not_skolereg,
        kobl_omk_skolereg_orgnr,
        kobl_omk_skolereg_orgnrbed,
        koblet_ikke_omk,
    ) = evaluate_omk_kat_merge(koblet_ikke, omk_kat, skolereg)

    merged_w_skolereg = merge_skolereg(
        innfil,
        skolereg_keep_cols,
        orgnr_col_innfil,
        orgnrbed_col_innfil,
        kobler_orgnr,
        kobler_orgnrbed,
        skolereg,
    )
    to_manuel_omk = pd.concat([kobl_omk_not_skolereg, koblet_ikke_omk])
    manual_omk(to_manuel_omk, skolereg, omk_kat, orgnr_col_innfil, orgnrbed_col_innfil)

    # evaluerer kobling mot skolereg gjennom omk_kat på nytt
    print(
        "Evaluerer kobling mot skolereg gjennom sekundærkatalogen på nytt etter manuel koding av orgnr"
    )
    omk_kat = get_omk_kat("latest")
    (
        kobl_omk_not_skolereg,
        kobl_omk_skolereg_orgnr,
        kobl_omk_skolereg_orgnrbed,
        koblet_ikke_omk,
    ) = evaluate_omk_kat_merge(koblet_ikke, omk_kat, skolereg)
    merged_w_omk = merge_omk(
        koblet_ikke,
        skolereg_keep_cols,
        orgnr_col_innfil,
        orgnrbed_col_innfil,
        kobl_omk_not_skolereg,
        kobl_omk_skolereg_orgnr,
        kobl_omk_skolereg_orgnrbed,
        skolereg,
        omk_kat,
        skolereg_aar,
    )

    return pd.concat([merged_w_skolereg, merged_w_omk, koblet_ikke_omk])


if __name__ == "__main__":
    # print(get_omk_kat())
    merged = orgnrkontroll(
        data,
        orgnr_col_innfil="orgnr_inn",
        orgnrbed_col_innfil="forgnr",
        skolereg_keep_cols="nace1_sn07",
    )

skolereg = get_skolereg()


omk_kat = get_omk_kat("latest")
omk_kat

orgnr_omk in skolereg["orgnr"].to_list()

orgnr_omk = "test1"
if (
    orgnr_omk not in skolereg["orgnr"].to_list()
    and orgnr_omk not in skolereg["orgnrbed"].to_list()
):
    print("here")

skolereg = get_omk_kat()
skolereg

data.columns

data.loc[data["fskolenr"] == "24499", "alder"].value_counts(dropna=False)
