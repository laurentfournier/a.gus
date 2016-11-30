from libs.ABE_ADCPi import ADCPi
from libs.ABE_helpers import ABEHelpers
import datetime, time
import os, sys

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)


while True:
    # read from 8 adc channels and print it to terminal
    print("%02f %02f %02f %02f %02f %02f %02f %02f" % (adc.read_voltage(1), adc.read_voltage(2), adc.read_voltage(3), adc.read_voltage(4), adc.read_voltage(5), adc.read_voltage(6), adc.read_voltage(7), adc.read_voltage(8)))

    # wait 1 second before reading the pins again
    time.sleep(0.5)
