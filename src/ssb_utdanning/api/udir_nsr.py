import pandas as pd
from typing import Any
from collections import Iterable
import requests


BASE_URL = "https://data-nsr.udir.no/v4"


def find_nsr_orgnr(orgnr: str) -> dict[str, Any]:
    response = requests.get(f"{BASE_URL}/enhet/{orgnr}")
    response.raise_for_status()
    return response.json()

def find_owner_orgnr(orgnr: str) -> str:
    foreldre = find_nsr_orgnr(orgnr)["ForeldreRelasjoner"]
    for forelder in foreldre:
        if forelder["Relasjonstype"]["Navn"] == "Eierstruktur":
            return forelder["Enhet"]["Organisasjonsnummer"]

def map_uorgnr_foretak(orgnr_col: pd.Series | Iterable) -> dict[str, str]:
    unique_orgnr = {orgnr for orgnr in orgnr_col if orgnr.startswith("U")}
    return {orgnr: find_owner_orgnr(orgnr) for orgnr in unique_orgnr}
    