from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import datetime, time
import os, sys

"""
================================================
ABElectronics ADC Pi 8-Channel ADC data-logger demo
Version 1.0 Created 11/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed
run with: python demo-read_voltage.py
================================================

Initialise the ADC device using the default addresses and sample rate, change
this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""


i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)


while True:
    # read from 8 adc channels and print it to terminal
    print("%02f %02f %02f %02f %02f %02f %02f %02f" % (adc.read_voltage(1), adc.read_voltage(2), adc.read_voltage(3), adc.read_voltage(4), adc.read_voltage(5), adc.read_voltage(6), adc.read_voltage(7), adc.read_voltage(8)))

    # wait 1 second before reading the pins again
    #time.sleep(1)
