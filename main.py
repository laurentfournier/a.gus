# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse

from multiprocessing import Process, Queue, Pipe
from threading       import Timer

import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

from bs4         import BeautifulSoup as bs
from lxml        import etree
from collections import Counter

# External libraries
import file_manager as fm
from licor_6xx import Licor6xx
from licor_7xx import Licor7xx
from licor_8xx import Licor8xx
'''
# GUI
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.uix.button import Button
from kivy.uix.widget import Widget'''

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Terminal #
  ############

parser = argparse.ArgumentParser(description = '')
parser.add_argument('-c', '--continuous', type=bool, help='No outputs limitation', default=True,  choices=[True, False])
parser.add_argument('-C', '--config',     type=bool, help='Configuration mode',    default=False, choices=[True, False])
parser.add_argument('-d', '--debug',      type=bool, help='Debugging mode',        default=False, choices=[True, False])
parser.add_argument('-l', '--loops',      type=int,  help='Number of outputs',     default=5)
parser.add_argument('-L', '--logging',    type=bool, help='Storing in .CSV files', default=True,  choices=[True, False])
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
BAUD    = 9600
PARITY  = 'N'
STOPBIT = 1
BYTE_SZ = 8
TIMEOUT = 5.0
LOG_DIR = 'logs/'

args_list  = { 'port' : PORT0,   'baud': BAUD,             'timeout': TIMEOUT,
               'config': CONFIG, 'continuous': CONTINUOUS, 'debug': DEBUG,
               'device': DEVICE, 'log': LOG,               'loops': LOOPS }

#q_in, q_out = Queue()
p_in6, p_out6        = Pipe()
p_in8, p_out8        = Pipe()
p_header6, p_header8 = Pipe()

data     = 0.0
cnt      = 0
exitFlag = 0

probe      = []
t_buffer   = {}
t_id       = -1
li8xStatus = 0
li8xValue  = 0
li6xStatus = 0
li6xValue  = 0
i2cStatus  = 0
i2cValue   = 0

#-------------------------------------------------------------
#----------------- Tests for Licor sensors -------------------
#-------------------------------------------------------------
def licor(ident, pipe, headers, **kwargs):
    config     = kwargs['config']
    continuous = kwargs['continuous']
    debug      = kwargs['debug']
    log        = kwargs['log']
    loops      = kwargs['loops']
    device     = kwargs['device']
    
    pid = kwargs['pid'] = os.getpid
    
    p_in6, p_in8, p_out6, p_out8 = pipe
    p_header6, p_header8         = headers
    
    # Connect to device
    try:
        global probe
        global t_buffer
        global t_id

        if   device == 820 or device == 840: probe = Licor8xx((p_in8, p_out8), p_header8, **kwargs)
        elif device == 6262:                 probe = Licor6xx((p_in6, p_out6), p_header6, **kwargs)
        #elif device == 7000:                 probe = Licor7xx((p_in7, p_out7), **kwargs)

        probe.connect()

    except Exception as e:
        if debug: print ("ERROR: {}".format(e))
        sys.exit("Could not connect to the device")

      ###################
      # Writing routine #
      ###################
    # Configure the device if required
    if config:
        try:
            #probe.config_R()
            probe.config_W()

        except Exception as e:
            if debug: print ("ERROR: {}".format(e))
            sys.exit("Could not connect to the device")

      ###################
      # Reading routine #
      ###################
    date_time = datetime.datetime.now()
    pathname = '{}licor{}/'.format(LOG_DIR, device)
    filename = '{}licor{}-data-{}.csv'.format(pathname, device, date_time)

    # Verify if directory already exists
    if not os.path.isdir(pathname):
        os.system('mkdir {}'.format(pathname))

    # If logging is enabled
    if log:
        with open(filename, 'w') as fp:
            # Write headers
            fp.write(';'.join(probe._header))
            fp.write('\n')

            while loops:
                data = probe.read()
                #if (datetime.datetime.now().strftime("%S") == "00"):
                try:
                    # Read from device
                    buff = data = probe.read()
                    p_out.send(buff)
                    
                    # Write data
                    fp.write(';'.join(data))
                    fp.write('\n')

                    # Do only once per minute
                    #while (datetime.datetime.now().strftime("%S") == "00"):
                    #    pass

                except Exception as e:
                    if debug: print ("ERROR: {}".format(e))

                # CTRL+C catcher - Not working
                except KeyboardInterrupt:
                    sys.exit("Program terminated properly")

                if not continuous: loops -= 1

            fp.close()

    # If logging is Disabled
    else:
        while loops:
            if (datetime.datetime.now().strftime("%S") == "00"):
                try:
                    # Read from device
                    data = probe.read()
                    p_out.send(data)

                    # Do only once per minute
                    while (datetime.datetime.now().strftime("%S") == "00"):
                        pass

                except Exception as e:
                    if debug: print ("ERROR: {}".format(e))

                # CTRL+C catcher - Not working
                except KeyboardInterrupt:
                    sys.exit("Program terminated properly")

            if not continuous: loops -= 1

#-------------------------------------------------------------
#----------------------- Main program ------------------------
#-------------------------------------------------------------
if __name__ == '__main__':
    os.system('clear')
    while not exitFlag:
        if (li8xStatus == True): print ("Li820:  {}").format(p_in8.recv())
        else: print ("Li820:  Inactive")

        if (li6xStatus == True): print ("Li6262: {}").format(p_in6.recv())
        else: print ("Li6262: Inactive")

        if (i2cStatus  == True): print "I2C:    Active" #(("I2C:    {}").format(probe.get_data())
        else: print ("I2C:    Inactive")
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
            args_list['port'] = PORT1
            args_list['device'] = 820
            t_id += 1
            t_id0 = t_id

            a = Process(target=licor, args=(str(t_id0), (p_in6, p_in8, p_out6, p_out8), (p_header6, p_header8)), kwargs=args_list)
            
            if not li8xStatus: li8xStatus = 1; a.start()
            else:              li8xStatus = 0; os.sytem('kill -9 {}'.format(kwargs['pid8']))

        elif user_input is '2':
            args_list['port'] = PORT0
            args_list['device'] = 6262
            t_id += 1
            t_id1 = t_id

            b = Process(target=licor, args=(str(t_id1), (p_in6, p_in8, p_out6, p_out8), (p_header6, p_header8)), kwargs=args_list)
            
            if not li6xStatus: li6xStatus = 1; b.start()
            else:              li6xStatus = 0; os.sytem('kill -9 {}'.format(kwargs['pid6']))

        elif user_input is '3':
            i2cStatus = 1
            cnt += 1
            args_list['id'] = cnt3 = cnt
            todo

        elif user_input is 'q' or 'Q':
            exitFlag = 1

        else: pass

#-------------------------------------------------------------
#-------------------------- Sample ---------------------------
#-------------------------------------------------------------
'''# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue, **args_list)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()

for word in nameList:
    workQueue.put(word)

queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()

print "Exiting Main Thread"
'''
