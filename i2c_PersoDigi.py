#!/usr/bin/env python
'''
    
'''
import datetime, time
import os, sys
import smbus

DIG = 0x27

aTest = 0x00
i = 0

bus = smbus.SMBus(1)

while True:
    bus.write_byte(DIG, aTest)
    
    reading = bus.read_byte(DIG)
    print ("Read byte: {}").format(hex(reading))

    if i == 0:
        i = 1
        aTest = 0xFF

    else:
        i = 0
        aTest = 0x00
        
    time.sleep(0.5)
bus.close()
