# ULg's Chemical Oceanography Unit - Embedded Gaz analyser _\a.ɡus\_
> Using a Raspberry Pi 3, controlled using Kivy (touch-screen optimized), the project strive to monitor (numeral values and graphs), export data as .csv and cloud-sync those datas from multiple probes. 


## Changelog:
[**2016/11/07**]
- Main file updated
- Data processing methods
- Small bugfixes first launch script
- Licor 820/840
  - Data processing 
  - Data extraction
  
[**2016/10/24**]
- ADCPi Hat (**I²C Sensors's test'**)

[**2016/10/21**]
- Licor 820 
  - "Functionalized" the code (**main.py + *.py**)
  - Merging licor_read & licor_write (**licor_8xx_6262.py**) 

[**2016/10/20**]
- Licor 820 
  - Reading module ~~(**licor_read.py**)~~
  - Writing module ~~(**licor_write.py**)~~

[**2016/10/15**]
- First launch script (**first_launch.py**)
- Args parser (**Debugging purpose**)


### To-do:
- Licor 840/6262
  - Data structures (**licor_8xx_6262.py**)
- Licor 820/840/6262
  - Models switch (**licor_8xx_6262.py**)
- I²C 
  - Communication protocol
  - Sensors data retrieving
- GUI (**Kivy**)


#### Further in time:
- Android API

#####  Having questions? Feel free to [contact me](mailto://mail@laurent-fournier.be) and i’ll gladly help you out.
