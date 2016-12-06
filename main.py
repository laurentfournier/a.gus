# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse
import threading
import Queue
import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

from bs4         import BeautifulSoup as bs
from lxml        import etree
from collections import Counter

# External libraries
import file_manager as fm
from tools     import *
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
parser.add_argument('-d', '--debug',      type=bool, help='Debugging mode',        default=True,  choices=[True, False])
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

FREQ       = 5
PORT       = '/dev/ttyUSB0'
BAUD       = 9600
PARITY     = 'N'
STOPBIT    = 1
BYTE_SZ    = 8
TIMEOUT    = 5.0
LOG_DIR    = 'logs/'

args_list  = { 'port' : PORT,    'baud': BAUD,             'timeout': TIMEOUT,
               'config': CONFIG, 'continuous': CONTINUOUS, 'debug': DEBUG,
               'device': DEVICE, 'log': LOG,               'loops': LOOPS }

data  = 0000.00
count = 0

exitFlag   = 0
threadList = [ "Thread-1", "Thread-2" ]
nameList   = ["One", "Two", "Three", "Four", "Five"]
queueLock  = threading.Lock()
workQueue  = Queue.Queue(10)
threads    = []
threadID   = 1

#-------------------------------------------------------------
#------------------ Create 'thread' object -------------------
#-------------------------------------------------------------
'''class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, kwargs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.kwargs = kwargs

    def run(self):
        print "Starting " + self.name
        t_process(self.name, self.q)
        print "Finishing " + self.name

def t_process(threadName, q):
    while not exitFlag:
        queueLock.acquire()

        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)

        else:
            queueLock.release()

        time.sleep(1)'''

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

#-------------------------------------------------------------
#----------------- Tests for Licor sensors -------------------
#-------------------------------------------------------------
def licor(**kwargs):
    config     = kwargs.pop('config',  CONFIG)
    continuous = kwargs.pop('continuous', CONTINUOUS)
    debug      = kwargs.pop('debug',   DEBUG)
    log        = kwargs.pop('log',     LOG)
    loops      = kwargs.pop('loops',   LOOPS)
    device     = kwargs.pop('device',  DEVICE)

    try:                                                                                # Connect to device
        if   device == 820 or device == 840: probe = Licor8xx(**kwargs)
        elif device == 6262:                 probe = Licor6xx(**kwargs)
        elif device == 7000:                 probe = Licor7xx(**kwargs)

        probe.connect()

    except Exception as e:
        if debug: print ("ERROR: {}".format(e))
        sys.exit("Could not connect to the device")

      ###################
      # Writing routine #
      ###################
    if config:                                                                          # Configure the device if required
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
    filename = 'licor{0}/licor{0}-data-{1}.csv'.format(device, date_time)

    if LOG_DIR:                                                                         # If LOG_DIR is set, add it to filename
        filename = os.path.join(LOG_DIR, filename)

    if log:                                                                             # If logging is enabled
        try:                                                                            # Verify if directory already exists
            with open(filename, 'r'): pass

        except Exception:                                                               # If not, create them
            os.system('mkdir {}licor{}/'.format(LOG_DIR, device))
            pass

        with open(filename, 'w') as fp:
            fp.write(';'.join(probe._header))                                           # Write headers
            fp.write('\n')

            while loops:
                if (datetime.datetime.now().strftime("%S") == "00"):
                    try:
                        data = probe.read()                                             # Read from device
                        fp.write(';'.join(data))                                        # Write data
                        fp.write('\n')

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
                    data = probe.read()

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
    licor(**args_list)
