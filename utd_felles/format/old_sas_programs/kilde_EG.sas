*****************************************************************************************;
* Prosjekt ......: X:\360\Fellesprogrammer\Formater\
* Programnavn ...: kilde.sas    se ogs�: a01_felles_utdstat.sas
* ------------------------------------------------------------------------------------- *;
* Skrevet n�r/av : 19.10.2005 - K�re Nyg�rd
* Beskrivelse ...: lager formater basert p� kilde
* ------------------------------------------------------------------------------------- *;
* Endret n�r/av  : 13.01.2009 - K�re Nyg�rd
* Beskrivelse ...: ny: 26 folkeh�gskoler (tidl.23)
*                  gjelder f.o.m. elever per 01.10.2008 og fullf�rt skole�ret 2007/2008
* ------------------------------------------------------------------------------------- *;
* Endret n�r/av  : 22.11.2011 - K�re Nyg�rd
* Beskrivelse ...: ny: 27 nettskoler
* ------------------------------------------------------------------------------------- *;
* Endret n�r/av  : 28.08.2012 - Greta K. �stli
* Beskrivelse ...: ny: 49 DBH data /*Data fra DBH, inkl. b�de fagskole- og UH-data */
* ------------------------------------------------------------------------------------- *;
* Endret n�r/av  : 11.03.2013 - K�re Nyg�rd
* Beskrivelse ...: lager ogs� et kort format: $kildek
* ------------------------------------------------------------------------------------- *;
* Endret n�r/av  : 16.02.2016 - K�re Nyg�rd
* Beskrivelse ...: 23: ny tekst
* ------------------------------------------------------------------------------------- *;
* Endret n�r/av  : 06.01.2020 - KMD
* Beskrivelse ...: Tilrettelagt EG, tatt bort RSUBMIT
* ------------------------------------------------------------------------------------- *;
*****************************************************************************************;

proc format;
  value $kilde
   ' '  = 'Blank'
   '01' = '01 Folke og boligtellingen 1970'
   '04' = '04 Unders�kelsen om skolegang 1999'
   '05' = '05 Folke og boligtellingen 1980'
   '07' = '07 Unders�kelsen om utdanning 2011'
   '08' = '08 Unders�kelsen om utdanning 2012'
   '10' = '10 Avsluttet grunnskole'
   '11' = '11 DUF,Datasystemet for utlendings-/flyktningsaker-Utlendingsdir'
   '20' = '20 Elev- og avsluttet-data rapportert fra fylkeskommunene'
   '21' = '21 Fagoppl�ring rapportert fra fylkeskommunene'
   '22' = '22 Arbeidsdirektoratet'
   '23' = '23 Annen videreg�ende utdanning'
   '24' = '24 Milit�re videreg�ende skoler'
   '25' = '25 Voksne videreg. oppl�ring fra FK/ utg�tt h�sten 2009'
   '26' = '26 Folkeh�gskoler'
   '27' = '27 Nettskoler'
   '30' = '30 Nasjonal vitnem�lsdatabase (NVB)'
   '31' = '31 Autorisasjonsregisteret for helsepersonell (HPR)'
   '40' = '40 FS universiteter'
   '41' = '41 FS h�gskoler'
   '42' = '42 MSTAS universiteter'
   '43' = '43 MSTAS h�gskoler'
   '44' = '44 Diskett/skjema universiteter'
   '45' = '45 Diskett/skjema h�gskoler'
   '46' = '46 Milit�re h�gskoler'
   '47' = '47 Doktorgradsregister NIFU'
   '48' = '48 Statens l�nekasse for utdanning'
   '49' = '49 DBH Database for h�yere utdanning' /* Fagskole- og UH-data fra DBH */
   '50' = '50 Etterrapporterte grader'
   '51' = '51 Etterrapporterte fagpr�ver'
   '52' = '52 Etterrapporterte fagskoledata'
   '99' = '99 Uoppgitt' 
  ;
run;
proc format;
  value $kildek
   '07' = '07 Unders�kelsen om utdanning 2011'
   '08' = '08 Unders�kelsen om utdanning 2012'
   '10' = '10 Avsluttet grunnskole'
   '11' = '11 Utdanningsopplysninger fra DUF' /* ??? */
   '20' = '20 Elev- og avsluttet-data' /* rapportert fra fylkeskommunene*/
   '21' = '21 Fagoppl�ring' /* rapportert fra fylkeskommunene */
   '22' = '22 Arbeidsdirektoratet'
   '23' = '23 Annen videreg�ende utdanning'
   '24' = '24 Milit�re videreg�ende skoler'
   '25' = '25 Voksne i videreg�ende oppl�ring' /* fra FK/ utg�tt h�sten 2009 */
   '26' = '26 Folkeh�gskoler'
   '27' = '27 Nettskoler'
   '30' = '30 Nasjonal vitnem�lsdatabase (NVB)'
   '31' = '31 Autorisasjonsregisteret for HPR' /* for helsepersonell */
   '40' = '40 FS universiteter'
   '41' = '41 FS h�gskoler'
   '42' = '42 MSTAS universiteter'
   '43' = '43 MSTAS h�gskoler'
   '44' = '44 Diskett/skjema universiteter'
   '45' = '45 Diskett/skjema h�gskoler'
   '46' = '46 Milit�re h�gskoler'
   '47' = '47 Doktorgradsregister NIFU'
   '48' = '48 Statens l�nekasse for utdanning'
   '49' = '49 DBH Database for h�yere utdanning' /* Fagskole- og UH-data fra DBH */
   '50' = '50 Etterrapporterte grader'
   '51' = '51 Etterrapporterte fagpr�ver'
   '52' = '52 Etterrapporterte fagskoledata'
  ;
run;
