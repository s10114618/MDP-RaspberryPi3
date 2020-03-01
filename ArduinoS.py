import serial
import time

class SC(object):
	def serialWrite(self, msg, ser):
		msg = msg+'\n'
		ser.write((str(msg).encode('UTF-8')))

	def serialRead(self, ser):
		read_serial=ser.readline()
		return read_serial
