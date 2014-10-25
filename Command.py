import json

class Command:
	'''Base class for basic Commands, this class should 
	be extended and overridden, not used independently'''
	
	@staticmethod
	def encode(cmd):
		'''Encode a string (cmd) into a proper 
		format the server will understand'''

	@staticmethod
	def decode(cmd):
		'''Decode a command returned from the server'''
		return json.loads(cmd)

class AckCommand(Command):
	'''Command sent from the server when a Player first connects'''
	def encode(cmd, pid):
		return json.dumps({"CMD" : cmd, 'pid' : str(pid)}) + "\r\n"

class TerminateCommand(Command):
	'''Command that issues a disconnect to the server so that it can 
	close the client socket'''
	def encode(cmd):
		return json.dumps({"CMD" : cmd}) + "\r\n"

class MoveCommand(Command):
	'''Command sent from a player to broadcast their current position'''
	def encode(cmd, dx, dy, pid):
		return json.dumps({"CMD" : cmd, 'dx':dx, 'dy':dy, 'pid':pid}) + "\r\n"

class MsgCommand(Command):
	'''Command sent from a player indicating their chat message'''
	def encode(cmd, pname, msg):
		return json.dumps({"CMD" : cmd, "pname" : pname, "msg" : msg}) + "\r\n"

class JoinCommand(Command):
	'''Command indicating a player has joined the game'''
	def encode(cmd, pid, playerName):
		return json.dumps({"CMD" : cmd, "pid" : pid, "pname" : playerName}) + "\r\n"

class PlayerExistCommand(Command):
	'''Command indicating that a player exists i.e. when a new player joins
	each player will send this to the new player telling them "WE EXIST" '''
	def encode(cmd, pid, playerName):
		return json.dumps({"CMD" : cmd, "pid" : pid, "pname" : playerName}) + "\r\n"

class DisconnectCommand(Command):
	'''Command to disconnect a user from the game'''
	def encode(cmd, pid):
		return json.dumps({"CMD" : cmd, "pid" : pid}) + "\r\n"

class PlayerDiedCommand(Command):
	'''Command indicating a player has died'''
	def encode(cmd, pid):
		return json.dumps({"CMD" : cmd, "pid" : pid}) + "\r\n"

class CountdownCommand(Command):
	'''Command issued from the Countdown timer i.e. this is used locally'''
	def encode(cmd, count):
		return json.dumps({"CMD" : cmd, "count" : count}) + "\r\n"

class EndCommand(Command):
    ''' Command used to end the game and declare a winner '''
    def encode(cmd, winnerPid):
        return json.dumps({"CMD" : cmd, "winnerPid" : winnerPid}) + "\r\n"
