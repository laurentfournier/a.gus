# -*- coding: utf-8 -*-

'''
    Files IO managing and processing
    
    Written by Laurent Fournier, November 2016
'''

import os, sys, subprocess
import time, datetime

class fManager:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.pos  = []
    
    # Set an IO file pointer
    def open(self):
        self.fp = open(self.name, self.mode)
        
    # Close file pointer
    def close(self):
        self.fp.close()
    
    # Load whole data from a config file
    def cfg_loader(self):
        index    =  0
        subindex = -1
        lines    = self.fp.read().split('\n')
            
        for i in lines:
            if (index is len(lines)-1):
                break

            elif (i[0] is '['):
                self.pos.append([i[1:-1], -1])
                subindex += 1
                
            else:
                self.pos[subindex][1] += 1
                self.pos[subindex].append(i.split('=')[0].lower())
                
            index += 1                        
                
    # Write data to config file
    def set_cfg(self, mod, opt):
        todo
                
    # Determine position and get the data required
    def get_cfg(self, entry):
        buff = []
        
        for i in range(len(self.pos)):
            for j in range(len(self.pos[i])):
                if (self.pos[i][j] == entry):
                    j += 2
                    while (j is not len(self.pos[i])):
                        buff.append(self.pos[i][j])
                        j += 1
            
        return buff
    
'''
    Main program

fp = fManager('config/.cfg', 'r')
fp.open()
fp.cfg_loader()
print fp.get_cfg('li820read')
fp.close()
'''

