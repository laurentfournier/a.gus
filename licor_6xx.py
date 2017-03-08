# -*- coding: utf-8 -*-

'''
    IO data from/to a Licor 6262

    Written by Laurent Fournier, November 2016
'''

import os, datetime, serial

# External libraries
import file_manager as fm

  ##################
  # Initialisation #
  ##################

class Licor6xx:
    def __init__(self, data, device):
        self.port    = device['port']
        self.baud    = device['baud']
        self.timeout = device['timeout']
        self.debug   = device['debug']
        self.device  = device['device']

        self.q_data, self.q_header = data

        fp = fm.fManager('config/.cfg', 'r')
        fp.open()
        fp.cfg_loader()

        '''# Write to the device
        if (self.config): self._header = [ line.strip() for line in fp.get_cfg('li6262write') ]
        # Read from the device
        else:'''
        self._header = [ line.strip() for line in fp.get_cfg('li6262read') ]

        self.q_header.put(self._header)
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
            self.con.flush()
            self.con.close()
            self.con.__del__()

        except Exception as e:
            self.con = None
            return e

        return True

    def read(self):
        self.con.readline()

        raw = self.con.readline()
        res = [ raw.split()[0], raw.split()[1], raw.split()[2], raw.split()[3], ]  # raw.split()[4]

        self.q_data.put(res)

        if self.debug:
            print ("\nNew Data Point")
            for each in zip(self._header, res):
                print (each[0], each[1])

        return res

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
        return "Licor Model Li-{}".format(self.device)
