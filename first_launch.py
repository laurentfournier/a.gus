'''
    Verify if everything is installed/created before 1st launch
    
    Written by Laurent Fournier, October 2016
'''

import os, sys
import datetime, time
import apt, pip


#-------------------------------------------------------------
#------------------ Create an object 'C-like' ----------------
#---------- Because there are no switch in Python ------------
#-------------------------------------------------------------

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall  = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True

        elif self.value in args:
            self.fall = True
            return True
        
        else:
            return False
        
        
#-------------------------------------------------------------
#--------------------- Define the cases ----------------------
#-------------------------------------------------------------

def setup(name, fType):
    for case in switch(fType):
        if case('apt'):
            os.system('sudo apt-get install -y ' + name)
            break
            
        if case('pip'):
            try:
                __import__(name)
            except ImportError:
                pip.main(['install', name])
            break

        if case('gar'):
            os.system('garden install ' + name)
            break

        if case('dir'):
            os.system('mkdir logs')
            break

        
#-------------------------------------------------------------
#--------------------------- Execute -------------------------
#-------------------------------------------------------------

if os.path.isfile(".cfg") is False:
    os.system('clear')    
    cache = apt.Cache()

    try:
        if cache['python-bs4'].is_installed is not True:
            setup('python-bs4', 'apt')
        
        if cache['python-lxml'].is_installed is not True:
            setup('python-lxml', 'apt')
            
        if cache['python-crontab'].is_installed is not True:
            setup('python-crontab', 'apt')
            
        if os.path.isdir("logs") is not True :
            setup('logs', 'dir')
            
        if os.system('pip list | grep Kivy | wc -l') is not 2:
            setup('Kivy', 'pip')
            setup('Kivy-Garden', 'pip')
            setup('graph', 'gar')

    except Exception as e:
        print ("ERROR: {}".format(e))

    os.mknod(".cfg")
