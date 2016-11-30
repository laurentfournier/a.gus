#!/usr/bin/env python
'''
    
'''

import datetime, time
import os, sys
import smbus

ADC = 0x48
DIG = 0x27

b = smbus.SMBus(1)

aTest = 0
bTest = 0x00

i = 3
j = 0

while True:
    aTest = bin(bTest + j)[2:].zfill(8)
    b.write_byte(ADC, int(aTest))
    reading = b.read_byte(ADC)
    print ("ADC{} : Value {} - Read {}").format(i, aTest, str(reading))
   
    i += 1
    j += 1
    if (i > 3): i = 0
    if (j > 3): j = 0
    
    time.sleep(1)

b.close()
