'''
    Read data from a Licor 820 and/or 840
    
    Written by David H. Hagan, May 2016
    Modifications by Laurent Fournier, October 2016

    To-do :
    - Devices switch
    - For 820: celltemp, cellpres, co2
    - For 840: celltemp, cellpres, co2, h2o, h2odewpoint
'''

import os, sys, subprocess
import time, datetime
import serial
#import string
import argparse
from bs4 import BeautifulSoup as bs

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Terminal #
  ############

parser = argparse.ArgumentParser(description = '')
parser.add_argument('-c', '--continuous', action='store_true', help='No outputs limitation')
parser.add_argument('-d', '--debug',   type=bool, help='Debugging mode',        default=True, choices=[True, False])
parser.add_argument('-l', '--loops',   type=int,  help='Number of outputs',     default=5)
parser.add_argument('-L', '--logging', type=bool, help='Storing in .CSV files', default=True, choices=[True, False])
parser.add_argument('-m', '--model',   type=int,  help='Select device model',   default=820,  choices=[820, 840])
args = parser.parse_args()
  
  ############
  # Settings #
  ############
  
DEBUG     = args.debug
LOG       = args.logging
FREQ      = 1
PORT      = '/dev/ttyUSB0'
BAUD      = 9600
PARITY    = 'N'
STOPBIT   = 1
BYTE_SZ   = 8
TIMEOUT   = 5.0
LOG_DIR   = 'logs/'

isLooping = args.loops                                                                  # Nr of data extractions
isStarted = False

device_nr = args.model                                                                  # List of devices's models


#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################
  
class Licor_R:
    def __init__(self, **kwargs):
        self.port       = kwargs.pop('port',    '/dev/ttyUSB0')
        self.baud       = kwargs.pop('baud',    BAUD)
        self.timeout    = kwargs.pop('timeout', TIMEOUT)
        self.debug      = kwargs.pop('debug',   DEBUG)

        self._header    = [ 'date',
                            'time',
                            'cell_temp',
                            'cell_pressure',
                            'co2']

    def connect(self):
        try:
            self.con = serial.Serial(self.port, self.baud, timeout=self.timeout)        # Connect to serial device
            self.con.flushInput()
            self.con.flushOutput()
            
        except Exception as e:
            self.con = None
            return e
        
        return True

    def read(self):                                                                     
        raw = bs(self.con.readline(), 'lxml')                                           # Read a complete row input stream

        raw = raw.li820.data                                                            # Define data structure
        res = [ datetime.datetime.now().isoformat(';'),                                 # where will be stored data from the device
                raw.celltemp.string,
                raw.cellpres.string,
                raw.co2.string, ]

        if DEBUG:
            print ("\nNew Data Point")
            for each in zip(self._header, res):
                print (each[0], each[1])
                
        return res

    def __repr__(self):
        return "Licor Model Li-{}".format(device_nr)


  ################
  # Main program #
  ################

if DEBUG:
    filename = 'licor{}-data-{}.csv'.format(device_nr, datetime.datetime.now())
    
    if LOG_DIR:                                                                             # If LOG_DIR is set, add it to filename
        filename = os.path.join(LOG_DIR, filename)
    
    try:                                                                                    # Connect to device
        licor = Licor_R(port=PORT, baud=BAUD, timeout=TIMEOUT, debug=DEBUG)
        licor.connect()
        
    except Exception as e:
        print ("ERROR: {}".format(e))
            
        sys.exit("Could not connect to the device")
    
    if LOG:                                                                                 # If logging enabled
        with open(filename, 'w') as fp:
            fp.write(';'.join(licor._header))                                               # Write headers
            fp.write('\n')
    
            while isLooping:
                try:                
                    data = licor.read()                                                     # Read from device
    
                    fp.write(';'.join(data))                                                # Write data
                    fp.write('\n')
                    
                except Exception as e:
                    print ("ERROR: {}".format(e))
                        
                time.sleep(FREQ)                                                            # Sleep for FREQ seconds
                
                if not args.continuous:
                    isLooping -= 1
                    
            fp.close()
            
    else:                                                                                   # If logging Disabled
        while isLooping:
            data = licor.read()
            time.sleep(FREQ)
            
            if not args.continuous:
                isLooping -= 1
