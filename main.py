# -*- coding: utf-8 -*-

'''
    IO data from/to multiple sensors

    Written by Laurent Fournier, October 2016
'''

from copy            import deepcopy
from multiprocessing import Process
from Queue           import Queue
from threading       import Timer, Thread

import os, sys
import argparse
import datetime
import json
import subprocess

import signal
signal.signal(signal.SIGINT, signal.default_int_handler)

# Kivy libraries
from kivy.app               import App
from kivy.clock             import Clock
from kivy.factory           import Factory
from kivy.properties        import (ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty)
from kivy.storage.jsonstore import JsonStore

from kivy.uix.accordion   import Accordion, AccordionItem
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.button      import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label       import Label
from kivy.uix.listview    import ListItemButton
from kivy.uix.modalview   import ModalView
from kivy.uix.popup       import Popup
from kivy.uix.settings    import Settings, SettingsWithSidebar
from kivy.uix.switch      import Switch
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget      import Widget

# External libraries
import log_manager as lm


#-------------------------------------------------------------
#--------------------- Configurations ------------------------
#-------------------------------------------------------------

  ############
  # Terminal #
  ############

parser = argparse.ArgumentParser(description = '')
parser.add_argument('-d', '--debug', type=bool, help='Stderr outputs', default=False, choices=[True])
args = parser.parse_args()

  ############
  # Settings #
  ############

DEBUG   = args.debug
CONFIG  = False
BAUD    = 9600
TIMEOUT = 5.0

PORT   = [ '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3',
           '0x64',         '0x65' ]

DEVICE = [ '820',          '840',          '6262',         '7000',
           'i2c1',         'i2c2' ]

args_device = { 'port':PORT[0],  'baud':BAUD,   'timeout':TIMEOUT,
                'config':CONFIG, 'debug':DEBUG, 'device':DEVICE[0],
                'state':False}

q_data   = Queue()
q_header = Queue()
devices   = []

exitFlag  =  False
li8xFlag  =  False
li6xFlag  =  False
i2cFlag   =  False
probeCnt  = -1


#-------------------------------------------------------------
#-------------------- Debugging program ----------------------
#-------------------------------------------------------------
def DebugApp():
    global exitFlag, li8xFlag, li6xFlag, i2cFlag, probeCnt
    global DEBUG, CONFIG, BAUD, TIMEOUT, PORT, DEVICE
    global args_device, q_data, q_header, devices

    os.system('clear')

    while not exitFlag:
        if (li8xFlag is True): print ("Li820:  Active")
        else:                  print ("Li820:  Inactive")

        if (li6xFlag is True): print ("Li6262: Active")
        else:                  print ("Li6262: Inactive")

        if (i2cFlag  is True): print ("I2C:    Active")
        else:                  print ("I2C:    Inactive")

        print ("____________________________________________________________\n")

        user_input = raw_input("\t|-----------------|\n"
                               "\t| 0. Execute      |\n"
                               "\t| --------------- |\n"
                               "\t| 1. Licor 820    |\n"
                               "\t| 2. Licor 6262   |\n"
                               "\t| 3. I2C          |\n"
                               "\t| --------------- |\n"
                               "\t| Q. Exit Program |\n"
                               "\t|-----------------|\n")
        os.system('clear')

        if user_input is '0':
            logger = lm.logManager((q_data, q_header), devices, DEBUG)
            logger.start()

            t_logg = Process(target=logger.read)
            t_logg.start()

        elif user_input is '1':
            probeCnt += 1
            args_device['id']     = probeCnt
            args_device['name']   = 'Licor820'
            args_device['port']   = PORT[0]
            args_device['device'] = DEVICE[0]

            devices.append(deepcopy(args_device))

            if not li8xFlag: li8xFlag = True
            else:            li8xFlag = False

        elif user_input is '2':
            probeCnt += 1
            args_device['id']     = probeCnt
            args_device['name']   = 'Licor6262'
            args_device['port']   = PORT[1]
            args_device['device'] = DEVICE[2]

            devices.append(deepcopy(args_device))

            if not li6xFlag: li6xFlag = True
            else:            li6xFlag = False

        elif user_input is '3':
            probeCnt += 1
            args_device['id']     = probeCnt
            args_device['name']   = 'I2C'
            args_device['port']   = PORT[4]
            args_device['device'] = DEVICE[4]

            devices.append(deepcopy(args_device))

            if not i2cFlag: i2cFlag = True
            else:           i2cFlag = False

        elif user_input is 'q' or 'Q':
            t_logg.terminate()
            logger.stop()
            exitFlag = True

        else: pass


