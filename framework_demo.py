#! /usr/bin/python

import serial,time,sys
import json

from macrobull.misc import serialChecker
from macrobull.dynamicPlot import dynamicFigure,defaultProcFunc

ESC=range(0,0x20)+range(0x80,0x100)+[0x7f]

baud=9600
intv=0.1

rt = [ '\n','\r' ]


def run(fs):
	global ser, buff
	w=ser.inWaiting()
	while w:

		s=ser.read()
		if s=='\n':
			#print buff, '\n','\n'

			js = buff[buff.find('{'):]
			js = js[:js.find('}')+1]

			if js:
				obj = json.loads(js)
				for key in obj:
					if obj[key]>0:
						df.appendData([obj[key]], key, 111)

				buff =''
		else:
			buff+=s

		w=ser.inWaiting()

dev=serialChecker(True, 'USB','AMA','ACM')
ser = serial.Serial(dev, baud, timeout=intv)
ser.flush()
ser.flushInput()
ser.flushOutput()
ser.close()

ser = serial.Serial(dev, baud, timeout=intv)
print "dev={} baudrate={}".format(dev, ser.getBaudrate())

buff=''

w=ser.inWaiting()
while w:
	ser.read(16)
	w=ser.inWaiting()

df=dynamicFigure(updateInterval=intv*1000,screenLen=20)
#df.keyHandler=pause
df.newData=run


try:
	df.run()
except BaseException,e:
	print(e)

ser.close()
print('Exited')
