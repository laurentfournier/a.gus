# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

import os, sys, subprocess
import datetime
import argparse

from multiprocessing import Process, Queue, Pipe
from threading       import Timer

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
parser.add_argument('-c', '--continuous', type=bool, help='No outputs limitation', default=True,  choices=[True, False])
parser.add_argument('-C', '--config',     type=bool, help='Configuration mode',    default=False, choices=[True, False])
parser.add_argument('-d', '--debug',      type=bool, help='Debugging mode',        default=True, choices=[True, False])
parser.add_argument('-l', '--loops',      type=int,  help='Number of outputs',     default=5)
parser.add_argument('-L', '--logging',    type=bool, help='Storing in .CSV files', default=False, choices=[True, False])
parser.add_argument('-m', '--model',      type=int,  help='Select device model',   default=6262,  choices=[820, 840, 6262, 7000])
args = parser.parse_args()

  ############
  # Settings #
  ############

CONFIG     = args.config
CONTINUOUS = args.continuous
DEBUG      = args.debug
DEVICE     = args.model
LOG        = args.logging
LOOPS      = args.loops             # Nr of data extractions

FREQ    = 5
PORT0   = '/dev/ttyUSB0'
PORT1   = '/dev/ttyUSB1'
PORT2   = '/dev/ttyUSB2'
PORT3   = '/dev/ttyUSB3'
PORT4   = '/dev/ttyUSB4'
PORT5   = '/dev/ttyUSB5'
PORT6   = '/dev/ttyUSB6'
PORT7   = '/dev/ttyUSB7'
BAUD    = 9600
PARITY  = 'N'
STOPBIT = 1
BYTE_SZ = 8
TIMEOUT = 5.0

args_list  = { 'port' : PORT0,   'baud': BAUD,             'timeout': TIMEOUT,
               'config': CONFIG, 'continuous': CONTINUOUS, 'debug': DEBUG,
               'device': DEVICE, 'log': LOG,               'loops': LOOPS }

q_in  = Queue()
q_out = Queue()

#data     = 0.0
#cnt      = 0
exitFlag = 0

#probe      = []
o_id       = -1
li8xStatus = 0
li6xStatus = 0
i2cStatus  = 0

#-------------------------------------------------------------
#----------------------- Main program ------------------------
#-------------------------------------------------------------
if __name__ == '__main__':
    os.system('clear')
    while not exitFlag:
        if (li8xStatus is True): print ("Li820:  Active")
        else:                    print ("Li820:  Inactive")

        if (li6xStatus is True): print ("Li6262: Active")
        else:                    print ("Li6262: Inactive")

        if (i2cStatus  is True): print ("I2C:    Active")
        else:                    print ("I2C:    Inactive")
        
        print ("_______________________________________________________________\n")

        user_input = raw_input("\t|-----------------|\n"
                               "\t| 0. Refresh      |\n"
                               "\t| --------------- |\n"
                               "\t| 1. Licor 820    |\n"
                               "\t| 2. Licor 6262   |\n"
                               "\t| 3. I2C          |\n"
                               "\t| --------------- |\n"
                               "\t| Q. Exit Program |\n"
                               "\t|-----------------|\n")
        os.system('clear')

        if   user_input is '0': pass

        elif user_input is '1':
            args_list['port'] = PORT0
            args_list['device'] = 820
            o_id += 1
            o_id0 = o_id

            Li820 = lm.logManager(queue=(q_in, q_out), kwargs=(args_list))
            
            if not li8xStatus: li8xStatus = 1; Li820.start(); Li820.read(mode='logger')
            else:              li8xStatus = 0; Li820.stop()

        elif user_input is '2':
            args_list['port'] = PORT1
            args_list['device'] = 6262
            o_id += 1
            o_id1 = o_id

            Li6262 = lm.logManager(queue=(q_in, q_out), kwargs=(args_list))

            if not li6xStatus: li6xStatus = 1; Li6262.start(); Li6262.read(mode='logger')
            else:              li6xStatus = 0; Li6262.stop()

        elif user_input is '3':
            args_list['port'] = I2C0
            args_list['device'] = I2C
            o_id += 1
            o_id2 = o_id

        elif user_input is 'q' or 'Q':
            if (li8xStatus): Li820.stop()
            if (li6xStatus): Li6262.stop()
            exitFlag = 1

        else: pass