#-------------------------------------------------------------
#----------------------- Main program ------------------------
#-------------------------------------------------------------
class ThreadData(BoxLayout):
    abs

class ThreadPlot(BoxLayout):
    abs

class AgusRoot(TabbedPanel):
    label_wid1  = ObjectProperty();
    switch_wid1 = ObjectProperty();
    spin_wid1   = ObjectProperty()

    label_wid2  = ObjectProperty();
    switch_wid2 = ObjectProperty();
    spin_wid2   = ObjectProperty()

    carousel    = ObjectProperty()
    info1       = StringProperty()
    info2       = StringProperty()

    no_Device   = False

    def get_probes(self):
        self.set_device(devices[0], 'state', self.switch_wid1.active)
        self.set_device(devices[0], 'port',  self.spin_wid1.text)
        self.label_wid1.text = 'Licor {} - {} - {}'.format(self.get_device(devices[0], 'device'), self.switch_wid1.active, self.get_device(devices[0], 'port'))
        self.info1 = str(self.get_device(devices[0], 'state'))

        self.set_device(devices[1], 'state', self.switch_wid2.active)
        self.set_device(devices[1], 'port',  self.spin_wid2.text)
        self.label_wid2.text = 'Licor {} - {} - {}'.format(self.get_device(devices[1], 'device'), self.switch_wid2.active, self.get_device(devices[1], 'port'))
        self.info2 = str(self.get_device(devices[1], 'state'))

        #self.set_probes()

    def set_probes(self):
        try:
            logger = lm.logManager((q_data, q_header), devices, DEBUG)
            logger.start()

            t_logg = Process(target=logger.read)
            t_logg.start()

        except:
            no_Device = True

        finally:
            pass

    def exit_app(self):
        t_logg.terminate()
        logger.stop()
        os.system("sudo shutdown now -h")

    def get_ports(self):
        # get active ports as text label:
        result1_1 = self.get_device(devices[0], 'port')
        result1_2 = self.get_device(devices[1], 'port')
        self.spin_wid1.text = str(result1_1)
        self.spin_wid2.text = str(result1_2)

        # get all other ports as list of values:
        result2 = PORT
        self.spin_wid1.values = map(str, result2)
        self.spin_wid2.values = map(str, result2)

    def set_ports(self):
        todo

    def get_data(self):
        todo

    def set_data(self):
        todo

    def get_device(self, device, tag):
        return device[tag]

    def set_device(self, device, tag, content):
        device[tag] = content


class AgusApp(App):
    def build_config(self, config):
        config.setdefaults('General', {'gps' : 'Enabled', 'fullscreen' : 'True'})

    def build_settings(self, settings):
        settings.add_json_panel("a.gus", self.config, data = """
            [
                {"type": "options", "title": "GPS", "section": "General", "key": "gps", "options": ["Enabled", "Disabled"]},
                {"type": "options", "title": "Fullscreen", "section": "General", "key": "fullscreen", "options": ["True", "False"]}
            ]""")

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            if (key == "gps"):
                try:
                    '''self.root.current_weather.update_weather()
                    self.root.forecast.update_weather()'''

                except AttributeError:
                    pass

if __name__ == '__main__':
    if DEBUG:
        DebugApp()

    else:
        args_device['name']   = 'Licor820'
        args_device['port']   = PORT[0]
        args_device['device'] = DEVICE[0]
        devices.append(deepcopy(args_device))

        args_device['name']   = 'Licor6262'
        args_device['port']   = PORT[1]
        args_device['device'] = DEVICE[2]
        devices.append(deepcopy(args_device))

        AgusApp().run()
