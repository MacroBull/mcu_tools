#! /usr/bin/python

import serial,time


from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from macrobull.misc import serialChecker

baud=9600
intv=0.1

print("serial2sock\n")
dev=serialChecker(True, 'USB','AMA','ACM')
ser = serial.Serial(dev, baud, timeout=intv)
ser.flush()
ser.flushInput()
ser.flushOutput()
ser.close()

baud = 460800
intv = 0.1
timeOut = 1
port = 8888

ser = serial.Serial(dev, baud, timeout=intv)
print "dev={} baudrate={} port={}".format(dev, ser.getBaudrate(), port)

class s2s(Protocol):
	def __exit__(self):
		print "Halted"
		ser.close()

	def dataReceived(self, sockData):
		if not ser.isOpen(): ser.open()

		ser.write(sockData)


		time.sleep(intv)
		serData = ' ' + ser.read(1024)
		t = timeOut
		while serData[-1]!='\n':
			t -=intv
			time.sleep(intv)
			serData += ser.read(ser.inWaiting())
			if t<0: break
#		serData = ser.read(1024)
#		i = timeOut
#		while i>0:
#			#if ser.inWaiting():
#			if serData[-1]!='\n':
#				serData += ser.read(ser.inWaiting())
#				i = timeOut
#			i -= intv
#			time.sleep(intv)

		serData = serData[1:]
		self.transport.write(serData)

		print "====Input====\n{}\n\n====Output====\n{}\n\n".format(sockData, serData)


	def connectionMade(self):
		print "Connected"

	def connectionLost(self, reason):
		if not ser.isOpen():
			ser.close()
		print "Disconnected"


factory = Factory()
factory.protocol = s2s
reactor.listenTCP(port,factory)
reactor.run()

if ser: ser.close()

print('Exited')
