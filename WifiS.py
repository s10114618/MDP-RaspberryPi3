import socket 
import time 
import sys 

class PcAPI(object):
        def __init__(self):
                self.tcp_ip = "192.168.200.11" # RPI IP address
                self.port = 8080
                self.conn = None
                self.client = None
                self.addr = None
                self.pc_is_connect = False
                self.buffer = ''
                
        def close_pc_socket(self):
                if self.conn:
                        self.conn.close()
                        print ("Closing server socket")
                if self.client:
                        self.client.close()
                        print ("Closing client socket")
                self.pc_is_connect = False
                
        def pc_is_connected(self):
                return self.pc_is_connect
        def init_pc_comm(self):
                # Create a TCP/IP socket
                
                try:
                        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #important to allow reuse of IP
                        self.conn.bind((self.tcp_ip,self.port))
                        self.conn.listen(1) #Listen for incoming connections
                        print ("Listening for incoming connections from PC...")
                        (self.client, self.addr) = self.conn.accept()
                        print ("Connected! Connection address: ",self.addr)
                        self.pc_is_connect = True
                except Exception as e : #socket.error:
                        print ("\nError: %s" % str(e))

        def write_to_PC(self, message):
                self.client.sendto(str(message+'\n').encode('UTF-8'),self.addr)

        def read_from_PC(self):
                    while not '\n' in self.buffer:
                            self.buffer += self.client.recv(2048).decode('utf-8')
                    line, self.buffer = self.buffer.split('\n', 1)
                    return line
