from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
from smbus import SMBus
from itertools import cycle
from time import sleep

import datetime
import os, sys

LED1 = 0x01
LED2 = 0x02
LED3 = 0x04
LED4 = 0x08
LED5 = 0x10
LED6 = 0x20
LED7 = 0x40
LED8 = 0x80

PATTERN = (LED1, LED2, LED3, LED4, LED5, LED6, LED7, LED8)

bus = SMBus(1)

while True:
    for LED in cycle(PATTERN):
        bus.write_byte(0x25, LED)
        sleep(0.1)
