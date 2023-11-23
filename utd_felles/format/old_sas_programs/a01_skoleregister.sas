*****************************************************************************************;
* Prosjekt ......: X:\360\Fellesprogrammer\Formater\
* Programnavn ...: a01_skoleregister
* ------------------------------------------------------------------------------------- *;
* Skrevet når/av : 06.09.2006 - Kåre Nygård
* Beskrivelse ...: lager formater for variabler på skoleregister
*                  NB! formatnavn må være maks. 8 pos.(inkl. $)
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 06.11.2009 - Kåre Nygård
* Beskrivelse ...: nytt iforb. nye nace-koder SN2007
* ------------------------------------------------------------------------------------- *;
* Endret når/av  : 14.12.2022 - Øyvind S.B
* Beskrivelse ...: la til et semikolon etter proc format i linje 45. Etter feilmelding
* ------------------------------------------------------------------------------------- *;

*****************************************************************************************;

* ------------------------------------------------------------------------------------- *;
* Følgende variabler har formater med tilhørende kodelister i Situasjonsuttaket fra BoF *;
* og som kan være mulige verdier i Skoleregisteret                                      *;
* ------------------------------------------------------------------------------------- *;
*   formatnavn  innhold                                                                 *;
* ------------------------------------------------------------------------------------- *;
*   $eierf      eierforhold - bare tekst - omkodet eierforhold S.360's standard
*   $eierfnr    eierforhold - både eierf-nr og tekst
*   $nace       nacekoder SN2007 i Skoleregisteret
*   $nace02s    nacekoder SN2002 i Skoleregisteret
*   $skolesl    skoleslag for nacekoder SN2007
*   $rectype
*   $regtype    regtype for alle 
*   $reg_tb     regtype for bedrifter avhengig av $rectype
*   $reg_tf     regtype for foretak   avhengig av $rectype
*   $status
*   $mdelr
*   $orgform
*   $sektor

*   NB! bør alle ha denne ?? : other = '* Skal ikke forekomme *'

*****************************************************************************************;

proc format;

*-- eierforhold -- omkodet eierforhold Seksjon 360's standard --*;
*-- 2 gjelder for g2000-g2003 / 4,5 for g2004-.....           --*;
value $eierf
  '1' = 'Stat'
  '2' = 'Kommune/fylkeskommune'
  '3' = 'Privat'
  '4' = 'Kommune'
  '5' = 'Fylke'
  '9' = 'Uoppgitt'
other = 'Skal ikke forekomme'
;

value $eierfnr
  '1' = '1 Stat'
  '2' = '2 Kommune/Fylke'
  '3' = '3 Privat'
  '4' = '4 Kommune'
  '5' = '5 Fylke'
other = '- * Skal ikke forekomme *'
;

value $nace02s
  '80.101' = '80.101 Førskoler'
  '80.102' = '80.102 Grunnskoler'
  '80.103' = '80.103 Spesialskoler for funksjonshemmede'
  '80.104' = '80.104 Kompetansesentra og andre spesialskoler'
  '80.105' = '80.105 PP-tjenester'
  '80.210' = '80.210 Videregående skoler allmennfag'
  '80.220' = '80.220 Videregående skoler yrkesfag'
  '80.301' = '80.301 Universiteter'
  '80.302' = '80.302 Høgskoler statlige'
  '80.303' = '80.303 Høgskoler militære'
  '80.309' = '80.309 Høgskoler andre'
  '80.410' = '80.410 Trafikkskoler'
  '80.421' = '80.421 Folkehøgskoler'
  '80.422' = '80.422 Arbeidsmarkedskurs'
  '80.423' = '80.423 Studieforbundskurs'
  '80.424' = '80.424 Kommunale musikkskoler'
  '80.425' = '80.425 Fond/legat'
  '80.429' = '80.429 Annen undervisning'
  '85.327' = '85.327 Barnehager'
  other    = '       Andre'
;

