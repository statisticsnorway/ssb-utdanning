OPTIONS NOSOURCE;
* ---------------- NB! * kj�r med SUBMIT * NB! ---------------------------------------- *;
*****************************************************************************************;
* Prosjekt ......: X:\360\Fellesprogrammer\Formater\
* Programnavn ...: a01_felles_utdstat
* ------------------------------------------------------------------------------------- *;
* Skrevet n�r/av : 04.12.2006 - K�re Nyg�rd
* Beskrivelse ...: lager formater for flere variabler i utdanningsstatistikk
*                  NB! formatnavn m� v�re maks. 8 pos.(inkl. $)
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
  '1' = '1 Ordin�r utdanning - unntatt fjernundervisning'
  '2' = '2 Etter-/videreutdanning - unntatt fjernundervisning'
  '3' = '3 Ordin�r utdanning som fjernundervisning - unntatt godkjent nettskoleutdanning'
  '4' = '4 Etter-/videreutdanning som fjernundervisning - unntatt godkjent nettskoleutdanning'
  '5' = '5 Ordin�r utdanning som fjernundervisning - godkjent nettskoleutdanning'
  '6' = '6 Etter-/videreutdanning som fjernundervisning - godkjent nettskoleutdanning '
;

*-- elevstatus --*;
VALUE $elevsta
  'A' = 'A Alternativ oppl�ringsplan (IOP utenfor l�replan) i hele kurset'
  'E' = 'E Elev'
  'P' = 'P Privatist'
  'S' = 'S Sluttet p� hele kurset i l�pet av skole�ret (etter 1. oktober)'
  'U' = 'U Utenlandsk utvekslingselev i Norge'
  'V' = 'V Voksne'
  'Blank' = '  Andre'
;

*--  --*;
value $ktrinn
 '1'	= '1-grunnkurs, Vg1'
 '2'	= '2-VKI, Vg2'
 '3'	= '3-VKII, Vg3/bedriftsoppl�ring'
 '4'	= '4-kurstrin utfylt utover vg 1,2,3'
 '5'	= '5-fagskoleutdanning'
other	= 'Annen utdanning/ktrinn blank'
;

*-- Skoleslag, omkodet --*;
value $sslag
  '1' = '1 Grunnskole'
  '2' = '2 Videreg�ende skole'
  '3' = '3 Universitet og h�gskole'
other = 'Uoppgitt'
;

*--  --*;
value $utd
  '100' = '100 Grunnskoler'
  '211' = '211 Elever i vgo'
  '212' = '212 L�rlinger i vgo'
  '213' = '213 Voksne i vgo'
  '220' = '220 Annen videreg�ende utdanning'
  '311' = '311 Statlige h�gskoler'
  '312' = '312 Milit�re h�gskoler'
  '313' = '313 Andre h�gskoler'
  '320' = '320 Annen universitets- og h�gskoleutdanning'
  '400' = '400 Universiteter og vitenskapelige h�gskoler'
  '401' = '401 Universiteter'
  '402' = '402 Vitenskapelige h�gskoler'
  '510' = '510 Folkeh�gskoler'
  '520' = '520 Arbeidsmarkedskurs'
  '610' = '610 Videreg�ende utdanning i utlandet'
  '620' = '620 H�yere utdanning i utlandet'
  '710' = '710 Fagskoleutdanning'
  '   ' = '    Blank'
;

  *-- kilde --*;
  value $kilde
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
   '52' = '52 Etterrapporterte fagskoler'
  ;

*--  --*;
value $komp
 '1'	= '1-Generell studiekompetanse'
 '2'	= '2-Yrkeskomp.med fag-/svennebrev'
 '3'	= '3-Yrkeskompetanse dokumentert med vitnem�l'
 '4'	= '4-Underveis til yrkeskomp.,3�r i skole f�r l�re'
 '5'	= '5-Yrkeskomp.med fag-/svennebrev,l�retid etter 3 �r i skole'
 ;

*-- kurstrin --*;
value $kurstri
  'A' = 'Ett�rig grunnkurs/Vg1'
  'D' = 'Alternativ oppl�ring/grunnkompetanse'
  'F' = 'Andre fagskoler (Lov om fagskoleutdanning tr�dte i kraft 20.06.2003)'
  'H' = 'VK I/Vg2'
  'I' = 'S�rl�p'
  'K' = 'To- eller tre�rige kurs (ikke GK over to �r)'
  'P' = 'VK II/bedriftsoppl�ring/Vg3'
  'T' = 'VK III/Bedriftsoppl�ring etter VK II/Vg3 i skole'
  'U' = 'Teknisk fagskole'
  'Z' = 'Kurs for praksiskandidater'
