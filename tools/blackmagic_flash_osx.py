#!/usr/bin/python
#
# Copyright (c) 2016 David "Buzz" Bussenschutt
# Distributed under the MIT License, available in the file LICENSE.
#
import os
import sys
import subprocess
from tempfile import *


# edit this to point ot your blackmagic probe....
blackm = "/dev/cu.usbmodemE2C5A4C1"

# if you run this from ./firmware then the ./firmware/build/*.elf should be there after a compile
elfpath = "build/"

import glob
elfs = glob.glob(elfpath+"*.elf")
first = ''
try:
	first = elfs[0]
except:
	print "No elf firmware found in "+elfpath
#print first

checksize = "arm-none-eabi-size "+first+" > /dev/null"
#print checksize
tmp = 1
try:
	tmp = subprocess.call(checksize,shell=True,stdout=None,stderr=None)
except:
	print "can't seem to find command: "+checksize
	sys.exit()

if tmp != 0:
	print "can't seem to execute command: "+checksize
	sys.exit()

fileh = NamedTemporaryFile(delete=False)

#print fileh.name

# gdb needs init file in current folder....
data = "target extended-remote "+blackm+"\nmon swdp_scan\nattach 1\nload\nkill\n"
#EOF
#f = open(filename, 'w')
fileh.write(data)
fileh.close()

try:
        tmp = subprocess.call("arm-none-eabi-gdb "+first+" --batch -x "+fileh.name,shell=True,stdout=None,stderr=None)
except:
        print "can't seem to do command: arm-none-eabi-gdb "+first+" --batch -x "+fileh.name
        sys.exit()
#
os.unlink(fileh.name)
