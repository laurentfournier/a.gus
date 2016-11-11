# ULg's Chemical Oceanography Unit - Embedded Gaz analyser _\a.ɡus\_
> Using a Raspberry Pi 3, controlled using Kivy (touch-screen optimized), the project strive to monitor (numeral values and graphs), export data as .csv and cloud-sync those datas from multiple probes. 

## Changelog:
[**2016/11/10**]
- Moved concerned files to **/config/** and **/libs/** instead of project's root 
- Minor adds to Makefile 
- I²C reading tests
##  
[**2016/11/07**]
- Main file updated
- Data processing methods (**file_manager.py**)
- Small bugfixes (**~~first_launch.py~~ -> Makefile**)
- Licor 820/840
  - Data processing 
  - Data extraction
##  
[**2016/10/24**]
- ADCPi Hat (**i2c_read.py**)
##
[**2016/10/21**]
- Licor 820 
  - "Functionalized" the code (**main.py + *.py**)
  - Merging licor_read & licor_write (**~~licor_*.py~~ -> licor_8xx_6262.py**) 
##
[**2016/10/20**]
- Licor 820 
  - Reading module ~~(**licor_read.py**)~~
  - Writing module ~~(**licor_write.py**)~~
##
[**2016/10/15**]
- First launch script (**~~first_launch.py~~**)
- Args parser (**Debugging purpose**)
##
## To-do:
- Licor 840/6262/7000
  - Data structures
- Licor 820/840/6262/7000
  - Models switch
- I²C 
  - Communication protocol
  - Sensors data retrieving
- X GUI (**Kivy**)
- Term GUI (**Curves**)

## Further in time:
- Cloud backup
- Android API
##
#####  Having questions? Feel free to [contact me](mailto://mail@laurent-fournier.be) and i’ll gladly help you out.
