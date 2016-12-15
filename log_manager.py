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
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################

def logManager:
    def __init__(self, queue, **kwargs):
        self.config     = kwargs['config']
        self.continuous = kwargs['continuous']
        self.debug      = kwargs['debug']
        self.log        = kwargs['log']
        self.loops      = kwargs['loops']
        self.device     = kwargs['device']
        #self.probe      = []
        
        self.q_in, self.q_out = queue

    def start(self):
        # Connect to device
        try:
            global probe

            if   (self.device == 820 or self.device == 840): self.probe = Licor8xx((q_in, q_out), q_header, **kwargs)
            elif (self.device == 6262):                      self.probe = Licor6xx((q_in, q_out), q_header, **kwargs)
            elif (self.device == 7000):                      self.probe = Licor7xx((q_in, q_out), q_header, **kwargs)

            self.probe.connect()

        except Exception as e:
            if (self.debug):
                print ("ERROR: {}".format(e))
                
            sys.exit("Could not connect to the device")

    def stop(self):
        self.probe.disconnect()

    def write(self, mode):
        # Configure the device if required
        if (self.config):
            try:
                if (mode is 'r'): self.probe.config_R()
                if (mode is 'w'): self.probe.config_W()

            except Exception as e:
                if (self.debug):
                    print ("ERROR: {}".format(e))

    def read(self, mode):
        date_time = datetime.datetime.now()
        pathname = '{}licor{}/'.format(LOG_DIR, device)
        filename = '{}licor{}-data-{}.csv'.format(pathname, device, date_time)

        # Verify if directory already exists
        if not (os.path.isdir(pathname)):
            os.system('mkdir {}'.format(pathname))

        # If logging is enabled
        if (self.log):
            with open(filename, 'w') as fp:
                # Write headers
                fp.write(';'.join(self.probe._header))
                fp.write('\n')

                while (self.loops):
                    data = self.probe.read()
                    if (datetime.datetime.now().strftime("%S") == "00"):
                        try:
                            # Read from device
                            buff = data = self.probe.read()
                            q_out.put(buff)

                            # Write data
                            fp.write(';'.join(data))
                            fp.write('\n')

                            # Do only once per minute
                            while (datetime.datetime.now().strftime("%S") == "00"):
                                pass

                        except Exception as e:
                            if (self.debug):
                                print ("ERROR: {}".format(e))

                    if not (self.continuous): self.loops -= 1

                fp.close()

        # If logging is Disabled
        else:
            while (self.loops):
                if (datetime.datetime.now().strftime("%S") == "00"):
                    try:
                        # Read from device
                        data = self.probe.read()
                        q_out.put(data)

                        # Do only once per minute
                        while (datetime.datetime.now().strftime("%S") == "00"):
                            pass

                    except Exception as e:
                        if (self.debug):
                            print ("ERROR: {}".format(e))

                if not (self.continuous): self.loops -= 1
