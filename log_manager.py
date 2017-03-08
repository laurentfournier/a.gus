# -*- coding: utf-8 -*-

'''
    Files IO managing and processing

    Written by Laurent Fournier, December 2016
'''

import os, sys, datetime

from multiprocessing import Process
from threading       import Timer, Thread#, Queue, Pipe
from Queue           import Queue, Empty
import subprocess

import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

# External libraries
from licor_6xx import Licor6xx
from licor_7xx import Licor7xx
from licor_8xx import Licor8xx

  ############
  # Settings #
  ############

LOG_DIR = 'logs/'


  ##################
  # Initialisation #
  ##################

class logManager:
    def __init__(self, data, devices, debug):
        self.devices = devices
        self.debug   = debug
        
        self.q_data, self.q_header = data

        self.probes = []
        self.buffer = []
        self.run    = False

    # Connect to device
    def start(self):
        try:
            for i in range(len(self.devices)):
                if   (self.devices[i]['device'] is '820'):  self.probes.append(Licor8xx((self.q_data, self.q_header), self.devices[i]))
                elif (self.devices[i]['device'] is '840'):  self.probes.append(Licor8xx((self.q_data, self.q_header), self.devices[i]))
                elif (self.devices[i]['device'] is '6262'): self.probes.append(Licor6xx((self.q_data, self.q_header), self.devices[i]))
                elif (self.devices[i]['device'] is '7000'): self.probes.append(Licor7xx((self.q_data, self.q_header), self.devices[i]))

            self.run = True
                
            for i in range(len(self.probes)):    
                self.probes[i].connect()

        except Exception as e:
            if (self.debug): print ("ERROR: {}".format(e))
            sys.exit("Could not connect to the device")

    # Disconnect to device
    def stop(self):
        try:
            for i in range(len(self.probes)):
                self.probes[i].disconnect()
                self.run = False

        except Exception as e:
            if (self.debug): print ("ERROR: {}".format(e))

    # Configure the device
    def write(self, probe, mode):
        if (self.config):
            try:
                if (mode is 'r'): probe.config_R()
                if (mode is 'w'): probe.config_W()

            except Exception as e:
                if (self.debug):
                    print ("ERROR: {}".format(e))

    # Log data
    def read(self):
        date_time = datetime.datetime.now()
        date      = datetime.datetime.now().strftime('%Y-%m-%d')
        time      = datetime.datetime.now().strftime('%H:%M:%S')
        
        path      = '{}'.format(LOG_DIR)
        filename  = '{}data-{}.csv'.format(path, date_time)

        # Verify if directory already exists
        if not (os.path.isdir(path)):
            os.system('mkdir {}'.format(path))

        # Logging
        with open(filename, 'w') as fp:
            fp.write('Date;Time;')

            while not self.q_header.empty():
                header = self.q_header.get()
                
                # Write headers
                fp.write(';'.join(header))
            fp.write('\n')

            while self.run is True:
                if (datetime.datetime.now().strftime("%S") == "00"):
                    try:
                        # Read from device
                        for i in range(len(self.probes)):
                            self.probes[i].read()

                        fp.write('{};{};'.format(datetime.datetime.now().strftime('%Y-%m-%d'),
                                                 datetime.datetime.now().strftime('%H:%M:%S')))                        

                        while not self.q_data.empty():
                            data = self.q_data.get()
                            # Write data
                            fp.write(';'.join(data))
                            
                            fp.write(';')
                        fp.write('\n')

                        fp.flush()
                        os.fsync(fp)
                        
                        # Do only once per minute
                        while (datetime.datetime.now().strftime("%S") == "00"):
                            pass

                    except Exception as e:
                        if (self.debug): print ("ERROR: {}".format(e))

            fp.close()
