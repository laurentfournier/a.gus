# -*- coding: utf-8 -*-

'''
    Files IO managing and processing
    
    Written by Laurent Fournier, December 2016
'''

import os, sys, subprocess
import datetime
import argparse

from multiprocessing import Process, Queue, Pipe
from threading       import Timer

import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

# External libraries
from licor_6xx import Licor6xx
from licor_7xx import Licor7xx
from licor_8xx import Licor8xx

#-------------------------------------------------------------
#------------------ Open configurations ----------------------
#-------------------------------------------------------------

  ############
  # Settings #
  ############

LOG_DIR = 'logs/'


#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################

class logManager:
    def __init__(self, queue, kwargs):
        self.config     = kwargs['config']
        self.continuous = kwargs['continuous']
        self.debug      = kwargs['debug']
        self.device     = kwargs['device']
        self.log        = kwargs['log']
        self.loops      = kwargs['loops']
        self.device     = kwargs['device']
        self.kwargs     = kwargs
        
        self.q_in, self.q_out = queue
        self.q_header = Queue()

    # Connect to device
    def start(self):
        try:
            if   (self.device == 820 or self.device == 840): self.probe = Licor8xx((self.q_in, self.q_out), self.q_header, self.kwargs)            
            elif (self.device == 6262):                      self.probe = Licor6xx((self.q_in, self.q_out), self.q_header, self.kwargs)            
            elif (self.device == 7000):                      self.probe = Licor7xx((self.q_in, self.q_out), self.q_header, self.kwargs)

            self.probe.connect()

        except Exception as e:
            if (self.debug): print ("ERROR: {}".format(e))
            sys.exit("Could not connect to the device")

    # Disconnect to device
    def stop(self):
        self.probe.disconnect()
        
    # Configure the device
    def write(self, mode):
        if (self.config):
            try:
                if (mode is 'r'): self.probe.config_R()
                if (mode is 'w'): self.probe.config_W()

            except Exception as e:
                if (self.debug):
                    print ("ERROR: {}".format(e))

    # Read data (w/ or w/out logging)
    def read(self, mode):
        date_time  = datetime.datetime.now()
        self.path  = '{}licor{}/'.format(LOG_DIR, self.device)
        self.fname = 'licor{}-data-{}.csv'.format(self.device, date_time)
        filename   = '{}licor{}-data-{}.csv'.format(self.path, self.device, date_time)

        # Verify if directory already exists
        if not (os.path.isdir(self.path)):
            os.system('mkdir {}'.format(self.path))

        # If logging is enabled
        if (mode is 'logger'):
            with open(filename, 'w') as fp:
                # Write headers
                fp.write(';'.join(self.probe._header))
                fp.write('\n')

                while (self.loops):
                    data = self.probe.read()
#                    if (datetime.datetime.now().strftime("%S") == "00"):
                    try:
                        # Read from device
                        buff = data = self.probe.read()
                        self.q_out.put(buff)

                        # Write data
                        fp.write(';'.join(data))
                        fp.write('\n')

                        # Do only once per minute
#                            while (datetime.datetime.now().strftime("%S") == "00"):
#                                pass

                    except Exception as e:
                        if (self.debug): print ("ERROR: {}".format(e))

                    if not (self.continuous): self.loops -= 1

                fp.close()

        # If logging is Disabled
        else:
            while (self.loops):
                if (datetime.datetime.now().strftime("%S") == "00"):
                    try:
                        # Read from device
                        data = self.probe.read()
                        self.q_out.put(data)

                        # Do only once per minute
                        while (datetime.datetime.now().strftime("%S") == "00"):
                            pass

                    except Exception as e:
                        if (self.debug): print ("ERROR: {}".format(e))

                if not (self.continuous): self.loops -= 1
