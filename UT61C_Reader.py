#! /usr/bin/python

import serial,time,sys
from numpy import NaN, log2, nan

from macrobull.misc import serialChecker
from macrobull.dynamicPlot import dynamicFigure,defaultProcFunc

ESC=range(0,0x20)+range(0x80,0x100)+[0x7f]

BUFFLEN=14

baud=9600
intv=0.5

rt = [ '\n','\r' ]

def ut61_parse(s):
	try:
		v=float(s[-6:-1])
	except ValueError,e:
		v=NaN

	u=''

	t = ord(s[1])
	if t & 0x04: u += '\Delta '

	'''
	t = ord(s[2])
	if t & 0x02: u +='n'

	t = ord(s[3])
	if t & 0x80: u +='\mu '
	elif t & 0x40: u +='m'
	elif t & 0x20: u +='k'
	elif t & 0x10: u +='M'
	elif t & 0x02: u +='%'
	'''

	if not(v is NaN):

		t = ord(s[0]) - 0x30
		if t: v*=10**(log2(t)-3)

		t = ord(s[2])
		if t & 0x02: v *=1e-9

		t = ord(s[3])
		if t & 0x80: v *=1e-6
		elif t & 0x40: v *=1e-3
		elif t & 0x20: v *=1e3
		elif t & 0x10: v *=1e6
		#elif t & 0x02: v *=1e-2
		elif t & 0x02: u +='\% Duty'

	t = ord(s[4])
	if t & 0x80: u +='V'
	elif t & 0x40: u +='A'
	elif t & 0x20: u +='\Omega '
	elif t & 0x08: u +='Hz'
	elif t & 0x04: u +='F'
	elif t & 0x02: u +='\degree C'
	elif t & 0x01: u +='\degree F'


	u += ' '

	t = ord(s[1])
	if t & 0x10: u += '(DC)'
	elif t & 0x08: u += '(AC)'

	return (v,r'$'+u+r'$')

def run(fs):
	global ser, buff
	w=ser.inWaiting()
	while w:

		s=ser.read()
		buff+=s
		while len(buff)>=BUFFLEN:
			#=time.time()
			#h = '{}.{:03}: '.format(int(t),int(t % 1 *1000))

			s=buff[:BUFFLEN]

			(v,u)=ut61_parse(s)
			#print(v is NaN)
			if not(v is NaN):
				df.appendData([v],u)

			for c in ESC:
				s=s.replace(chr(c),'.')
			h=' '.join(['{:02x}'.format(ord(c)) for c in buff[:BUFFLEN]])
			print h,'\t',s,'\t',v,'\t',u
			buff=buff[BUFFLEN:]


		w=ser.inWaiting()


print("serialReader baud=2400 intv=0.5 \n")
#dev=serialChecker(True,'USB')#,'AMA','ACM')
dev=serialChecker(True, 'USB','AMA','ACM')
ser = serial.Serial(dev, baud, timeout=intv)
ser.flush()
ser.flushInput()
ser.flushOutput()
ser.close()

baud=2400

if len(sys.argv)>1:
	baud = float(sys.argv[1])

if len(sys.argv)>2:  intv = float(sys.argv[2])

ser = serial.Serial(dev, baud, timeout=intv)
print "dev={} baudrate={}".format(dev, ser.getBaudrate())

buff=''
while 1:
	w=ser.inWaiting()
	if w:
		s=ser.read()
		if s==' ': break
	else:
		time.sleep(intv)


df=dynamicFigure(updateInterval=intv*1000,screenLen=20)
#df.keyHandler=pause
df.newData=run


try:
	df.run()
except BaseException,e:
	print(e)

ser.close()
print('Exited')
