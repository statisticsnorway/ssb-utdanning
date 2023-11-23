OPTIONS NOSOURCE;
*--------------------- NB! ** Kjør med SUBMIT!! ** -----------------------------*;
*********************************************************************************;
* Prosjekt...........: X:\360\Fellesprogrammer\Formater\                         
* Programnavn........: a01_ISCED97_siffer
*-------------------------------------------------------------------------------*;
* Skrevet når/av.....: 18.01.2008 - Geir Nygård
* Beskrivelse........: Lager formater for ISCED-97 koden (4 posisjoner)
*					   NB! ** Formatnavn må være maks. 8 pos. (inkl. $)
*-------------------------------------------------------------------------------*:
*	formatnavn - innhold                                                        *;
*-------------------------------------------------------------------------------*;
*	$level	1.		siffer i ISCED-97 koden
*	$field	2.		siffer i ISCED-97 koden
*	$nfield	2. - 3. siffer i ISCED-97 koden
*	$dfield 2. - 4. siffer i ISCED-97 koden
*********************************************************************************;

RSUBMIT;
libname library '$UTD/kat/formater';
run;
proc format library = library;

value $level 	/*1. siffer i ISCED-koden*/
	'0' = 'Pre-primary education'
	'1' = 'Primary education or first stage of basic education'
	'2' = 'Lower secondary or second stage of basic education'
	'3' = 'Upper secondary education'
	'4' = 'Post-secondary non-tertiary education'
	'5' = 'First stage of tertiary education'
	'6' = 'Second stage of tertiary education'

	'9' = 'Not specified' /*Ikke et opprinnelig nivå i ISCED*/
;

value $field	/*2. siffer i ISCED-koden*/
	'0' = 'General programmes'
	'1' = 'Education'
	'2' = 'Humanities and Arts'
	'3' = 'Social Sciences, Business and Law'
	'4' = 'Science, Mathematics and Computing'
	'5' = 'Engineering, Manufacturing and Construction'
	'6' = 'Agriculture and Veterinary'
	'7' = 'Health and Welfare'
	'8' = 'Services'
	'9' = 'Unknown'
;

value $nfield	/*2.+ 3. siffer i ISCED-koden*/
	'01' = 'Basic programmes'
	'08' = 'Literacy and numeracy'
	'09' = 'Personal development'
	'14' = 'Teacher training and education science'
	'21' = 'Arts'
	'22' = 'Humanities'
	'31' = 'Social and behavioural science'
	'32' = 'Journalism and information'
	'34' = 'Business and administration'
	'38' = 'Law'
	'42' = 'Life science'
	'44' = 'Physical science'
	'46' = 'Mathematics and statistics'
	'48' = 'Computing'
	'52' = 'Engineering and engineering trades'
	'54' = 'Manufacturing and processing'
	'58' = 'Archtitecture and building'
	'62' = 'Agriculture, forestry and fishery'
	'64' = 'Veterinary'
	'72' = 'Health'
	'76' = 'Social science'
	'81' = 'Personal services'
	'84' = 'Transport services'
	'85' = 'Environmental protection'
	'86' = 'Security services'
	'99' = 'Fields of education not known or unspecified'
;