value $nace
  '85.100' = '85.100 Førskoleundervisning'
  '85.201' = '85.201 Ordinær grunnskoleundervisning'
  '85.202' = '85.202 Spesialskoleundervisning for funksjonshemmede'
  '85.203' = '85.203 Kompetansesentra og annen spesialundervisning'
  '85.310' = '85.310 Videregående opplæring innen allmennfaglige studieretninger'
  '85.320' = '85.320 Videregående opplæring innen tekniske og andre yrkesfaglige studieretninger'
  '85.410' = '85.410 Undervisning ved fagskoler'
  '85.421' = '85.421 Undervisning ved universiteter'
  '85.422' = '85.422 Undervisning ved vitenskapelige høgskoler'
  '85.423' = '85.423 Undervisning ved statlige høgskoler'
  '85.424' = '85.424 Undervisning ved militære høgskoler'
  '85.429' = '85.429 Undervisning ved andre høgskoler'
  '85.510' = '85.510 Undervisning innen idrett og rekreasjon'
  '85.521' = '85.521 Kommunal kulturskoleundervisning'
  '85.522' = '85.522 Undervisning i kunstfag'
  '85.529' = '85.529 Annen undervisning innen kultur'
  '85.530' = '85.530 Trafikkskoleundervisning'
  '85.591' = '85.591 Folkehøgskoleundervisning'
  '85.592' = '85.592 Arbeidsmarkedskurs'
  '85.593' = '85.593 Studieforbunds- og frivillige organisasjoners kurs'
  '85.594' = '85.594 Voksenopplæringssentre'
  '85.595' = '85.595 Timelærervirksomhet'
  '85.596' = '85.596 Undervisning innen religion'
  '85.599' = '85.599 Annen undervisning ikke nevnt annet sted'
  '85.601' = '85.601 Pedagogisk-psykologisk rådgivingstjeneste'
  '85.609' = '85.609 Andre tjenester tilknyttet undervisning'
  '88.911' = '88.911 Barnehager'
/*  other    = '       Andre'*/
;

value $skolesl
   'BH' = 'BH Barnehager'
   'GS' = 'GS Grunnskoler'
   'VG' = 'VG Videregående skoler'
   'UH' = 'UH Universiteter/høgskoler'
   'FH' = 'FH Folkehøgskoler'
/*  other = '   Andre'*/
  ;

value $rectype
  '1' = '1 Foretak'
  '2' = '2 Virksomhet'
other = '- Uoppgitt'
;

value $regtype
  '01' = '01 Enbedriftsforetak'
  '02' = '02 Flerbedriftsforetak'
  '03' = '03 Foretak med kun spesialenheter'
  '04' = '04 Hjelpeforetak'
  '05' = '05 Foretak med kun AAFY'
  '06' = '06 Har aldri hatt bedrift'
  '07' = '07 Skal ikke ha bedrift'
  '08' = '08 Siste bedrift(er) solgt'
  '09' = '09 Siste bedrift(er) slettet'
  '10' = '10 Nytt foretak (skyggesak)'
;

value $reg_tf
  '01' = '01 Enbedriftsforetak'
  '02' = '02 Flerbedriftsforetak'
  '03' = '03 Foretak med kun spesialenheter'
  '04' = '04 Hjelpeforetak'
  '05' = '05 Foretak med kun AAFY'
  '06' = '06 Har aldri hatt bedrift'
  '07' = '07 Skal ikke ha bedrift'
  '08' = '08 Siste bedrift(er) solgt'
  '09' = '09 Siste bedrift(er) slettet'
  '10' = '10 Nytt foretak (skyggesak)'
;

value $reg_tb
  '00' = '00 Investeringsbedrift'
  '01' = '01 Bedrift i enbedriftsforetak'
  '02' = '02 Bedrift i flerbedriftsforetak'
  '03' = '03 Spesialenhet'
  '04' = '04 Hjelpeavdeling'
  '05' = '05 AAFY (underenhet til fysisk person)'
;

value $status
  'B' = 'B Ikke slettet'
  'D' = 'D Slettet som dublett'
  'F' = 'F Slettet for sammenslåing'
  'S' = 'S Slettet'
other = '- Uoppgitt'
;

value $mdelr
  'A' = 'A Livs- og skadeforsikring'
  'B' = 'B Barnehager'
  'D' = 'D Distriktsleger'
  'E' = 'E El-verk'
  'H' = 'H Helseinstitusjoner'
  'K' = 'K Kommuneforetak'
  'S' = 'S Skoleregister'
  'X' = 'X Seksjon for utenrikshandel, energi og industristatistikk'
  'Y' = 'Y Seksjon for bygg- og tjenestestatistikk'
  'Z' = 'Z Seksjon for samferdsel- og reiselivsstatistikk'
;

