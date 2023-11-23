OPTIONS NOSOURCE;
* ---------------- NB! * kjør med SUBMIT * NB! ---------------------------------------- *;
*****************************************************************************************;
* Prosjekt ......: X:\360\Fellesprogrammer\Formater\
* Programnavn ...: a01_felles_utdstat
* ------------------------------------------------------------------------------------- *;
* Skrevet når/av : 04.12.2006 - Kåre Nygård
* Beskrivelse ...: lager formater for flere variabler i utdanningsstatistikk
*                  NB! formatnavn må være maks. 8 pos.(inkl. $)
*****************************************************************************************;
RSUBMIT;
libname library '$UTD/prog/formater';
run;
proc format library = library;

*-- klassetrinn --*;
value klasse
  0 = '00'
  1 = '01'
  2 = '02'
  3 = '03'
  4 = '04'
  5 = '05'
  6 = '06'
  7 = '07'
  8 = '08'
  9 = '09'
  . = " -"
;

*-- evufjern --*;
value $evufjer
  '1' = '1 Ordinær utdanning - unntatt fjernundervisning'
  '2' = '2 Etter-/videreutdanning - unntatt fjernundervisning'
  '3' = '3 Ordinær utdanning som fjernundervisning - unntatt godkjent nettskoleutdanning'
  '4' = '4 Etter-/videreutdanning som fjernundervisning - unntatt godkjent nettskoleutdanning'
  '5' = '5 Ordinær utdanning som fjernundervisning - godkjent nettskoleutdanning'
  '6' = '6 Etter-/videreutdanning som fjernundervisning - godkjent nettskoleutdanning '
;

*-- elevstatus --*;
VALUE $elevsta
  'A' = 'A Alternativ opplæringsplan (IOP utenfor læreplan) i hele kurset'
  'E' = 'E Elev'
  'P' = 'P Privatist'
  'S' = 'S Sluttet på hele kurset i løpet av skoleåret (etter 1. oktober)'
  'U' = 'U Utenlandsk utvekslingselev i Norge'
  'V' = 'V Voksne'
  'Blank' = '  Andre'
;

*--  --*;
value $ktrinn
 '1'	= '1-grunnkurs, Vg1'
 '2'	= '2-VKI, Vg2'
 '3'	= '3-VKII, Vg3/bedriftsopplæring'
 '4'	= '4-kurstrin utfylt utover vg 1,2,3'
 '5'	= '5-fagskoleutdanning'
other	= 'Annen utdanning/ktrinn blank'
;

*-- Skoleslag, omkodet --*;
value $sslag
  '1' = '1 Grunnskole'
  '2' = '2 Videregående skole'
  '3' = '3 Universitet og høgskole'
other = 'Uoppgitt'
;

*--  --*;
value $utd
  '100' = '100 Grunnskoler'
  '211' = '211 Elever i vgo'
  '212' = '212 Lærlinger i vgo'
  '213' = '213 Voksne i vgo'
  '220' = '220 Annen videregående utdanning'
  '311' = '311 Statlige høgskoler'
  '312' = '312 Militære høgskoler'
  '313' = '313 Andre høgskoler'
  '320' = '320 Annen universitets- og høgskoleutdanning'
  '400' = '400 Universiteter og vitenskapelige høgskoler'
  '401' = '401 Universiteter'
  '402' = '402 Vitenskapelige høgskoler'
  '510' = '510 Folkehøgskoler'
  '520' = '520 Arbeidsmarkedskurs'
  '610' = '610 Videregående utdanning i utlandet'
  '620' = '620 Høyere utdanning i utlandet'
  '710' = '710 Fagskoleutdanning'
  '   ' = '    Blank'
;

  *-- kilde --*;
  value $kilde
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
   '52' = '52 Etterrapporterte fagskoler'
  ;

*--  --*;
value $komp
 '1'	= '1-Generell studiekompetanse'
 '2'	= '2-Yrkeskomp.med fag-/svennebrev'
 '3'	= '3-Yrkeskompetanse dokumentert med vitnemål'
 '4'	= '4-Underveis til yrkeskomp.,3år i skole før lære'
 '5'	= '5-Yrkeskomp.med fag-/svennebrev,læretid etter 3 år i skole'
 ;

