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

baud = 9600
intv = 0.05
port = 8888

#try:
#	ser = serial.Serial(dev, baud, timeout=intv)
#	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	sock.bind(('', port))
#	sock.settimeout(sockTOut)
#	print "dev={} baudrate={} port={}".format(dev, ser.getBaudrate(), port)
#
#	conn = listenSock(sock)
#
#	while 1:
#		sockData = serData = ''
#		status = 1
#		try:
#			while ser.inWaiting():
#				serData += ser.read(1)
#			sockData = conn.recv(1024)
#			if sockData: status = 0
#		except BaseException:
#			status = 2
#
#		#print "{}:{}:{},{}".format(time.time(), status, serData, sockData)
#		print "{}:{}:{},{}".format(conn.getpeername(), status, serData, sockData)
#		if status == 1:
#			conn = listenSock(sock)
#
#		ser.write(sockData)
#		conn.sendall(serData)


class s2s(Protocol):
	def __exit__(self):
		print "Halted"
		ser.close()

	def dataReceived(self, sockData):
		if not ser.isOpen(): ser.open()

		ser.write(sockData)
#		while not serData:
#			while ser.inWaiting():
#				serData += ser.read(10)
		serData = ser.read(1024)
		serData += ser.read(ser.inWaiting())

		self.transport.write(serData)

		print "====Input====\n{}\n\n====Output====\n{}\n\n".format(sockData, serData)


	def connectionMade(self):
		print "Connected"
		ser = serial.Serial(dev, baud, timeout=intv)
		print "dev={} baudrate={} port={}".format(dev, ser.getBaudrate(), port)

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
