import os

import pandas as pd

from ssb_utdanning import UtdData
from ssb_utdanning import UtdKatalog
from ssb_utdanning import utdanning_logger
from ssb_utdanning.config import SKOLEREG_PATH
from ssb_utdanning.config import VIGO_PATH


def get_skolereg(year: str | int = "latest", sub_category: str = "") -> UtdKatalog:
    """Retrieves skolereg catalogue.

    Retrieves an `UtdKatalog` instance representing school registration data for a given year
    and sub-category. If no sub-category is specified, it excludes all predefined categories, i.e barnehage, vgskoler, grunnskoler, test.

    Args:
        year (str | int, optional): The year for which the data is to be retrieved. Can be
                                    an integer representing the year or 'latest' for the
                                    most recent data. Defaults to 'latest'.
        sub_category (str): A specific sub-category of school data to be retrieved.
                            Options include 'barnehage', 'vgskoler', 'test', 'grunnskoler'.
                            Defaults to an empty string, which means no specific sub-category.

    Returns:
        UtdKatalog: An instance of UtdKatalog configured with the appropriate file pattern,
                    key columns, and exclusions based on the inputs.

    Raises:
        ValueError: If the specified sub-category is not recognized.
    """
    possible_subcategories = ["barnehage", "vgskoler", "test", "grunnskoler", ""]
    if sub_category not in possible_subcategories:
        raise ValueError(
            f"sub-category {sub_category} not found in pre-defined sub-categories: {possible_subcategories}"
        )
    if not sub_category:
        exclude_keywords = possible_subcategories[:-1]
    else:
        exclude_keywords = [
            cat for cat in possible_subcategories if cat not in sub_category
        ]

    if year == "latest":
        return UtdKatalog(
            glob_pattern=os.path.join(
                SKOLEREG_PATH, f"skolereg_{sub_category}*.parquet"
            ),
            key_cols=["orgnr", "orgnrbed"],
            exclude_keywords=exclude_keywords,
        )
    return UtdKatalog(
        glob_pattern=os.path.join(
            SKOLEREG_PATH, f"skolereg_{sub_category}*{year}*.parquet"
        ),
        key_cols=["orgnr", "orgnrbed"],
        exclude_keywords=exclude_keywords,
    )


def get_vigo_skole(year: str | int = "latest") -> UtdKatalog:
    """Retrieves vigo-skole catalogue.

    Retrieves an `UtdKatalog` instance representing VIGO school data for a specified year.
    If no year is specified, it fetches data for the most recent year.

    Args:
        year (str | int, optional): The year for which the data is to be retrieved. Can be
                                    an integer representing the year or 'latest' for the
                                    most recent data. Defaults to 'latest'.

    Returns:
        UtdKatalog: An instance of UtdKatalog configured with the appropriate file pattern
                    and key columns for accessing VIGO school data.
    """
    if year == "latest":
        return UtdKatalog(
            glob_pattern=os.path.join(VIGO_PATH, "vigo_skole_testfil_slett*.parquet"),
            key_cols=["SKOLENR"],
        )
    return UtdKatalog(
        glob_pattern=os.path.join(
            VIGO_PATH, f"vigo_skole_testfil_slett*{year}*.parquet"
        ),
        key_cols=["SKOLENR"],
    )