*-- kurstrin --*;
value $kurstri
  'A' = 'Ettårig grunnkurs/Vg1'
  'D' = 'Alternativ opplæring/grunnkompetanse'
  'F' = 'Andre fagskoler (Lov om fagskoleutdanning trådte i kraft 20.06.2003)'
  'H' = 'VK I/Vg2'
  'I' = 'Særløp'
  'K' = 'To- eller treårige kurs (ikke GK over to år)'
  'P' = 'VK II/bedriftsopplæring/Vg3'
  'T' = 'VK III/Bedriftsopplæring etter VK II/Vg3 i skole'
  'U' = 'Teknisk fagskole'
  'Z' = 'Kurs for praksiskandidater'
other = 'Uoppgitt'
;

*-- studieretning/utdanningsprogram --*;
value $studret
  '21' = '21 Allmenne, økonomiske og administrative fag'
  '22' = '22 Musikk, dans og drama'
  '23' = '23 Idrettsfag'
  '31' = '31 Helse- og sosialfag'
  '32' = '32 Naturbruk'
  '33' = '33 Formgivingsfag'
  '34' = '34 Hotell- og næringsmiddelfag'
  '35' = '35 Byggfag'
  '36' = '36 Tekniske byggfag'
  '37' = '37 Elektrofag'
  '38' = '38 Mekaniske fag'
  '39' = '39 Kjemi- og prosessfag'
  '40' = '40 Trearbeidsfag'
  '41' = '41 Medier og kommunikasjon'
  '42' = '42 Salg og service'   
  '50' = '50 Teknisk fagskole'        
  '51' = '51 Andre fagskoler'
  '60' = '60 Idrettsfag' /* Kunnskapsløftet */
  '61' = '61 Musikk, dans og drama' /* Kunnskapsløftet */
  '62' = '62 Studiespesialisering' /* Kunnskapsløftet */
  '63' = '63 Kunst, design og arkitektur' /* Kunnskapsløftet */
  '64' = '64 Medier og kommunikasjon' /* Kunnskapsløftet */
  '70' = '70 Bygg- og anleggsteknikk' /* Kunnskapsløftet */
  '71' = '71 Design og håndverk' /* Kunnskapsløftet */
  '72' = '72 Elektrofag' /* Kunnskapsløftet */
  '73' = '73 Helse- og oppvekstfag' /* Kunnskapsløftet */
  '74' = '74 Medier og kommunikasjon(gammel ordning)' /* Kunnskapsløftet */
  '75' = '75 Naturbruk' /* Kunnskapsløftet */
  '76' = '76 Restaurant- og matfag' /* Kunnskapsløftet */
  '77' = '77 Service og samferdsel' /* Kunnskapsløftet */
  '78' = '78 Teknikk og industriell produksjon' /* Kunnskapsløftet */
  '98' = '98 Alternativ opplæring' /* Kunnskapsløftet */
  '99' = '99 Paragraf-20-kurs med uoppgitt studieretning'
 other = '   Uten studieretning'        
;

*-- sosial bakgrunn --*;
value $sosbak
  '1' = 'Mor eller far eller begge har utd. på nivå 7 eller 8'
  '2' = 'Mor eller far eller begge har utd. på nivå 6'
  '3' = 'Mor eller far eller begge har utd. på nivå 3, 4 eller 5'
  '4' = 'Mor eller far eller begge har utd. på nivå 0, 1 eller 2'
  '9' = 'Uoppgitt, når begge foreldrene har uoppgitt utdanning'
other = 'Uoppgitt'
;

value $sosbakb
  '1' = 'Lang høyere utdanning'
  '2' = 'Kort høyere utdanning'
  '3' = 'Videregående utdanning'
  '4' = 'Grunnskoleutdanning'
other = 'Uoppgitt'
;

*-- utfall resultat --*;
value $utfalla
  'A' = 'A Annulert'
  'I' = 'I Ikke bestått'
  'B' = 'B Bestått'
;
*-- utfall --*;
value $utfallc
  'C' = 'C Annulert'
  'D' = 'D Ikke bestått'
  'P' = 'P Bestått'
;
*-- utfall omkodet --*;
value $utfall
  '2' = '2 Ikke fullført'
  '8' = '8 Fullført'
;

*-- heltid/deltid --*;
value $heldel
  '1' = '1 heltid'
  '2' = '2 deltid'
;

*-- filtype for uh-avsluttet --*;
value $filavsl
  '3' = '3 Eksamen'
  '4' = '4 Grad'
;

*-- kodetype --*;
value $kode_ut
  '1' = '1 Samlekode'
  '2' = '2 Enkeltkode'
;

*--  --*;
value $utdplan
  '1' = '1 Har utdanningsplan'
  '2' = '2 Har ikke utdanningsplan'
;

