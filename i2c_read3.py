#!/usr/bin/env python
import smbus
import time

# open the bus (0 -- original Pi, 1 -- Rev 2 Pi)
b = smbus.SMBus(1)

# make certain the pins are set high so they can be used as inputs
b.write_byte(0x25, 0xff)
#b.write_byte_data(0x25, 0x04, 69)

while True:
    pin1 = b.read_byte(0x25)
    #pin2 = b.read_byte_data(0x25, 0x04)
    print "rb: %02x" % pin1
    #print "rbd: %02x" % pin2
    time.sleep(1)

b.close()
