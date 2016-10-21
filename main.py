'''
    IO data from/to multiple sensors
    
    Written by Laurent Fournier, October 2016
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse

from bs4  import BeautifulSoup as bs
from lxml import etree

import first_launch   as fl
import licor_8xx_6262 as li

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
parser.add_argument('-m', '--model',      type=int,  help='Select device model',   default=820,   choices=[820, 840, 6262])
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
DEVICE     = args.model                                                                 # List of devices's models

FREQ       = 60
PORT       = '/dev/ttyUSB0'
BAUD       = 9600
PARITY     = 'N'
STOPBIT    = 1
BYTE_SZ    = 8
TIMEOUT    = 5.0
LOG_DIR    = 'logs/'


#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ###################
  # Reading routine #
  ###################
  
filename = 'licor{}-data-{}.csv'.format(DEVICE, datetime.datetime.now())

if LOG_DIR:                                                                             # If LOG_DIR is set, add it to filename
    filename = os.path.join(LOG_DIR, filename)

try:                                                                                    # Connect to device
    licor = li.Licor(port=PORT, baud=BAUD, timeout=TIMEOUT, debug=DEBUG)
    licor.k()
    
except Exception as e:
    if DEBUG:
        print ("ERROR: {}".format(e))
        
    sys.exit("Could not connect to the device")

if LOG:                                                                                 # If logging enabled
    with open(filename, 'w') as fp:
        fp.write(';'.join(licor._header))                                               # Write headers
        fp.write('\n')

        while LOOPS:
            try:                
                data = licor.read()                                                     # Read from device

                fp.write(';'.join(data))                                                # Write data
                fp.write('\n')
                
            except Exception as e:
                if DEBUG:
                    print ("ERROR: {}".format(e))
                    
            time.sleep(FREQ)                                                            # Sleep for FREQ seconds
            
            if not CONTINUOUS:
                LOOPS -= 1
                
        fp.close()
        
else:                                                                                   # If logging Disabled
    while LOOPS:
        data = licor.read()
        time.sleep(FREQ)
        
        if not CONTINUOUS:
            LOOPS -= 1
            
  ###################
  # Writing routine #
  ###################
  
if CONFIG:
    try:                                                                                # Connect to device
        licor = Licor(port=PORT, baud=BAUD, timeout=TIMEOUT, debug=DEBUG)
        licor.connect()
        #licor.config_R()
        licor.config_W()
        
    except Exception as e:
        print ("ERROR: {}".format(e))
                
        sys.exit("Could not connect to the device")
