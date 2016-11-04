'''
    Files IO managing and processing
    
    Written by Laurent Fournier, Novembre 2016
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
        j        =  0
        lines    = self.fp.read().split('\n')
            
        for i in lines:
            print (index, i)
            
            if (index == len(lines)-1):
                break

            elif (i[0] is '['):
                self.pos.append([i[1:-1].lower(), index, -1])
                subindex += 1
                
            else:
                self.pos[subindex][2] += 1
                self.pos[subindex].append(i.split('=')[0].lower())
            index += 1                        
        
        while (j < len(self.pos[j])):
            del self.pos[j][self.pos[j][2]+3]
            j += 1
                            
        print (self.pos)
                
    # Write data to config file
    def cfg_write(self):
        todo
                
    # Determine position in the data loaded
    def search(self, entry):
        todo
        
'''
    Main program
    
'''

f = fManager('.cfg', 'r')
f.open()
f.cfg_loader()
f.close()
