#!/usr/bin/python
# demo.py - CMD Args Demo By nixCraft
import sys 
from time import sleep
from os import path as op
from subprocess import check_call, check_output
from glob import glob

# Get the total number of args passed to the demo.py
total = len(sys.argv)
 
# Get the arguments list 
cmdargs = str(sys.argv)
 
# Print it
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)

