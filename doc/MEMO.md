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

				Li6262 Cfg

*01  4.0000E+00, 1.0000E+00, 1.3998E-01, 1.0207E-05, 6.4168E-09,-6.7441E-13, 4.1861E-17, 0.0000E+00,2
*02  3.6720E+01, 1.5048E+04, 6.2200E-03, 2.7736E-06, 2.6441E-11, 0.0000E+00, 0.0000E+00, 1.0000E+00
*05 22, 0.0000E+00, 1.0000E+03                                                                   
*06 22, 3.5000E+02, 5.1000E+02                                                                   
*07 1                                                                                            
*08 1, 0.0000E+00, 1.0000E+00                                                                    
*08 2, 0.0000E+00, 1.0000E+00                                                                    
*09 0,1,1                                                                                        
*1322,43,32,38,42                                                                                
*15 0                                                                                            
*71  5.9123E+01                                                                                  
*72  1.5300E-02                                                                                  
*73 43                                                                                           
*74 5                                                                                            
*75  0.0000E+00                                                                                  
*76 2                                                                                            
*77  0.0000E+00                                                                                  
*78  1.5000E+00
*91 22,43
*92 32,38
*93 22,38
*94 21,31
*95 22,46
*96 22,42
*97 22,45
*98 21,42
*99 21,31

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

Traceback (most recent call last):
  File "main.py", line 222, in <module>
Process Process-1:
Process Process-2:
    Traceback (most recent call last):
user_input = raw_input("\t|-----------------|\n"
Traceback (most recent call last):
  File "/usr/lib/python2.7/multiprocessing/process.py", line 258, in _bootstrap
  File "/usr/lib/python2.7/multiprocessing/process.py", line 258, in _bootstrap
KeyboardInterrupt
    self.run()
    self.run()
  File "/usr/lib/python2.7/multiprocessing/process.py", line 114, in run
  File "/usr/lib/python2.7/multiprocessing/process.py", line 114, in run
    self._target(*self._args, **self._kwargs)
    self._target(*self._args, **self._kwargs)
  File "main.py", line 156, in licor
  File "main.py", line 156, in licor
    data = probe.read()
    data = probe.read()
  File "/home/pi/a.gus/licor_8xx.py", line 89, in read
  File "/home/pi/a.gus/licor_6xx.py", line 79, in read
    raw = self.con.readline()
    raw = bs(self.con.readline(), 'lxml')
  File "/usr/lib/python2.7/dist-packages/serial/serialposix.py", line 446, in read
  File "/usr/lib/python2.7/dist-packages/serial/serialposix.py", line 446, in read
    ready,_,_ = select.select([self.fd],[],[], self._timeout)
    ready,_,_ = select.select([self.fd],[],[], self._timeout)
KeyboardInterrupt
KeyboardInterrupt

```
