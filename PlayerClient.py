import socket
from threading import *
from Observable import Observable
from time import sleep
from Command import *

class PlayerClient(Thread, Observable):
	'''Blocking client that can be used to communicate
	with the server to send/receive data'''

	def __init__(self, playerName, address, port):
		Thread.__init__(self, name="PlayerClient-"+str(playerName))
		Observable.__init__(self)
		self.address = address
		self.port = port
		#initialize the socket that this player will use
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.playerName = playerName
		#data received from the server
		self.data = None
		#connect to the server
		self.connect()

	def connect(self):
		'''Allows a player to connect to a server'''
		self.sock.connect((self.address, int(self.port)))

	def getSocket(self):
		return self.sock

	def disconnect(self):
		self.send(TerminateCommand.encode('TERM'))

	def send(self, command):
		'''Send a specific command to the server'''
		self.sock.send(command.encode())

	def run(self):
		'''Blocking receive from the server that 
		is used for push notification to the Player'''

		while True:
			#blocking call to receive data
			self.data = self.sock.recv(2048);
			if self.data:
				print(self.playerName + '*******' + self.data.decode())
				#set changed since we received data
				self.setChanged()
				#notify any Observers
				self.notifyAll()
			else:
				print("Stopping " + self.playerName + " Client Listener")
				self.disconnect()
				break