# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

import os, sys, datetime, argparse
from copy import deepcopy

from multiprocessing import Process
from threading       import Timer, Thread#, Queue, Pipe
from Queue           import Queue
import subprocess

import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

# External libraries
import log_manager as lm

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Terminal #
  ############

parser = argparse.ArgumentParser(description = '')
parser.add_argument('-d', '--debug', type=bool, help='Stderr outputs', default=False, choices=[True])
args = parser.parse_args()

  ############
  # Settings #
  ############

DEBUG   = args.debug
CONFIG  = False
BAUD    = 9600
TIMEOUT = 5.0

PORT   = [ '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3',
           '0x64',         '0x65' ]

DEVICE = [ '820',          '840',          '6262',         '7000',
           'i2c1',         'i2c2' ]

args_device = { 'port' : PORT[0], 'baud': BAUD,   'timeout': TIMEOUT,
                'config': CONFIG, 'device': DEVICE[0] }

q_data   = Queue()
q_header = Queue()
devices   = []

exitFlag  =  False
li8xFlag  =  False
li6xFlag  =  False
i2cFlag   =  False
probeCnt  = -1

#-------------------------------------------------------------
#----------------------- Main program ------------------------
#-------------------------------------------------------------
if __name__ == '__main__':
    os.system('clear')

    while not exitFlag:
        if (li8xFlag is True): print ("Li820:  Active")
        else:                  print ("Li820:  Inactive")

        if (li6xFlag is True): print ("Li6262: Active")
        else:                  print ("Li6262: Inactive")

        if (i2cFlag  is True): print ("I2C:    Active")
        else:                  print ("I2C:    Inactive")

        print ("____________________________________________________________\n")

        user_input = raw_input("\t|-----------------|\n"
                               "\t| 0. Execute      |\n"
                               "\t| --------------- |\n"
                               "\t| 1. Licor 820    |\n"
                               "\t| 2. Licor 6262   |\n"
                               "\t| 3. I2C          |\n"
                               "\t| --------------- |\n"
                               "\t| Q. Exit Program |\n"
                               "\t|-----------------|\n")
        os.system('clear')

        if user_input is '0':
            logger = lm.logManager((q_data, q_header), devices, DEBUG)
            logger.start()

        elif user_input is '1':
            probeCnt += 1
            args_device['id']     = probeCnt
            args_device['name']   = 'Licor820'
            args_device['port']   = PORT[0]
            args_device['device'] = DEVICE[0]
            
            devices.append(deepcopy(args_device))

            if not li8xFlag: li8xFlag = True
            else:            li8xFlag = False

        elif user_input is '2':
            probeCnt += 1
            args_device['id']     = probeCnt
            args_device['name']   = 'Licor6262'
            args_device['port']   = PORT[1]
            args_device['device'] = DEVICE[2]
            
            devices.append(deepcopy(args_device))

            if not li6xFlag: li6xFlag = True
            else:            li6xFlag = False

        elif user_input is '3':
            probeCnt += 1
            args_device['id']     = probeCnt
            args_device['name']   = 'I2C'
            args_device['port']   = PORT[4]
            args_device['device'] = DEVICE[4]
            
            devices.append(deepcopy(args_device))

            if not i2cFlag: i2cFlag = True
            else:           i2cFlag = False

        elif user_input is 'q' or 'Q':
            logger.stop()
            exitFlag = True

        else: pass