def orgnrkontroll_func(
    data: pd.DataFrame | UtdData,
    year: str | int = "latest",
    skolereg_keep_cols: set[str] | list[str] | None = None,
    vigo_keep_cols: set[str] | list[str] | None = None,
    orgnr_col_innfil: str = "orgnr",
    orgnrbed_col_innfil: str = "orgnrbed",
    fskolenr_col_innfil: str = "fskolenr",
    skolereg_subcategory: str = "",
) -> pd.DataFrame | UtdData:
    """Performs merge validation and merges orgnr from skolereg and vigo-skole catalogues.

    Performs data validation and merging operations on educational data from different catalogs.
    Ensures the integrity of organizational number fields, merges additional data from school
    and VIGO catalogs, and handles missing data or discrepancies in organizational numbers.

    Args:
        data (pd.DataFrame | UtdData): The input dataset, either as a DataFrame or UtdData instance.
        year (str | int, optional): The year of the data to process. Defaults to 'latest'.
        skolereg_keep_cols (set[str] | list[str] | None, optional): Columns to keep from the skolereg data.
        vigo_keep_cols (set[str] | list[str] | None, optional): Columns to keep from the VIGO data.
        orgnr_col_innfil (str): Column name for organizational numbers in the input data. Defaults to "orgnr".
        orgnrbed_col_innfil (str): Column name for subsidiary organizational numbers in the input data. Defaults to "orgnrbed".
        fskolenr_col_innfil (str): Column name for school numbers in the input data. Defaults to "fskolenr".
        skolereg_subcategory (str): Subcategory of school data to filter from the skolereg data.

    Returns:
        pd.DataFrame | UtdData: The consolidated dataset after validation and merging operations.

    Raises:
        ValueError: If essential columns are missing or have duplicates in the input data.
        TypeError: If 'skolereg_keep_cols' or 'vigo_keep_cols' are not provided in an appropriate format.
    """
    # import skolereg and vigo_skole
    skolereg = get_skolereg(year=year, sub_category=skolereg_subcategory)
    vigo = get_vigo_skole(year=year)

    # initial checks

    # check that orgnr-cols are not equal
    if orgnr_col_innfil == orgnrbed_col_innfil:
        raise ValueError(
            "Orgnr variables should not be equal. Insert two different variables, i.e. orgnr, orgnrbed"
        )

    # verify that inn-data contains orgnr-cols and fskolenr-col
    if isinstance(data, UtdData):
        data_cols = list(data.data.columns)
        if orgnr_col_innfil not in data_cols or orgnrbed_col_innfil not in data_cols:
            raise ValueError(
                f"Inndata does not contain both {orgnr_col_innfil} and {orgnrbed_col_innfil} variables"
            )
        if fskolenr_col_innfil not in data_cols:
            raise ValueError(f"Inndata does not contain variable {fskolenr_col_innfil}")
    else:
        data_cols = list(data.columns)
        if orgnr_col_innfil not in data_cols or orgnrbed_col_innfil not in data_cols:
            raise ValueError(
                f"Inndata does not contain both {orgnr_col_innfil} and {orgnrbed_col_innfil} variables"
            )
        if fskolenr_col_innfil not in data_cols:
            raise ValueError(f"Inndata does not contain variable {fskolenr_col_innfil}")

    # verify that keep cols variables are list or set
    if type(skolereg_keep_cols) not in [list, set, type(None)]:
        raise TypeError("Please insert skolereg_keep_cols as list or set")
    if type(vigo_keep_cols) not in [list, set, type(None)]:
        raise TypeError("Please insert vigo_keep_cols as list or set")

    # convert keep cols variabels to set
    if isinstance(skolereg_keep_cols, list):
        skolereg_keep_cols = set(skolereg_keep_cols)
    elif isinstance(skolereg_keep_cols, type(None)):
        skolereg_keep_cols = set(skolereg.data.columns)
        skolereg_keep_cols.discard("orgnr")
        skolereg_keep_cols.discard("orgnrbed")
        skolereg_keep_cols.discard("orgnrforetak")

    if isinstance(vigo_keep_cols, list):
        vigo_keep_cols = set(vigo_keep_cols)

    if year == "latest":
        pass
    elif len(str(year)) == 4 and str(year).isdigit():
        pass
    else:
        year = input("Formatet på aargangsvariabel er feil. Vi trenger YYYY:")

    # merge skolereg on data on orgnr
    skolereg.key_cols = ["orgnr"]
    utdanning_logger.logger.info(
        f"Merging skolereg on dataset on variable '{orgnr_col_innfil}'"
    )
    skolereg_orgnr_merged = skolereg.merge_on(
        dataset=data, key_col_in_data=orgnr_col_innfil, keep_cols=skolereg_keep_cols
    )
    skolereg_not_merged_orgnr = skolereg_orgnr_merged.loc[
        skolereg_orgnr_merged["_merge"] != f"{skolereg.key_cols[0]}_both"
    ].copy()
    skolereg_orgnr_merged = skolereg_orgnr_merged.loc[
        skolereg_orgnr_merged["_merge"] == f"{skolereg.key_cols[0]}_both"
    ].copy()

    # merge skolereg on data on orgnrbed
    skolereg.key_cols = ["orgnrbed"]
    utdanning_logger.logger.info(
        f"Merging skolereg on dataset on variable '{orgnrbed_col_innfil}'"
    )
    skolereg_not_merged_orgnr = skolereg_not_merged_orgnr[data_cols]
    skolereg_orgnrbed_merged = skolereg.merge_on(
        dataset=skolereg_not_merged_orgnr,
        key_col_in_data=orgnrbed_col_innfil,
        keep_cols=skolereg_keep_cols,
    )
    skolereg_not_merged = skolereg_orgnrbed_merged.loc[
        skolereg_orgnrbed_merged["_merge"] != f"{skolereg.key_cols[0]}_both"
    ].copy()
    skolereg_orgnrbed_merged = skolereg_orgnrbed_merged.loc[
        skolereg_orgnrbed_merged["_merge"] == f"{skolereg.key_cols[0]}_both"
    ].copy()

    # merging vigo_skole catalog on datset on fskolenr
    utdanning_logger.logger.info(
        f"Merging vigo_skole on dataset on variable '{orgnr_col_innfil}'"
    )
    skolereg_not_merged = skolereg_not_merged[data_cols]
    vigo_fskolenr_merged = vigo.merge_on(
        dataset=skolereg_not_merged,
        key_col_in_data=fskolenr_col_innfil,
        keep_cols=vigo_keep_cols,
    )
    vigo_not_merged_fskolenr = vigo_fskolenr_merged.loc[
        vigo_fskolenr_merged["_merge"] != f"{vigo.key_cols[0]}_both"
    ].copy()
    vigo_fskolenr_merged = vigo_fskolenr_merged.loc[
        vigo_fskolenr_merged["_merge"] == f"{vigo.key_cols[0]}_both"
    ].copy()

    # concatenating partially merged datasets
    skolereg_orgnr_merged["_merge"] = orgnr_col_innfil
    skolereg_orgnrbed_merged["_merge"] = orgnrbed_col_innfil
    vigo_fskolenr_merged["_merge"] = fskolenr_col_innfil
    vigo_not_merged_fskolenr["_merge"] = None
    final = pd.concat(
        [
            skolereg_orgnr_merged,
            skolereg_orgnrbed_merged,
            vigo_fskolenr_merged,
            vigo_not_merged_fskolenr,
        ]
    )

    # final status report
    print("-" * 80)
    utdanning_logger.logger.info("Final merge report")
    print("-" * 80)
    utdanning_logger.logger.info("\n%s", final["_merge"].value_counts(dropna=False))
    if len(final) > len(data):
        n_dups = len(final) - len(data)
        utdanning_logger.logger.warning(f"{n_dups} duplicates were found")
    else:
        utdanning_logger.logger.info("Duplicates rows not detected")
    if isinstance(data, UtdData):
        return UtdData(data=final, path=data.path)
    return final
