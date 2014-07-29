#! /usr/bin/python

import serial,time,sys

from macrobull.misc import serialChecker, average

from macrobull.dynamicPlot import dynamicFigure,defaultProcFunc

ESC=range(0,0x20)+range(0x80,0x100)+[0x7f]

BUFFLEN=16

baud=9600
intv=0.05
data='H'

rt = [ '\n','\r' ]

print("serialReader [-c (for text mode)] baud=9600 intv=0.5 data='H'\n")
#dev=serialChecker(True,'USB')#,'AMA','ACM')
dev=serialChecker(True, 'USB','AMA','ACM')
ser = serial.Serial(dev, baud, timeout=intv)
ser.flush()
ser.flushInput()
ser.flushOutput()
ser.close()



if len(sys.argv)>1:
	baud = float(sys.argv[1])

if len(sys.argv)>2:  intv = float(sys.argv[2])
if len(sys.argv)>3:  data = sys.argv[3]

ser = serial.Serial(dev, baud, timeout=intv)
print "dev={} baudrate={}".format(dev, ser.getBaudrate())

buf = ''

def run(fs):
	global ser, buff
	w=ser.inWaiting()
	while w:
		s=ser.read(1)
		if s=='\n':
			dstr = buf.split(' ')
			d1, d2 = int(dstr[0], 16), int(dstr[1], 16)

			print dstr

			df.appendData([d1],'ch1', procFunc=[lambda x,y:average(5,x,y), lambda x,y:average(0,x,y) ], flotLabels = ['5sec', 'overall'])
			df.appendData([d2],'ch2', procFunc=[lambda x,y:average(5,x,y), lambda x,y:average(0,x,y) ], flotLabels = ['5sec', 'overall'])
			buf = ''
		else:
			buf = buf+s
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
