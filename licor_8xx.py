# -*- coding: utf-8 -*-

'''
    IO data from/to a Licor 820 and 840a

    Written by David H. Hagan, May 2016
    Modifications by Laurent Fournier, October 2016
'''

import os
import datetime
import serial

from bs4         import BeautifulSoup as bs
from lxml        import etree

from multiprocessing import Process

# External libraries
import file_manager as fm

#-------------------------------------------------------------
#----- Better know what you are doing from this point --------
#-------------------------------------------------------------

  ##################
  # Initialisation #
  ##################

class Licor8xx(Process):
    def __init__(self, pipe, header, kwargs):
        self.port       = kwargs['port']
        self.baud       = kwargs['baud']
        self.timeout    = kwargs['timeout']
        self.config     = kwargs['config']
        self.continuous = kwargs['continuous']
        self.debug      = kwargs['debug']
        self.log        = kwargs['log']
        self.loops      = kwargs['loops']
        self.device     = kwargs['device']

        self.p_in, self.p_out = pipe
        self.header = header

        fp = fm.fManager('config/.cfg', 'r')
        fp.open()
        fp.cfg_loader()

        if (self.config):                                                                 # Write to the device
            if   (self.device == 820):  self._header = [ line.strip() for line in fp.get_cfg('li820write') ]
            elif (self.device == 840):  self._header = [ line.strip() for line in fp.get_cfg('li840write') ]
            else: print ("Wrong device's Model")

        else:                                                                           # Read from the device
            if   (self.device == 820):  self._header = [ line.strip() for line in fp.get_cfg('li820read') ]
            elif (self.device == 840):  self._header = [ line.strip() for line in fp.get_cfg('li840read') ]
            else: print ("Wrong device's Model")

        self.header.put(self._header)
        fp.close()

    def connect(self):
        try:
            # Connect to serial device
            self.con = serial.Serial(self.port, self.baud, timeout=self.timeout)
            # Wash buffers
            self.con.flushInput()
            self.con.flushOutput()
            #self.con.reset_input_buffer()
            #self.con.reset_output_buffer()

        except Exception as e:
            self.con = None
            return e

        return True

    def disconnect(self):
        try:
            self.con.reset_input_buffer()
            self.con.reset_output_buffer()
            self.con.flush()
            self.con.close()
            self.con.__del__()

        except Exception as e:
            self.con = None
            return e

        return True

    def read(self):
        self.con.readline()
        
        # Define data structure
        if self.device == 820:
            raw = bs(self.con.readline(), 'lxml')
            raw = raw.li820.data
            
            res = [ datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'),
                    raw.celltemp.string, raw.cellpres.string, raw.co2.string, ]

        elif self.device == 840:
            raw = bs(self.con.readline(), 'lxml')
            raw = raw.li840.data
            
            res = [ datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%H:%M:%S'),
                    raw.celltemp.string, raw.cellpres.string, raw.co2.string, raw.h2o.string, raw.h2odewpoint, ]

        self.res = res
        self.p_out.put(res)

        if self.debug:
            print ("\nNew Data Point")
            for each in zip(self._header, res):
                print (each[0], each[1])

        return self.res

    # Write a complete instruction row
    def config_W(self):
        if self.device == 820:
            conf = etree.Element(self._header[0])                                       # <li820>
            cfgs = etree.SubElement(conf, self._header[9])                              #   <cfg>
            outr = etree.SubElement(cfgs, self._header[11])                             #       <outrate>  --> 1
            outr.text = "1"
            conn = etree.SubElement(conf, self._header[1])                              #   <rs232>
            co2a = etree.SubElement(conn, self._header[5])                              #       <co2abs>   --> False
            co2a.text = "false"
            ivol = etree.SubElement(conn, self._header[6])                              #       <ivolt>    --> False
            ivol.text = "false"
            raws = etree.SubElement(conn, self._header[7])                              #       <raw>      --> False
            raws.text = "false"

        # Send command
        self.con.write(etree.tostring(conf, pretty_print = False))
        print ("Input: " + etree.tostring(conf, pretty_print = False))
        # Licor answer (ACK true or false)
        data_response = self.con.readline()
        print ("Output: " + data_response)

    # Ask actual config
    def config_R(self):
        info = etree.Element(self._header[0])
        # <liXXX>?</liXXX>
        info.text = "?"

        self.con.write(etree.tostring(info, pretty_print = False))
        print ("Input: " + etree.tostring(info, pretty_print = False))
        data_response = self.con.readline()
        print ("Output: " + data_response)

    def get_data(self, search):
        if (search is 'pid'): answer = self.pid

        return answer

    def __repr__(self):
        return "Licor Model Li-{}".format(device_nr)
