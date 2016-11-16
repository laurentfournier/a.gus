# -*- coding: utf-8 -*-

'''
    IO data from/to a Licor 6262
    
    Written by Laurent Fournier, November 2016

    LI6262: Temp->C    Pres->kPa  CO2->μm/m  H2O->mm/m  DewPt->C  
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse

from bs4  import BeautifulSoup as bs
from lxml import etree

# External libraries
import file_manager as fm

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Settings #
  ############

CONFIG     = False
CONTINUOUS = True
DEBUG      = True
LOG        = True
LOOPS      = 5                                                                          # Nr of data extractions
DEVICE     = 820                                                                        # List of devices's models

FREQ       = 60
PORT       = '/dev/ttyUSB0'
BAUD       = 9600
PARITY     = 'N'
STOPBIT    = 1
BYTE_SZ    = 8
TIMEOUT    = 5.0
LOG_DIR    = 'logs/'
HEADER     = []


#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################
  
class Licor6xx:
    def __init__(self, **kwargs):
        self.port       = kwargs.pop('port',    PORT)
        self.baud       = kwargs.pop('baud',    BAUD)
        self.timeout    = kwargs.pop('timeout', TIMEOUT)
        self.config     = kwargs.pop('config',  CONFIG)
        self.continuous = kwargs.pop('continuous', CONTINUOUS)
        self.debug      = kwargs.pop('debug',   DEBUG)
        self.log        = kwargs.pop('log',     LOG)
        self.loops      = kwargs.pop('loops',   LOOPS)
        self.device     = kwargs.pop('device',  DEVICE)
        self._header    = kwargs.pop('header',  HEADER)

        fp = fm.fManager('config/.cfg', 'r')
        fp.open()
        fp.cfg_loader()

        if self.config:                                                                 # Write to the device
            self._header = [ line.strip() for line in fp.get_cfg('li6262write') ]
            
        else:                                                                           # Read from the device
            self._header = [ line.strip() for line in fp.get_cfg('li6262read') ]

        fp.close()

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
        raw = self.con.readline()
        res = [ datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'),
                raw.split()[0], raw.split()[1], raw.split()[2], raw.split()[3], raw.split()[4] ]

        if self.debug:
            print ("\nNew Data Point")
            for each in zip(self._header, res):
                print (each[0], each[1])
                
        return res

    def config_W(self):                                                                 # Write a complete instruction row
        self.con.write(self._header[0])                                                 # Send command
        print ("Input: " + self._header[0])
        data_response = self.con.readline()                                             # Licor answer
        print ("Output: " + data_response)
    
    def config_R(self):                                                                 # Ask actual config
        self.con.write(self._header[1])
        print ("Input: " + self._header[1])
        data_response = self.con.readline()
        print ("Output: " + data_response)
    
    def __repr__(self):
        return "Licor Model Li-{}".format(device_nr)

