# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse

from multiprocessing import Process, Queue

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
LOOPS      = args.loops                                                                 # Nr of data extractions

FREQ    = 5
PORT    = '/dev/ttyUSB0'
BAUD    = 9600
PARITY  = 'N'
STOPBIT = 1
BYTE_SZ = 8
TIMEOUT = 5.0
LOG_DIR = 'logs/'

args_list  = { 'port' : PORT,    'baud': BAUD,             'timeout': TIMEOUT,
               'config': CONFIG, 'continuous': CONTINUOUS, 'debug': DEBUG,
               'device': DEVICE, 'log': LOG,               'loops': LOOPS }

data     = 0.0
cnt      = 0
exitFlag = 0

probe      = []
t_buffer   = []
li8xStatus = 0
li8xValue  = 0
li6xStatus = 0
li6xValue  = 0
i2cStatus  = 0
i2cValue   = 0

#-------------------------------------------------------------
#----------------- Tests for Licor sensors -------------------
#-------------------------------------------------------------
def licor(**kwargs):
    config     = kwargs['config']
    continuous = kwargs['continuous']
    debug      = kwargs['debug']
    log        = kwargs['log']
    loops      = kwargs['loops']
    device     = kwargs['device']
    ids        = kwargs['id']
    
    try:                                                                                # Connect to device
        global probe
        
        if   device == 820 or device == 840: probe.append(Licor8xx(**kwargs))
        elif device == 6262:                 probe.append(Licor6xx(**kwargs))
        elif device == 7000:                 probe.append(Licor7xx(**kwargs))
        
        probe[ids].connect()

    except Exception as e:
        if debug: print ("ERROR: {}".format(e))
        sys.exit("Could not connect to the device")

      ###################
      # Writing routine #
      ###################
    if config:                                                                          # Configure the device if required
        try:
            #probe[cnt].config_R()
            probe[cnt].config_W()

        except Exception as e:
            if debug: print ("ERROR: {}".format(e))
            sys.exit("Could not connect to the device")

      ###################
      # Reading routine #
      ###################
    global t_buffer
    date_time = datetime.datetime.now()
    pathname = '{}licor{}/'.format(LOG_DIR, device)
    filename = '{}licor{}-data-{}.csv'.format(pathname, device, date_time)
    
    if not os.path.isdir(pathname):                                                     # Verify if directory already exists
        os.system('mkdir {}'.format(pathname))

    if log:                                                                             # If logging is enabled
        with open(filename, 'w') as fp:
            fp.write(';'.join(probe[ids]._header))                                      # Write headers
            fp.write('\n')

            while loops:
                if (datetime.datetime.now().strftime("%S") == "00"):
                    try:
                        data = probe[ids].read()                                        # Read from device
                        fp.write(';'.join(data))                                        # Write data
                        fp.write('\n')
                        t_buffer[0] = data
                        
                        while (datetime.datetime.now().strftime("%S") == "00"):
                            pass

                    except Exception as e:
                        if debug: print ("ERROR: {}".format(e))

                    except KeyboardInterrupt:                                           # CTRL+C catcher - Not working
                        sys.exit("Program terminated properly")

                if not continuous: loops -= 1

            fp.close()

    else:                                                                               # If logging is Disabled
        while loops:
            if (datetime.datetime.now().strftime("%S") == "00"):
                try:
                    data = probe[ids].read()
                    while (datetime.datetime.now().strftime("%S") == "00"):
                        pass

                except Exception as e:
                    if debug: print ("ERROR: {}".format(e))

                except KeyboardInterrupt:                                               # CTRL+C catcher - Not working
                    sys.exit("Program terminated properly")

            if not continuous: loops -= 1

#-------------------------------------------------------------
#----------------------- Main program ------------------------
#-------------------------------------------------------------
if __name__ == '__main__':
    os.system('clear')
    while not exitFlag:
        if (li8xStatus == True): print "Li820:  Active" #(("Li820:  {}").format(probe[cnt1].get_data())
        else: print ("Li820:  Inactive")
        if (li6xStatus == True): print "Li6262: Active" #(("Li6262: {}").format(probe[cnt2].get_data())
        else: print ("Li6262: Inactive")
        if (i2cStatus  == True): print "I2C:    Active" #(("I2C:    {}").format(probe[cnt3].get_data())
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
            li8xStatus = 1
            args_list['device'] = 820
            args_list['id'] = cnt1 = cnt
            a = Process(target=licor, kwargs=args_list)
            a.start()
            cnt += 1

        elif user_input is '2':
            args_list['device'] = 6262
            args_list['id'] = cnt2 = cnt
            cnt += 1
            
            b = Process(target=licor, kwargs=args_list)
            
            if not li6xStatus:
                li6xStatus = 1
                b.start()
                
            else:
                li6xStatus = 0
                b.terminate()
            
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
