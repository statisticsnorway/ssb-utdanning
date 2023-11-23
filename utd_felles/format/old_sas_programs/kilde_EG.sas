*****************************************************************************************;
* Prosjekt ......: X:\360\Fellesprogrammer\Formater\
* Programnavn ...: kilde.sas    se også: a01_felles_utdstat.sas
* ------------------------------------------------------------------------------------- *;
* Skrevet når/av : 19.10.2005 - Kåre Nygård
* Beskrivelse ...: lager formater basert på kilde
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 13.01.2009 - Kåre Nygård
* Beskrivelse ...: ny: 26 folkehøgskoler (tidl.23)
*                  gjelder f.o.m. elever per 01.10.2008 og fullført skoleåret 2007/2008
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 22.11.2011 - Kåre Nygård
* Beskrivelse ...: ny: 27 nettskoler
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 28.08.2012 - Greta K. Østli
* Beskrivelse ...: ny: 49 DBH data /*Data fra DBH, inkl. både fagskole- og UH-data */
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 11.03.2013 - Kåre Nygård
* Beskrivelse ...: lager også et kort format: $kildek
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 16.02.2016 - Kåre Nygård
* Beskrivelse ...: 23: ny tekst
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 06.01.2020 - KMD
* Beskrivelse ...: Tilrettelagt EG, tatt bort RSUBMIT
* ------------------------------------------------------------------------------------- *;
*****************************************************************************************;

proc format;
  value $kilde
   ' '  = 'Blank'
   '01' = '01 Folke og boligtellingen 1970'
   '04' = '04 Undersøkelsen om skolegang 1999'
   '05' = '05 Folke og boligtellingen 1980'
   '07' = '07 Undersøkelsen om utdanning 2011'
   '08' = '08 Undersøkelsen om utdanning 2012'
   '10' = '10 Avsluttet grunnskole'
   '11' = '11 DUF,Datasystemet for utlendings-/flyktningsaker-Utlendingsdir'
   '20' = '20 Elev- og avsluttet-data rapportert fra fylkeskommunene'
   '21' = '21 Fagopplæring rapportert fra fylkeskommunene'
   '22' = '22 Arbeidsdirektoratet'
   '23' = '23 Annen videregående utdanning'
   '24' = '24 Militære videregående skoler'
   '25' = '25 Voksne videreg. opplæring fra FK/ utgått høsten 2009'
   '26' = '26 Folkehøgskoler'
   '27' = '27 Nettskoler'
   '30' = '30 Nasjonal vitnemålsdatabase (NVB)'
   '31' = '31 Autorisasjonsregisteret for helsepersonell (HPR)'
   '40' = '40 FS universiteter'
   '41' = '41 FS høgskoler'
   '42' = '42 MSTAS universiteter'
   '43' = '43 MSTAS høgskoler'
   '44' = '44 Diskett/skjema universiteter'
   '45' = '45 Diskett/skjema høgskoler'
   '46' = '46 Militære høgskoler'
   '47' = '47 Doktorgradsregister NIFU'
   '48' = '48 Statens lånekasse for utdanning'
   '49' = '49 DBH Database for høyere utdanning' /* Fagskole- og UH-data fra DBH */
   '50' = '50 Etterrapporterte grader'
   '51' = '51 Etterrapporterte fagprøver'
   '52' = '52 Etterrapporterte fagskoledata'
   '99' = '99 Uoppgitt' 
  ;
run;
proc format;
  value $kildek
   '07' = '07 Undersøkelsen om utdanning 2011'
   '08' = '08 Undersøkelsen om utdanning 2012'
   '10' = '10 Avsluttet grunnskole'
   '11' = '11 Utdanningsopplysninger fra DUF' /* ??? */
   '20' = '20 Elev- og avsluttet-data' /* rapportert fra fylkeskommunene*/
   '21' = '21 Fagopplæring' /* rapportert fra fylkeskommunene */
   '22' = '22 Arbeidsdirektoratet'
   '23' = '23 Annen videregående utdanning'
   '24' = '24 Militære videregående skoler'
   '25' = '25 Voksne i videregående opplæring' /* fra FK/ utgått høsten 2009 */
   '26' = '26 Folkehøgskoler'
   '27' = '27 Nettskoler'
   '30' = '30 Nasjonal vitnemålsdatabase (NVB)'
   '31' = '31 Autorisasjonsregisteret for HPR' /* for helsepersonell */
   '40' = '40 FS universiteter'
   '41' = '41 FS høgskoler'
   '42' = '42 MSTAS universiteter'
   '43' = '43 MSTAS høgskoler'
   '44' = '44 Diskett/skjema universiteter'
   '45' = '45 Diskett/skjema høgskoler'
   '46' = '46 Militære høgskoler'
   '47' = '47 Doktorgradsregister NIFU'
   '48' = '48 Statens lånekasse for utdanning'
   '49' = '49 DBH Database for høyere utdanning' /* Fagskole- og UH-data fra DBH */
   '50' = '50 Etterrapporterte grader'
   '51' = '51 Etterrapporterte fagprøver'
   '52' = '52 Etterrapporterte fagskoledata'
  ;
run;
