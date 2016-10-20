'''
    IO data from/to a Licor 820, 840 and 6262
    
    Written by David H. Hagan, May 2016
    Modifications by Laurent Fournier, October 2016

    To-do :
    - Devices switch
    - For 820:  celltemp, cellpres, co2
    - For 840:  celltemp, cellpres, co2, h2o, h2odewpoint
    - For 6262: celltemp, cellpres, co2, h2o, h2odewpoint
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse
#import string

from bs4  import BeautifulSoup as bs
from lxml import etree


#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Settings #
  ############

CONFIG     = args.config
CONTINUOUS = args.continuous
DEBUG      = args.debug
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

  ##################
  # Initialisation #
  ##################
  
class Licor:
    def __init__(self, **kwargs):
        self.port       = kwargs.pop('port',    '/dev/ttyUSB0')
        self.baud       = kwargs.pop('baud',    BAUD)
        self.timeout    = kwargs.pop('timeout', TIMEOUT)
        self.debug      = kwargs.pop('debug',   DEBUG)

        if CONFIG:                                                                      # Write to the device
            self._header = [ 'li820',                                                   # (RW)Must be present all the time
                             'rs232',                                                   # (R)
                             'celltemp',                                                # 
                             'cellpres',                                                # 
                             'co2',                                                     # 
                             'co2abs',                                                  # 
                             'ivolt',                                                   # 
                             'raw',                                                     # 
                             'data',                                                    # (W)
                             'cfg',                                                     # (W)
                             'cal',                                                     # (W)
                             'outrate']                                                 # (W)
            
        else:                                                                           # Read from the device
            self._header = [ 'date',
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

    def config_W(self):                                                                 # Write a complete instruction row
        conf = etree.Element(self._header[0])                                           # <li820>
        cfgs = etree.SubElement(conf, self._header[9])                                  #   <cfg>
        outr = etree.SubElement(cfgs, self._header[11])                                 #       <outrate>  --> 1
        outr.text = "1"
        conn = etree.SubElement(conf, self._header[1])                                  #   <rs232>
        co2a = etree.SubElement(conn, self._header[5])                                  #       <co2abs>   --> False
        co2a.text = "false"
        ivol = etree.SubElement(conn, self._header[6])                                  #       <ivolt>    --> False
        ivol.text = "false"
        raws = etree.SubElement(conn, self._header[7])                                  #       <raw>      --> False
        raws.text = "false"

        self.con.write(etree.tostring(conf, pretty_print = False))                      # Send command
        print ("Input: " + etree.tostring(conf, pretty_print = False))                  # Licor answer (ACK true or false)
        data_response = self.con.readline()
        print ("Output: " + data_response)
    
    def config_R(self):                                                                 # Write a config request
        info = etree.Element(self._header[0])                                           # Write the actual configuration
        info.text = "?"                                                                 # <li820>?</li820>
        
        self.con.write(etree.tostring(info, pretty_print = False))
        print ("Input: " + etree.tostring(info, pretty_print = False))
        data_response = self.con.readline()
        print ("Output: " + data_response)
    
    def __repr__(self):
        return "Licor Model Li-{}".format(device_nr)

