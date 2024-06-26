from ssb_utdanning import UtdData
from ssb_utdanning import orgnrkontroll_func
from ssb_utdanning.orgnrkontroll import get_skolereg
from ssb_utdanning.orgnrkontroll import get_vigo_skole

skolereg = get_skolereg().data

vigo = get_vigo_skole().data


path_inn = "/ssb/stamme01/utd_pii/grskavsl/wk16/MOD/ssb-prod-gro-grunnskole-produkt/klargjorte-data/"
filename_inn = "kag_nudb_p2022_p2023_v1.parquet"
inndata = UtdData(path=path_inn + filename_inn)
inndata.data = inndata.data[["inn_fnr", "orgnr", "fskolenr"]]
inndata.data.drop_duplicates(subset="inn_fnr", inplace=True)


result = orgnrkontroll_func(
    data=inndata,
    year="latest",
    skolereg_keep_cols=["nace1_sn07", "nace2_sn07", "nace3_sn07", "skolekom"],
    vigo_keep_cols=["SKOLENR", "KOMMNR"],
    orgnr_col_innfil="orgnr",
    fskolenr_col_innfil="fskolenr",
    skolereg_subcategory="",
)
