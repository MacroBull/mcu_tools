#! /usr/bin/python

import serial,time,sys

from macrobull.misc import serialChecker
#from macrobull.dynamicPlot import dynamicFigure,defaultProcFunc

ESC=range(0,0x20)+range(0x80,0x100)+[0x7f]

BUFFLEN=16

baud=9600
intv=0.5
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


dump=dumpall=False
for i,a in enumerate(sys.argv):
	if a.find('dump')>=0:
		dumpall=a=='dump-all'
		dump=True
		break

if dump:
	sys.argv.pop(i)
	print 'dump enabled'
	f=open('serial_dump.txt','w')

char_mode = False
for i,a in enumerate(sys.argv):
	if '-c' == a:
		sys.argv.pop(i)
		print("Text mode")
		char_mode = True

if len(sys.argv)>1:
	baud = float(sys.argv[1])

if len(sys.argv)>2:  intv = float(sys.argv[2])
if len(sys.argv)>3:  data = sys.argv[3]

ser = serial.Serial(dev, baud, timeout=intv)
print "dev={} baudrate={}".format(dev, ser.getBaudrate())

def glb(s, ml):
	if char_mode:
		for i in range(min(len(s), BUFFLEN)):
			if s[i] in rt:
				return i+1
	return BUFFLEN

buff=''
try:
	while 1:
		w=ser.inWaiting()
		if w:
			s=ser.read()
			buff+=s
			bl=glb(buff,BUFFLEN)
			while len(buff)>=bl:
				#print int(time.time()),': ',
				t=time.time()

				h = '{}.{:03}: '.format(int(t),int(t % 1 *1000))
				print h,
				if dumpall: f.write(h)
				
				s=buff[:bl]
				for c in ESC:
					s=s.replace(chr(c),'.')
				h=' '.join(['{:02x}'.format(ord(c)) for c in buff[:bl]])
				#h=' '.join([hex(ord(c))[2:].rjust(2) for c in buff[:bl]])
				print h,' '*(8+3*(BUFFLEN-bl)),s
				if dumpall: f.write('{}\t{}\n'.format(h,s))
				elif dump: f.write('{}\n'.format(s))
				buff=buff[bl:]

		else:
			ser.write(data)
			time.sleep(intv)

#except (KeyboardInterrupt, SystemExit):
except BaseException,e:
	print(e)

ser.close()
if dump: f.close()
print('Exited')
