"""Katalogs are files that are somewhere inbetween real data and metadata.

They usually have a single columns with some sort of identifier, like orgnr or nus2000.
Then they have 2+ columns of other groupings or data that can be "attached" to real data.
They may represent a list of idents that there is no other info on, that we have tracked down info for,
that we would like to "re-attach" each year, for example.

Katalogs can also be called "kodeverk", "kodelister", "omkodingskatalog" etc.
View "katalog" as an umbrella-term above these.
"""

from ssb_utdanning.katalog.katalog import UtdKatalog as UtdKatalog
