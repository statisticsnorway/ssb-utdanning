"""The orgnrkontroll tries to apply information from different catalogues to fill out information on education-institutions.

It tries to join on both the columns orgnr and orgnrbed, from for example skoleregister and vigo.
While running it reports on how many are missing join-opportunities. The schools with no matches are left up to the user to correct for.
"""

from ssb_utdanning.orgnrkontroll.orgnrkontroll import get_skolereg
from ssb_utdanning.orgnrkontroll.orgnrkontroll import get_vigo_skole
from ssb_utdanning.orgnrkontroll.orgnrkontroll import orgnrkontroll_func
