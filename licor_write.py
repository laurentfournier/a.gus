'''
    Write data to a Licor 820 and/or 840
    
    Written by Laurent Fournier, October 2016

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
from lxml import etree
from bs4  import BeautifulSoup as bs

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Terminal #
  ############

parser = argparse.ArgumentParser(description = '')
parser.add_argument('-c', '--config', action='store_true', help='Ask actual configuration')
parser.add_argument('-d', '--debug', type=bool, help='Debugging mode',      default=True, choices=[True, False])
parser.add_argument('-m', '--model', type=int,  help='Select device model', default=820,  choices=[820, 840])
args = parser.parse_args()
  
  ############
  # Settings #
  ############
  
DEBUG     = args.debug
FREQ      = 1
PORT      = '/dev/ttyUSB0'
BAUD      = 9600
PARITY    = 'N'
STOPBIT   = 1
BYTE_SZ   = 8
TIMEOUT   = 5.0
LOG_DIR   = 'logs/'

isStarted  = False
device_nr  = args.model                                                                 # List of devices's models


#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################
  
class Licor_W:
    def __init__(self, **kwargs):
        self.port       = kwargs.pop('port',    '/dev/ttyUSB0')
        self.baud       = kwargs.pop('baud',    BAUD)
        self.timeout    = kwargs.pop('timeout', TIMEOUT)
        
        self._header    = [ 'li820',                                                    # (0)Must be present all the time
                            'rs232',                                                    # (1)Reading purpose
                            'celltemp',                                                 # (2)
                            'cellpres',                                                 # (2)
                            'co2',                                                      # (2)
                            'co2abs',                                                   # (2)
                            'ivolt',                                                    # (2)
                            'raw',                                                      # (2)
                            'data',                                                     # (1)Config purpose
                            'cfg',                                                      # (1)Config purpose
                            'cal']                                                      # (1)Config purpose

    def connect(self):
        try:
            self.con = serial.Serial(self.port, self.baud, timeout=self.timeout)        # Connect to serial device
            self.con.flushInput()
            self.con.flushOutput()
            
        except Exception as e:
            self.con = None
            return e
        
        return True

    def config_W(self):                                                                 # Write a complete instruction row
        conf = etree.Element(self._header[0])                                           # <li820>
        conn = etree.SubElement(conf, self._header[1])                                  #   <rs232>
        co2a = etree.SubElement(conn, self._header[5])                                  #       <co2abs>   --> False
        co2a.text = "false"
        ivol = etree.SubElement(conn, self._header[6])                                  #       <ivolt>    --> False
        ivol.text = "false"
        raws = etree.SubElement(conn, self._header[7])                                  #       <raw>      --> False
        raws.text = "false"

        if not args.config:
            self.con.write(etree.tostring(conf, pretty_print = False))                  # Send command
            print ("Input: " + etree.tostring(conf, pretty_print = False))              # Licor answer (ACK true or false)

            data_response = self.con.readline()
            print ("Output: " + data_response)
    
    def config_R(self):                                                                 # Write a config request
        info = etree.Element(self._header[0])                                           # Write the actual configuration
        info.text = "?"                                                                 # <li820>?</li820>
        #data = etree.SubElement(info, self._header[8])                                 # --> List all
        #data.text = "?"                                                                # 

        if args.config:
            self.con.write(etree.tostring(info, pretty_print = False))
            print ("Input: " + etree.tostring(info, pretty_print = False))

            data_response = self.con.readline()
            print ("Output: " + data_response)
    
    def __repr__(self):
        return "Licor Model Li-{}".format(device_nr)


  ################
  # Main program #
  ################
  
if DEBUG:
    try:                                                                                    # Connect to device
        licor = Licor_W(port=PORT, baud=BAUD, timeout=TIMEOUT, debug=DEBUG)
        licor.connect()
        licor.config_R()
        licor.config_W()
    
    except Exception as e:
        print ("ERROR: {}".format(e))
            
        sys.exit("Could not connect to the device")
    

        