value $orgform
  'AAFY' = 'AAFY Virk. ikke-næringsdrivende person'
  'ANNA' = 'ANNA Annen juridisk person'
  'ANS'  = 'ANS  Ansvarlig selskap'
  'AS'   = 'AS   Aksjeselskap'
  'ASA'  = 'ASA  Alment aksjeselskap (børsnotert)'
  'BA'   = 'BA   Selskap med begrenset ansvar'
  'BBL'  = 'BBL  Boligbyggelag'
  'BEDR' = 'BEDR Bedrift'
  'BO'   = 'BO   Andre bo'
  'BRL'  = 'BRL  Borettslag'
  'DA'   = 'DA   Selskap med delt ansvar'
  'ENK'  = 'ENK  Enkeltmannsforetak'
  'EOFG' = 'EOFG Europeisk økonomisk foretaksgruppe'
  'ESEK' = 'ESEK Eierseksjonssameie'
  'FKF'  = 'FKF  Fylkeskommunalt selskap'
  'FLI'  = 'FLI  Forening/lag/innretning'
  'FYLK' = 'FYLK Fylkeskommune'
  'GFS'  = 'GFS  Gjensidig forsikringsselskap'
  'IKJP' = 'IKJP Andre ikke juridiske personer'
  'IKS'  = 'IKS  Interkommunalt selskap'
  'KBO'  = 'KBO  Konkursbo'
  'KF'   = 'KF   Kommunalt selskap'
  'KIRK' = 'KIRK Kirkelig enhet (sokn el. fellesråd)'
  'KOMM' = 'KOMM Kommune'
  'KS'   = 'KS   Kommandittselskap'
  'KTRF' = 'KTRF Kontorfellesskap'
  'NUF'  = 'NUF  Nordisk avdeling av utenlandsk enhet'
  'OPMV' = 'OPMV Særskilt oppdelt enhet jfr momslov'
  'ORGL' = 'ORGL Organisasjonsledd'
  'PERS' = 'PERS Andre enkeltpersoner'
  'PRE'  = 'PRE  Partrederi'
  'REGN' = 'REGN Enkeltpers. i Regnskapsførerregisteret'
  'REV'  = 'REV  Enkeltpers. i Revisorregisteret'
  'SAM'  = 'SAM  Tingsrettslig sameie'
  'SF'   = 'SF   Statsforetak'
  'SPA'  = 'SPA  Sparebank'
  'STAT' = 'STAT Staten'
  'STI'  = 'STI  Stiftelse'
  'SÆR'  = 'SÆR  Annet foretak iflg. særskilt lov'
  'TVAM' = 'TVAM Tvangsregistrert for moms'
  'UTBG' = 'UTBG Frivillig registrert utleiebygg'
  'UTLA' = 'UTLA Utenlandsk enhet'
  'VIFE' = 'VIFE Virksomhet drevet i fellesskap'
  'VPFO' = 'VPFO Verdipapirfond'
;

value $sektor
  '000' = '000 Uoppgitt'
  '110' = '110 Stats-og trygdeforvaltningen'
  '150' = '150 Norges Bank'
  '170' = '170 Gammel kode'
  '190' = '190 Statlige låneinstitusjoner'
  '210' = '210 Forretningsbanker, inkl. Postbanken'
  '250' = '250 Sparebanker'
  '310' = '310 Kredittforetak'
  '370' = '370 Finansieringsselskaper'
  '380' = '380 Verdipapirfond'
  '390' = '390 Andre finansielle foretak, ekskl. hj.'
  '391' = '391 Finansielle holdingselskaper'
  '410' = '410 Livsforsikringsselskaper mv.'
  '470' = '470 Skadeforsikringsselskaper'
  '490' = '490 Finansielle hjelpeforetak'
  '510' = '510 Fylkeskommuner'
  '550' = '550 Kommuner'
  '610' = '610 Statens forretningsdrift'
  '630' = '630 Statlig eide foretak'
  '635' = '635 Statsforetak'
  '650' = '650 Gammel kode'
  '660' = '660 Kommunal forretningsdrift'
  '680' = '680 Selvstendig kommuneforetak'
  '710' = '710 Private foretak med begrenset ansvar'
  '740' = '740 Private ikke forr.messige produsentor.'
  '760' = '760 Personlige foretak mv.'
  '770' = '770 Private ikke-forr.messige konsumentor.'
  '790' = '790 Personlig næringsdrivende'
  '810' = '810 Lønnstakere, pensj., trygdede, studenter'
  '890' = '890 Ufordelt sektor'
  '900' = '900 Utenlandske sektorer i alt'
  '930' = '930 Utenlandske kredittinstitusjoner ellers'
/*  other = '--- Uoppgitt'*/
;

run;