other = 'Uoppgitt'
;

*-- studieretning/utdanningsprogram --*;
value $studret
  '21' = '21 Allmenne, �konomiske og administrative fag'
  '22' = '22 Musikk, dans og drama'
  '23' = '23 Idrettsfag'
  '31' = '31 Helse- og sosialfag'
  '32' = '32 Naturbruk'
  '33' = '33 Formgivingsfag'
  '34' = '34 Hotell- og n�ringsmiddelfag'
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
  '60' = '60 Idrettsfag' /* Kunnskapsl�ftet */
  '61' = '61 Musikk, dans og drama' /* Kunnskapsl�ftet */
  '62' = '62 Studiespesialisering' /* Kunnskapsl�ftet */
  '63' = '63 Kunst, design og arkitektur' /* Kunnskapsl�ftet */
  '64' = '64 Medier og kommunikasjon' /* Kunnskapsl�ftet */
  '70' = '70 Bygg- og anleggsteknikk' /* Kunnskapsl�ftet */
  '71' = '71 Design og h�ndverk' /* Kunnskapsl�ftet */
  '72' = '72 Elektrofag' /* Kunnskapsl�ftet */
  '73' = '73 Helse- og oppvekstfag' /* Kunnskapsl�ftet */
  '74' = '74 Medier og kommunikasjon(gammel ordning)' /* Kunnskapsl�ftet */
  '75' = '75 Naturbruk' /* Kunnskapsl�ftet */
  '76' = '76 Restaurant- og matfag' /* Kunnskapsl�ftet */
  '77' = '77 Service og samferdsel' /* Kunnskapsl�ftet */
  '78' = '78 Teknikk og industriell produksjon' /* Kunnskapsl�ftet */
  '98' = '98 Alternativ oppl�ring' /* Kunnskapsl�ftet */
  '99' = '99 Paragraf-20-kurs med uoppgitt studieretning'
 other = '   Uten studieretning'        
;

*-- sosial bakgrunn --*;
value $sosbak
  '1' = 'Mor eller far eller begge har utd. p� niv� 7 eller 8'
  '2' = 'Mor eller far eller begge har utd. p� niv� 6'
  '3' = 'Mor eller far eller begge har utd. p� niv� 3, 4 eller 5'
  '4' = 'Mor eller far eller begge har utd. p� niv� 0, 1 eller 2'
  '9' = 'Uoppgitt, n�r begge foreldrene har uoppgitt utdanning'
other = 'Uoppgitt'
;

value $sosbakb
  '1' = 'Lang h�yere utdanning'
  '2' = 'Kort h�yere utdanning'
  '3' = 'Videreg�ende utdanning'
  '4' = 'Grunnskoleutdanning'
other = 'Uoppgitt'
;

*-- utfall resultat --*;
value $utfalla
  'A' = 'A Annulert'
  'I' = 'I Ikke best�tt'
  'B' = 'B Best�tt'
;
*-- utfall --*;
value $utfallc
  'C' = 'C Annulert'
  'D' = 'D Ikke best�tt'
  'P' = 'P Best�tt'
;
*-- utfall omkodet --*;
value $utfall
  '2' = '2 Ikke fullf�rt'
  '8' = '8 Fullf�rt'
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
  'H' = 'H H�gskolekandidat i ingeni�rfag'
  'M' = 'M Master-utdanning'
;

