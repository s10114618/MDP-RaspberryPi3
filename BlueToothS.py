import subprocess
from bluetooth import *

class BT(object):

        def __init__(self):
                self.server_socket = None
                self.client_socket = None
                self.bt_is_connected = False


        def close_bt_socket(self):
                if self.client_socket:
                        self.client_socket.close()
                        print ("Closing client socket")
                if self.server_socket:
                        self.server_socket.close()
                        print ("Closing server socket")
                self.bt_is_connected = False


        def bt_is_connect(self):
                return self.bt_is_connected


        def connect_bluetooth(self):        
                btport = 4
                try:
                        self.server_socket = BluetoothSocket( RFCOMM )
                        self.server_socket.bind(("", btport))
                        self.server_socket.listen(1)    # Listen for requests
                        self.port = self.server_socket.getsockname()[1]
                        uuid = "00001101-0000-1000-8000-00805F9B34FB"

                        advertise_service( self.server_socket, "SampleServer",
                                           service_id = uuid,
                                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                                           profiles = [ SERIAL_PORT_PROFILE ],
			                   )
                        print ("Waiting for BT connection on RFCOMM channel %d" % self.port)
                        # Accept requests
                        self.client_socket, client_address = self.server_socket.accept()
                        print ("Accepted connection from ", client_address)
                        self.bt_is_connected = True

                except Exception as e:
                        print ("\nError: %s" %str(e))


        def blueSend(self, message):
                    self.client_socket.send(str(message))

                        
        def blueRecev(self):
                try:
                        return self.client_socket.recv(2048)

                except BluetoothError:
                        print ("\nBluetooth Read Error. Connection lost")
                        self.close_bt_socket()
                        self.connect_bluetooth()        # Reestablish connection

