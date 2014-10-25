from Observer import Observer
import socket
from PlayerHandler import PlayerHandler

class GameServer(Observer):

	def __init__(self, address, port, limitPlayers):
		'''Initialize the GameServer with the ip address, port that it 
		will run on and number of players the game can support.'''

		self.address = (address, port)
		self.port = port
		self.limitPlayers = limitPlayers
		self.players = []
		self.sock = None

	def setup(self):
		'''Setup the server socket connection'''
		#create a new socket for this server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#bind the server to the address supplied
		self.sock.bind(self.address)
		#set the connection to listen for upto 5 connections
		self.sock.listen(5)

	def run(self):
		'''Starts the game server'''
		
		#setup the server socket to start listening
		self.setup()

		print('FROGGER SERVER RUNNING (' + str(self.address[0]) + ') CTRL+C TO SHUTDOWN.')

		#start listening for connectiongs
		while True:
		    try:
		        client, address = self.sock.accept()
		        print('PLAYER CONNECTED FROM: ', address)
		        
		        #create a new Player listener
		        newPlayer = PlayerHandler(client, self)

		        if len(self.players) >= self.limitPlayers:
		        	print("Limiting Players")
		        	newPlayer.close()
		        	continue

		        #listen in on player for state changes
		        #instantiate a handler to handle the player's connection
		        self.players.append(newPlayer)
		        print("Num players : " + str(len(self.players)))
		        #start the player handler thread
		        newPlayer.start()	
		        #introduce players to this new player i.e. if there are any
		        self.introduce(newPlayer)

		    except KeyboardInterrupt as e:
		    	#need to loop over all PlayerHandlers and safely kill them
		        print("RECEIVED CTRL+C, SHUTTING DOWN...")
		        for ph in self.players:
		        	ph.join()
		        break

		#shutdown the server        
		self.sock.close()

	def introduce(self, player):
		'''Introduce this player to the others in the world'''
		for p in self.players:
			if p is not player:
				print(str(p.getPid()) + " is observing " + str(player.getPid()))
				#make the other players listen in on this new player
				player.addObserver(p)
				#tell this player to listen to the others
				p.addObserver(player)

	def removePlayer(self, player):
		'''When a player disconnects, this will remove all their 
		observers and also each player will stop notifying them
		if there are players'''
		for p in self.players:
			if p is not player:
				p.removeObserver(player)

		self.players.remove(player)
		player.removeObservers()

		#reduce the player count
		print(player.getName() + " has DC, "  + str(len(self.players)) + " plyrs remaining")

if __name__ == "__main__":
	s = GameServer(socket.gethostbyname(socket.gethostname()), 1337, 3)
	s.run()