*--  --*;
value $realkom
  '0' = '0 Generell studiekompetanse'
  '1' = '1 Realkompetanse'
  '2' = '2 Annet, uoppgitt'
  '3' = '3 Yrkesfaglig utd.(Y-veien)'
  ' ' = '  blank'
;

*--  --*;
value $utveks
  ' ' = '  Ikke utveksling pr. 1/10'
  '1' = '1 Innreisende pr. 1/10'
  '2' = '2 Utreisende pr. 1/10'
;

*-- gradmerk --*;
value $gradmrk
  'B' = 'B Bachelor-utdanning'
  'H' = 'H Høgskolekandidat i ingeniørfag'
  'M' = 'M Master-utdanning'
;

* -- uhgruppe + gradmerk fra NUS2000-katalog -- *;
value $uhgrmrk
  '01 ' = '01 Forberedende prøver'
  '02 ' = '02 Lavere nivås utdanning'
  '03 ' = '03 Andre ettårige studier, grunnutdanning'
  '04 ' = '04 Høgskolekandidat, toårig,'
  '05 ' = '05 Ingeniørutdanning, toårig grunnutdanninger'
  '05H' = '05H Høgskolekandidat i ingeniørfag, toårig'
  '06 ' = '06 Andre toårige studier, grunnutdanninger'
  '07 ' = '07 Høgskolekandidat, treårig'
  '08 ' = '08 Allmenn-/grunnskolelærerutdanning'
  '08B' = '08B Bachelor, lærerutdanning (ved Rudolf Steinerhøyskolen)'
  '09 ' = '09 Førskolelærer'
  '09B' = '09B Bachelor, førskole-/barnehagelærerutdanning'
  '10 ' = '10 Yrkesfaglærer'
  '10B' = '10B Bachelor, yrkesfaglærerutdanning'
  '11 ' = '11 Ingeniørutdanning, treårig'
  '11B' = '11B Bachelor, ingeniørfag'
  '12 ' = '12 Sykepleier'
  '12B' = '12B Bachelor, sykepleierutdanning'
  '13 ' = '13 Helsefagutdanning, 3-4 år grunnutdanning, ikke sykepleier'
  '13B' = '13B Bachelor, helsefagutdanning, ikke sykepleier'
  '14 ' = '14 Høgskolekandidat, fireårig'
  '14B' = '14B Bachelor, høgskolekandidat, fireårig'
  '15 ' = '15 Etatsutdanninger'
  '16 ' = '16 Andre tre-og fireårige grunnutdanninger (ikke høgskolekandidat)'
  '17 ' = '17 Cand.mag.-utdanning'
  '18 ' = '18 Videreutd. i ledelse/org./adm./økonomi'
  '19 ' = '19 Videreutd. for ingeniører'
  '20 ' = '20 Videreutd. for sykepleiere'
  '21 ' = '21 Videreutd. for annet helsepersonell enn sykepleiere'
  '22 ' = '22 Annen videreutd. til og med to år'
  '23 ' = '23 Praktisk-pedagogisk utdanning (PPU)'
  '24 ' = '24 Siviløkonom'
  '25B' = '25B Bachelor, allmenne fag'
  '26B' = '26B Bachelor, humanistiske og estetiske fag, ikke 4-årig'
  '27B' = '27B Bachelor, lærerutdanninger og utdanninger i pedagogikk, ikke allmenn-/grunnskole-, førskole-, fag- og yrkesfaglærer'
  '28B' = '28B Bachelor, samfunnsfag og juridiske fag'
  '29B' = '29B Bachelor, økonomiske og administrative fag'
  '30B' = '30B Bachelor, naturvitenskapelige fag, håndverksfag og tekniske fag, ikke ingeniør'
  '31 ' = '31 Høyere nivås utdanning'
  '32 ' = '32 Cand.philol'
  '33 ' = '33 Cand.polit'
  '34 ' = '34 Cand.scient/cand.real.-utdanning'
  '35 ' = '35 Cand.jur.-utdanning'
  '35M' = '35M Master, rettsvitenskap'
  '36 ' = '36 Cand.med.-utdanning'
  '37 ' = '37 Cand.agric.-Utdanning'
  '38 ' = '38 Cand.musicae.-utdanning'
  '39 ' = '39 Cand.theol.-utdanning'
  '40 ' = '40 Cand.san.-utdanning'
  '41 ' = '41 Cand.oecon.-utdanning'
  '42 ' = '42 Cand.psychol.-utdanning'
  '43 ' = '43 Cand.sociol.-utdanning'
  '44 ' = '44 Cand.sosion.-utdanning'
  '45 ' = '45 Cand.act.-utdanning'
  '45M' = '45M Master, aktuarfag' 
  '46 ' = '46 Cand.techn.-utdanning'
  '47 ' = '47 Cand.pharm.-utdanning'
  '47M' = '47M Master, farmasi-utdanning'
  '48 ' = '48 Cand.med.vet.'
  '49 ' = '49 Cand.merc.'
  '50 ' = '50 Cand.odont'
  '50M' = '50M Master, odontologi-utdanning'
  '51 ' = '51 Cand.ed./cand.paed'
  '52 ' = '52 Hovedfagskandidat'
  '53 ' = '53 Magisterutdanning'
  '54 ' = '54 Siviløkonomutdanning,CEMS-master'
  '54M' = '54M Siviløkonom-/Master-utdanning'
  '55 ' = '55 Sivilingeniør'
  '55M' = '55M Master, teknologifag'
  '56 ' = '56 Master of Science'
  '56M' = '56M Master of Science'
  '57 ' = '57 Master of Philosophy'
  '57M' = '57M Master of Philosophy'
  '58 ' = '58 Master of Arts'
  '58M' = '58M Master of Arts'
  '59 ' = '59 Master of International Business'
  '59M' = '59M Master of International Business'
  '60 ' = '60 Master of Business Administration'
  '60M' = '60M Master of Business Administration'
  '61 ' = '61 Master of Management'
  '61M' = '61M Master of Management'
  '62 ' = '62 Master of Technology Management'
  '62M' = '62M Master of Technology Management'
  '63 ' = '63 Mastergrader ved statlige høgskoler'
  '63M' = '63M Mastergrader ved statlige høgskoler'
  '64 ' = '64 Master of Laws'
  '64M' = '64M Master of Laws'
  '65 ' = '65 Annen utd. på nivå 7,ikke videreutd./påbygging'
  '66 ' = '66 Videreutdanninger/påbygging, inntil to år'
  '67 ' = '67 Spesialutdanning for leger og tannleger'
  '68 ' = '68 Jordmorutdanning, to år'
  '69M' = '69M Master, ettårig, lavere nivå'
  '70 ' = '70 Ph.d.'
  '71M' = '71M Master, allmenne fag'
  '72M' = '72M Master, humanistiske og estetiske fag'
  '73M' = '73M Master, lærerutdanninger og utdanninger i pedagogikk'
  '74M' = '74M Master, samfunnsfag og juridiske fag, ikke rettsvitenskap'
  '75M' = '75M Master, økonomiske og administrative fag, ikke siviløkonom'
  '76M' = '76M Master, naturvitenskapelige fag, håndverksfag og tekniske fag, ikke sivilingeniør/master i teknologi'
  '77M' = '77M Master, helse-, sosial- og idrettsfag, ikke farmasi og odontologi'
  '78M' = '78M Master, primærnæringsfag'
  '79M' = '79M Master, samferdsels- og sikkerhetsfag og andre servicefag'
  '80M' = '80M Master, uoppgitt fagfelt'
  '81 ' = '81 Dr.philos.'
  '82 ' = '82 Dr.polit'
  '83 ' = '83 Dr.scient'
  '84 ' = '84 Dr.juris/dr.legis.'
  '85 ' = '85 Dr.med.'
  '86 ' = '86 Dr.theol.'
  '87 ' = '87 Dr.techn.'
  '88 ' = '88 Dr.odont.'
  '89 ' = '89 Dr.med.vet.'
  '90 ' = '90 Dr.agric.'
  '91 ' = '91 Dr.oecon.'
  '92 ' = '92 Dr.ing.'
  '93 ' = '93 Dr.art'
  '94 ' = '94 Dr.psychol.'
  '95 ' = '95 Andre forskerutdanninger (lisensiater)'
  '96B' = '96B Bachelor, helse-, sosial- og idrettsfag, ikke sykepleier og helsefag som inngår i UH-gruppe 13B'
  '97B' = '97B Bachelor, primærnæringsfag'
  '98B' = '98B Bachelor, samferdsels- og sikkerhetsfag og andre servicefag'
  '99B' = '99B Bachelor, uoppgitt fagfelt'
  '   ' = 'blank'
;
* -- bostedskommune i forhold til skolekommune -- *;
value $skobo
  '1' = '1 bokommune = skolekommune'
  '2' = '2 bofylke = skolefylke'
  '3' = '3 bofylke ulik skolefylke'
  '9' = '9 annet'
;
run;
ENDRSUBMIT;
