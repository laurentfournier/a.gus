'''
    Terminal interface
    
    Written by Laurent Fournier, October 2016

    To-do :
    - 
'''

import os, sys, subprocess
import time, datetime
import serial
import argparse
import curses

    # screen.clear()              cls
    # screen.addstr("")           add text
    
screen = curses.initscr()

curses.noecho() 
curses.curs_set(0) 
screen.keypad(1)

def root():
    screen.addstr("1. Select probe\n")
    screen.addstr("2. Select number of data extractions\n")
    screen.addstr("3. Read logs\n\n")
    screen.addstr("H. Help\n")
    screen.addstr("Q. Quit\n")
    
def lvone():
    screen.addstr("1. Test 1\n")
    screen.addstr("2. Test 2\n")
    screen.addstr("3. Test 3\n\n")
    screen.addstr("H. Help\n")
    screen.addstr("P. Previous\n")
    screen.addstr("Q. Quit\n")

while True: 
    event = screen.getch() 
    root()

    if event is ord("1"): 
        lvone() 

    elif event is ord("q") or event is ord("Q"): 
        screen.clear() 
        break 

    elif event == ord("h") or event is ord("H"): 
        screen.clear() 
        screen.addstr("No help yet *_*") 
        
curses.endwin()

