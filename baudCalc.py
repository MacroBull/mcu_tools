#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:36:57 2013
Project	:baudrate calculate
Version	:0.0.1
@author	:macrobull

"""
mctlTable = [
	"00000000", "00000010", "00100010", "00101010",
	"10101010", "10101110", "11101110", "11111110"
	]

import sys
if (len(sys.argv)<2):
	print('Usage: baudCalc.py freq baud')
	exit()

freq = float(sys.argv[1])
baud = int(sys.argv[2])
print("Clock={}Hz, Baudrate={}\n".format(freq, baud))

br1= int((freq / baud) / 256)
freq = freq / baud % 256
br0= int(freq)
mctl= int(round(8 * (freq - br0)))

print("UCA0BR0 = {};".format(br0))
print("UCA0BR1 = {};".format(br1))
print("UCA0MCTL = UCBR{};".format(mctl))
print("\n#define UCBR{} 0b{}".format(mctl,mctlTable[mctl]))
