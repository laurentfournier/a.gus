#!/usr/bin/env python
'''
    
'''
import datetime, time
import os, sys
import smbus

ADC = 0x48

aTest = 0x40
bTest = 0x00
i = 0

bus = smbus.SMBus(1)

while True:
    bus.write_byte_data(ADC, int(aTest), i)
    reading = bus.read_byte(ADC)
    
    print ("Read byte: {} - Write byte: {} - Value: {}").format(hex(reading), hex(aTest), hex(i))
   
    i += 10
    if (i > 250): i = 0
    
    time.sleep(0.5)
bus.close()
