from ArduinoS import *
from BlueToothS import *
from  WifiS import *
import serial
import time
from timeit import default_timer as timer
from threading import *
import re
import gc

def recvBluez(): # Send from bluetooth
	print ("start recvbluez")
	while 1:
		start_time = 0
		start_time = timer()
		msg = bluez.blueRecev().decode("utf-8")
		print("Message:'"+ msg +"' was sent from Bluez")
		pc.write_to_PC(("AN.*"+ msg))
		print ("Message:'"+ msg +"' was sent to wifi. Time Taken:" + str(timer()-start_time) + "s")


def recvWifi(): #Send from wifi
	print ("start recwifi ")
	while 1:
		start_time = 0
		start_time = timer()
		msg = pc.read_from_PC()
		print("Message:'"+ msg +"' was sent from Wifi")
		if re.match('AN.*', msg):
			bluez.blueSend(msg)
			print ("Message:'"+ msg +"' was sent to Bluetooth. Time Taken:" + str(timer()-start_time) + "s")
		else:
			serialz.serialWrite(msg,ser)
			print ("Message:'"+ msg +"' was sent to Serial. Time Taken:" + str(timer()-start_time) + "s")
					

def recvArduino(): #Send from Arduino
	print ("start recvarduino ")
	while 1:
		start_time = 0
		start_time = timer()
		msg = serialz.serialRead(ser)
		msg = msg.decode("utf-8")
		print ("Message:'"+ msg +"' was sent from Arduino ")
		msg = msg.replace('\r\n','')
		pc.write_to_PC(msg)
		print ("Message:'"+ msg +"' was sent to wifi " + str(timer()-start_time) + "s")


class Threading(object):
	def multiThreading(self):
		try:	
			t1 = Thread(target=recvBluez,name="t1")
			t2 = Thread(target=recvWifi,name="t2")
			t3 = Thread(target=recvArduino,name="t3")

			t1.start()
			t2.start()
			t3.start()
		except Exception as e:
			print (str(e))



if __name__ == "__main__":
	print('start main')

	ser = serial.Serial('/dev/ttyACM0', 115200)######
	serialz = SC()
	
	bluez = BT() #self initialise
	bluez.connect_bluetooth()
	
	pc = PcAPI()
	pc.init_pc_comm()
	
	thread = Threading()
	thread.multiThreading()

	

	
