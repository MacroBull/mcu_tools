#! /usr/bin/python

import serial,time,sys, socket

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
intv = 0.01
sockTOut = 0.2
port = 8886


def listenSock(s):
	s.listen(1)
	e = 1
	while e:
		try:
			e = None
			conn, addr = s.accept()
		except BaseException, e:
			pass

	conn.settimeout(sockTOut)
	print 'Connected by', addr
	return conn

try:
	ser = serial.Serial(dev, baud, timeout=intv)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('', port))
	sock.settimeout(sockTOut)
	print "dev={} baudrate={} port={}".format(dev, ser.getBaudrate(), port)

	conn = listenSock(sock)

	while 1:
		sockData = serData = ''
		status = 1
		try:
			while ser.inWaiting():
				serData += ser.read(1)
			sockData = conn.recv(1024)
			if sockData: status = 0
		except BaseException:
			status = 2

		#print "{}:{}:{},{}".format(time.time(), status, serData, sockData)
		print "{}:{}:{},{}".format(conn.getpeername(), status, serData, sockData)
		if status == 1:
			conn = listenSock(sock)

		ser.write(sockData)
		conn.sendall(serData)



except BaseException, e:
	print e

try:
	conn.close()
	sock.close()
except NameError:
	pass

ser.close()


print('Exited')
