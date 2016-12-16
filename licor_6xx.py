# -*- coding: utf-8 -*-

'''
    IO data from/to a Licor 6262

    Written by Laurent Fournier, November 2016
'''

import os
import datetime
import serial

from multiprocessing import Process

# External libraries
import file_manager as fm

#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################

class Licor6xx:
    def __init__(self, queue, header, kwargs):
        self.port       = kwargs['port']
        self.baud       = kwargs['baud']
        self.timeout    = kwargs['timeout']
        self.config     = kwargs['config']
        self.continuous = kwargs['continuous']
        self.debug      = kwargs['debug']
        self.log        = kwargs['log']
        self.loops      = kwargs['loops']
        self.device     = kwargs['device']

        self.q_in, self.q_out = queue
        self.header = header

        fp = fm.fManager('config/.cfg', 'r')
        fp.open()
        fp.cfg_loader()

        # Write to the device
        if (self.config): self._header = [ line.strip() for line in fp.get_cfg('li6262write') ]
        # Read from the device
        else:             self._header = [ line.strip() for line in fp.get_cfg('li6262read') ]

        self.header.put(self._header)
        fp.close()

    def connect(self):
        try:
            # Connect to serial device
            self.con = serial.Serial(self.port, self.baud, timeout=self.timeout)
            # Wash buffers
            self.con.flushInput()
            self.con.flushOutput()

        except Exception as e:
            self.con = None
            return e

        return True

    def disconnect(self):
        try:
            self.con.close()
            self.con.__del__()

        except Exception as e:
            self.con = None
            return e

        return True

    def read(self):
        raw = self.con.readline()

        res = [ datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'),
                raw.split()[0], raw.split()[1], raw.split()[2], raw.split()[3], raw.split()[4] ]

        self.res = res
        self.q_out.put(res)

        if self.debug:
            print ("\nNew Data Point")
            for each in zip(self._header, res):
                print (each[0], each[1])

        return self.res

    # Write a complete instruction row
    def config_W(self):
        # Send command
        self.con.write(self._header[0])
        print ("Input: " + self._header[0])
        # Licor answer
        data_response = self.con.readline()
        print ("Output: " + data_response)

    # Ask actual config
    def config_R(self):
        self.con.write(self._header[1])
        print ("Input: " + self._header[1])
        data_response = self.con.readline()
        print ("Output: " + data_response)

    def get_data(self, search):
        if (search is 'pid'): answer = self.pid

        return answer

    def __repr__(self):
        return "Licor Model Li-{}".format(device_nr)
