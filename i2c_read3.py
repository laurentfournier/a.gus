'''
    ADC 8591 0x48
    Dig 8574 0x27
'''

#!/usr/bin/env python
from libs.ABE_ADCPi import ADCPi
from libs.ABE_helpers import ABEHelpers
import datetime, time
import os, sys
import smbus

ADC = 0x48
DIG = 0x27

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)

# open the bus (0 -- original Pi, 1 -- Rev 2 Pi)
b = smbus.SMBus(1)

# make certain the pins are set high so they can be used as inputs
#b.write_byte(DIG, 0xff)
#b.write_byte_data(DIG, 0x04, 69)

while True:
    #pin1 = b.read_byte(DIG)
    #pin2 = b.read_byte_data(DIG, 0x04)
    #print "rb: %02x" % pin1
    #print "rbd: %02x" % pin2
    time.sleep(1)

    # read from 8 adc channels and print it to terminal
    print("%02f %02f %02f %02f %02f %02f %02f %02f" % (adc.read_voltage(1), adc.read_voltage(2), adc.read_voltage(3), adc.read_voltage(4), adc.read_voltage(5), adc.read_voltage(6), adc.read_voltage(7), adc.read_voltage(8)))

    # wait 1 second before reading the pins again
    #time.sleep(1)

b.close()
