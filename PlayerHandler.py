import socket
from queue import Queue
from threading import Thread
from Observable import Observable
from Observer import Observer
from Command import *

class PlayerHandler(Thread, Observable, Observer):
    '''Thread that will handle communication with 
    each individual Client in the game world'''

    #autoincrementing player id
    PID=0

    def __init__(self, sock, server):
        '''Initialize a new PlayerHandler to communicate with the client's
        game engine'''
        #create a new Thread to handle this Player's Communication
        Thread.__init__(self, name="PlayerHandler"+str(PlayerHandler.PID))
        #initialize the parent
        Observable.__init__(self)
        #assign our unique ID
        self.pid = PlayerHandler.PID
        #increment the PID for the next player
        PlayerHandler.PID+=1
        #my name
        self.playerName = 'BOB'
        #server instance
        self.server = server
        #the socket connection for this Player
        self.sock = sock
        #data to be sent down the socket
        self.data = None
        #ack the connection
        self.ack()

    def close(self):
        '''Close the socket connection'''
        self.sock.close()

    def disconnect(self):
        '''Disconnect the user from the World and send a Command
        notifying everyone that you left'''

        print("KILLING " + "(" + str(self.pid) + ")")
        self.data = DisconnectCommand.encode('DC', self.pid).encode()
        self.setChanged()
        self.notifyAll()
        self.server.removePlayer(self)
        self.close()

    def ack(self):
        '''Send an ACK to the client indicating the command was received'''
        self.sock.send(AckCommand.encode('ACK', self.pid).encode())

    def getPid(self):
        '''Return the Player id'''
        return self.pid

    def getName(self):
        '''Getter for the player name'''
        return self.playerName

    def parseName(self, cmd):
        '''Parse a command and detect if its a player name broadcast
        This is used to tell everyone what the name of the player is 
        that just joined i.e. instead of IDs'''
        cmd = Command.decode(cmd.decode())
        if cmd['CMD'].strip() == 'JOIN':
            self.playerName = cmd['pname'].strip()
            print(self.playerName + " joined")

    def parseTerm(self, cmd):
        '''Parse a command and detect if its a TERM signal indicating
        that a client has quit the game. This is needed
        to prevent broken pipe issies and perform a graceful shutdown of 
        the socket'''
        cmd = Command.decode(cmd.decode())
        if cmd['CMD'].strip() == 'TERM':
            self.disconnect()
            return True
        return False

    def run(self):
        '''TCP Echo handler, all incoming requests are handled here 
        and rebroadcasted to any Client Observers'''
        while True:
            clientData = self.sock.recv(2048)
            #if data has bee received
            if clientData:
                self.data = clientData
                #check if we need to get our name
                print("GOD DAMNnit server")
                print(clientData.decode())
                self.parseName(clientData)
                #detect if we need to close the connection
                if self.parseTerm(clientData):
                    break
                self.setChanged()
                #notify any listeners i.e. the server
                self.notifyAll()
                #ack the commandw
            else:
                self.disconnect()
                break;

    def update(self, player):
        '''When another Player in the game world sends a 
        state change (Command), this is the handler that 
        will get those updates'''
        if player.data is not None:
            self.sock.send(player.data)
            player.clearChanged()
            #player.data = None