value $dfield	/*2. - 4. siffer i ISCED-koden*/
	'010' = 'Basic/broad general programmes'
	'080' = 'Literacy and numeracy'
	'090' = 'Personal skills'
	'099' = 'Personal skills, unspecified'
	'140' = 'Teacher training and education science (broad programmes)' 
	'142' = 'Education science'
	'143' = 'Training for pre-school teachers'
	'144' = 'Training for teachers at basic levels'
	'145' = 'Training for teachers with subject specialisation'
	'146' = 'Training for teachers of vocational subjects'
	'210' = 'Arts (broad programmes)'
	'211' = 'Fine arts'
	'212' = 'Music and performing arts'
	'213' = 'Audio-visual techniques and media production'
	'214' = 'Design'
	'215' = 'Craft skills'
	'219' = 'Arts, unspecified'
	'220' = 'Humanities (broad programmes)'
	'221' = 'Religion'
	'222' = 'Foreign languages'
	'223' = 'Mother tongue'
	'224' = 'Numismatics'
	'225' = 'History and archaeology'
	'226' = 'Philosophy and ethics'
	'229' = 'Humanities, unspecified' 
	'299' = 'Humanities and Arts, unspecified'
	'310' = 'Social and behavioural science (broad programmes)'
	'311' = 'Psychology'
	'312' = 'Sociology and cultural studies'
	'313' = 'Political science and civics'
	'314' = 'Economics'
	'321' = 'Journalism and reporting'
	'322' = 'Library, information, archive'
	'340' = 'Business and administration (broad programmes)'
	'341' = 'Wholesale and retail sales'
	'342' = 'Marketing and advertising'
	'343' = 'Finance, banking, insurance'
	'344' = 'Accounting and taxation'
	'345' = 'Management and administration'
	'346' = 'Secreterial and office work'
	'347' = 'Working life'
	'380' = 'Law'
	'399' = 'Social sciences, Business and Law, unspecified'
	'421' = 'Biology and biochemistry'
	'422' = 'Environmental science' 
	'441' = 'Physics'
	'442' = 'Chemistry'
	'443' = 'Earth science'
	'449' = 'Physical science, unspecified' 
	'461' = 'Mathematics'
	'462' = 'Statistics' 
	'481' = 'Computer science'
	'482' = 'Computer use'
	'499' = 'Science, Mathematics and Computing, unspecified'
	'520' = 'Engineering and engineering trades (broad programmes)'
	'521' = 'Mechanics and metal work'
	'522' = 'Electricity and energy'
	'523' = 'Electronics and automation'
	'524' = 'Chemical and process'
	'525' = 'Motor vehicles, ships and aircraft'
	'529' = 'Engineering and engineering trades, unspecfied'  
	'540' = 'Manufacturing and processing (broad programmes)'
	'541' = 'Food processing'
	'542' = 'Textile, clothes, fottwear, leather'
	'543' = 'Materials (wood, paper, plastic, glass)'
	'544' = 'Mining and extraction'
	'581' = 'Archtitecture and town planning'
	'582' = 'Building and civil engineering' 
	'599' = 'Engineering, Manufacturing and Construction, unspecified'
	'620' = 'Agriculture, forestry and fishery (broad programmes)'
	'621' = 'Crop and livestock production'
	'622' = 'Horticulture'
	'623' = 'Forestry'
	'624' = 'Fisheries'
	'640' = 'Veterinary' 
	'641' = 'Veterinary science'
	'720' = 'Health (broad programmes)'
	'721' = 'Medicine'
	'723' = 'Nursing and caring'
	'724' = 'Dental studies'
	'725' = 'Medical diagnostic and treatment technology'
	'726' = 'Therapy and rehabilitation'
	'727' = 'Pharmacy'
	'761' = 'Child care and youth services'
	'762' = 'Social work and counselling'
	'799' = 'Health and Welfare, unspecified'
	'810' = 'Personal services (broad programmes)'
	'811' = 'Hotel, restaurant and catering'
	'812' = 'Travel, tourism and leisure'
	'813' = 'Sports'
	'814' = 'Domestic services'
	'815' = 'Hair and beaty services'
	'840' = 'Transports services (broad programmes'
	'850' = 'Environmental protection (broad programme)'
	'851' = 'Environmental protection technology'
	'852' = 'Natural environments and wildlife'
	'853' = 'Community sanitation services'
	'860' = 'Security services (broad programmes)'
	'861' = 'Protection of persons and property'
	'862' = 'Occupational health and safety'
	'863' = 'Military and defence'
	'899' = 'Services, unspecified'
	'999' = 'Unspecified'
	;

run;
ENDRSUBMIT;
