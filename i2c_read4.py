#!/usr/bin/env python
'''
    ADC 8591 0x48
    Dig 8574 0x27
'''

from libs.ABE_ADCPi import ADCPi
from libs.ABE_helpers import ABEHelpers
import datetime, time
import os, sys
import smbus

ADC = 0x48
DIG = 0x27

b = smbus.SMBus(1)

aTest = 0
bTest = b'00000000'

inc = 0
i = 0
j = 0

while True:
    aTest = bin(0 + inc)[2:].zfill(8)
    b.write_byte(ADC, int(aTest))
    reading = b.read_byte(ADC)
    print ("ADC{} : Value {} - Read {}").format(inc, aTest, str(reading))
   
    inc += 1
    if (inc > 3): inc = 0
    
    time.sleep(1)

b.close()
