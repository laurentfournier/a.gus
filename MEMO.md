```
To-do:
Main	
 Multi-threading

1st	
 Makefile
 -+ config.txt
 - sonic-pi
 - wolfram
 + deps
 + rpi-upgrade
 + log dir
 + cfg dir

I²C
 Reading routine

GUI
 Terminal
 Visual
	
Backup
 Offline
 Cloud-based ?

Check:
Serialisation (no ascii..?)

Priorité:
 température
 pH
 turbidité
 Makefile
 gui
 lan
 smartphone

-----------------------------------------------------------------------------
-----------------------------------------------------------------------------

µSpir:
temperature ~20-50 - failsafe 38
pH ~7.5-11.5 - failsafe 11
luminosité
co2
conductivité

-----------------------------------------------------------------------------
-----------------------------------------------------------------------------

				Li820 Grammar

{val | val |...} 	| = or .
{bool} 			Boolean values
{float} 		Floating point values in decimal or exponential notation
{int} 			Integers
{iso date} 		4 digit year - 2 digit month - 2 digit day

<LI820>
 	<ACK>{bool}</ACK>
 	<VER>{string}</VER>
 	<DATA>
 		<CO2>{float}</CO2>
 		<CO2ABS>{float}</CO2ABS>
		<CELLTEMP>{float}</CELLTEMP>
 		<CELLPRES>{float}</CELLPRES>
 		<IVOLT>{float}</IVOLT>
 		<RAW>{integer}</RAW>
 	</DATA>
 	<RS232>
 		<CO2>{bool}</CO2>
 		<CO2ABS>{bool}</CO2ABS>
 		<CELLTEMP>{bool}</CELLTEMP>
 		<CELLPRES>{bool}</CELLPRES>
 		<IVOLT>{bool}</IVOLT>
 		<STRIP>{bool}</STRIP>
 		<ECHO>{bool}</ECHO>
 		<RAW>{bool}</RAW>
 	</RS232>
 	<CFG>
 		<OUTRATE>{float}</OUTRATE>
 		<HEATER>{bool}</HEATER>
 		<PCOMP>{bool}</PCOMP>
 		<FILTER>{int}</FILTER>
 		<ALARMS>
 			<ENABLED>{bool}</ENABLED>
 			<HIGH>{int}</HIGH>
 			<HDEAD>{int}</HDEAD>
 			<LOW>{int}</LOW>
 			<LDEAD>{int}</LDEAD>
 		</ALARMS>
 		<BENCH>{5|14}</BENCH>
 		<DACS> 
			<RANGE>{2.5 | 5.0}</RANGE>
 			<D1>{NONE | CO2 | CELLTEMP | CELLPRES}</D1>
 			<D1_0>{float}</D1_0>
			<D1_F>{float}</D1_F>
 			<D2>{NONE | CO2 | CELLTEMP | CELLPRES}</D2>
 			<D2_0>{float}</D2_0>
			<D2_F>{float}</D2_F>
 		</DACS>
 	</CFG>
 	<CAL>
 		<DATE>{iso date}</DATE>
 		<CO2ZERO>{bool}</CO2ZERO>
 		<CO2SPAN>{int}</CO2SPAN>
 		<CO2SPAN_A>{int}</CO2SPAN_A>
		<CO2SPAN_B>{int}</CO2SPAN_B>
 		<CO2LASTZERO>{iso date}</CO2LASTZERO>
 		<CO2LASTSPAN>{iso date}</CO2LASTSPAN>
 	</CAL>
 	<ERROR>{string}</ERROR>
</LI820> 

-----------------------------------------------------------------------------
-----------------------------------------------------------------------------


```