* -- uhgruppe + gradmerk fra NUS2000-katalog -- *;
value $uhgrmrk
  '01 ' = '01 Forberedende pr�ver'
  '02 ' = '02 Lavere niv�s utdanning'
  '03 ' = '03 Andre ett�rige studier, grunnutdanning'
  '04 ' = '04 H�gskolekandidat, to�rig,'
  '05 ' = '05 Ingeni�rutdanning, to�rig grunnutdanninger'
  '05H' = '05H H�gskolekandidat i ingeni�rfag, to�rig'
  '06 ' = '06 Andre to�rige studier, grunnutdanninger'
  '07 ' = '07 H�gskolekandidat, tre�rig'
  '08 ' = '08 Allmenn-/grunnskolel�rerutdanning'
  '08B' = '08B Bachelor, l�rerutdanning (ved Rudolf Steinerh�yskolen)'
  '09 ' = '09 F�rskolel�rer'
  '09B' = '09B Bachelor, f�rskole-/barnehagel�rerutdanning'
  '10 ' = '10 Yrkesfagl�rer'
  '10B' = '10B Bachelor, yrkesfagl�rerutdanning'
  '11 ' = '11 Ingeni�rutdanning, tre�rig'
  '11B' = '11B Bachelor, ingeni�rfag'
  '12 ' = '12 Sykepleier'
  '12B' = '12B Bachelor, sykepleierutdanning'
  '13 ' = '13 Helsefagutdanning, 3-4 �r grunnutdanning, ikke sykepleier'
  '13B' = '13B Bachelor, helsefagutdanning, ikke sykepleier'
  '14 ' = '14 H�gskolekandidat, fire�rig'
  '14B' = '14B Bachelor, h�gskolekandidat, fire�rig'
  '15 ' = '15 Etatsutdanninger'
  '16 ' = '16 Andre tre-og fire�rige grunnutdanninger (ikke h�gskolekandidat)'
  '17 ' = '17 Cand.mag.-utdanning'
  '18 ' = '18 Videreutd. i ledelse/org./adm./�konomi'
  '19 ' = '19 Videreutd. for ingeni�rer'
  '20 ' = '20 Videreutd. for sykepleiere'
  '21 ' = '21 Videreutd. for annet helsepersonell enn sykepleiere'
  '22 ' = '22 Annen videreutd. til og med to �r'
  '23 ' = '23 Praktisk-pedagogisk utdanning (PPU)'
  '24 ' = '24 Sivil�konom'
  '25B' = '25B Bachelor, allmenne fag'
  '26B' = '26B Bachelor, humanistiske og estetiske fag, ikke 4-�rig'
  '27B' = '27B Bachelor, l�rerutdanninger og utdanninger i pedagogikk, ikke allmenn-/grunnskole-, f�rskole-, fag- og yrkesfagl�rer'
  '28B' = '28B Bachelor, samfunnsfag og juridiske fag'
  '29B' = '29B Bachelor, �konomiske og administrative fag'
  '30B' = '30B Bachelor, naturvitenskapelige fag, h�ndverksfag og tekniske fag, ikke ingeni�r'
  '31 ' = '31 H�yere niv�s utdanning'
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
  '54 ' = '54 Sivil�konomutdanning,CEMS-master'
  '54M' = '54M Sivil�konom-/Master-utdanning'
  '55 ' = '55 Sivilingeni�r'
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
  '63 ' = '63 Mastergrader ved statlige h�gskoler'
  '63M' = '63M Mastergrader ved statlige h�gskoler'
  '64 ' = '64 Master of Laws'
  '64M' = '64M Master of Laws'
  '65 ' = '65 Annen utd. p� niv� 7,ikke videreutd./p�bygging'
  '66 ' = '66 Videreutdanninger/p�bygging, inntil to �r'
  '67 ' = '67 Spesialutdanning for leger og tannleger'
  '68 ' = '68 Jordmorutdanning, to �r'
  '69M' = '69M Master, ett�rig, lavere niv�'
  '70 ' = '70 Ph.d.'
  '71M' = '71M Master, allmenne fag'
  '72M' = '72M Master, humanistiske og estetiske fag'
  '73M' = '73M Master, l�rerutdanninger og utdanninger i pedagogikk'
  '74M' = '74M Master, samfunnsfag og juridiske fag, ikke rettsvitenskap'
  '75M' = '75M Master, �konomiske og administrative fag, ikke sivil�konom'
  '76M' = '76M Master, naturvitenskapelige fag, h�ndverksfag og tekniske fag, ikke sivilingeni�r/master i teknologi'
  '77M' = '77M Master, helse-, sosial- og idrettsfag, ikke farmasi og odontologi'
  '78M' = '78M Master, prim�rn�ringsfag'
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
  '96B' = '96B Bachelor, helse-, sosial- og idrettsfag, ikke sykepleier og helsefag som inng�r i UH-gruppe 13B'
  '97B' = '97B Bachelor, prim�rn�ringsfag'
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
