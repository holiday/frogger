''' run the game '''
import sys, pygame, random
from threading import *
from gameObjects import *
from FpsClock import *
from Observer import *
from Command import *
import time

class FroggerRun(Thread, Observer):
	def __init__(self, pid, dummy, listener):
		Thread.__init__(self, name="FroggerRun")
		self.listener = listener
		self.pid = pid
		self.dummy = dummy
		self.listener.addObserver(self)
		self._can_quit = False
		self._winner = None
		self._winner_pid = 0
		self.deadCount = 0
		self.sendCount = 0

		pygame.init()

		self.timer = FpsClock()

		self.s = Screen(20, 20, 24, self.timer)
		self.timer.begin()


        ##### PUT THE ELEMENTS ON THE SCREEN 
		self.s.add_character(TrafficLeft("images/car.png", self.s, 18, 17, 12))
		self.s.add_character(TrafficLeft("images/car.png", self.s, 17, 17, 12))
		self.s.add_character(TrafficLeft("images/car.png", self.s, 16, 17, 12))

		self.s.add_character(TrafficRight("images/car.png", self.s, 11, 16, 13))
		self.s.add_character(TrafficRight("images/car.png", self.s, 12, 16, 13))
		self.s.add_character(TrafficRight("images/car.png", self.s, 13, 16, 13))

		self.s.add_character(TrafficRight("images/car.png", self.s, 1, 16, 13))
		self.s.add_character(TrafficRight("images/car.png", self.s, 2, 16, 13))
		self.s.add_character(TrafficRight("images/car.png", self.s, 3, 16, 13))
		self.s.add_character(TrafficRight("images/car.png", self.s, 4, 16, 13))

		self.s.add_character(TrafficLeft("images/bike.png", self.s, 11, 15, 14))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 12, 15, 14))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 13, 15, 14))

		self.s.add_character(TrafficLeft("images/bike.png", self.s, 5, 15, 14))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 6, 15, 14))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 7, 15, 14))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 8, 15, 14))

		self.s.add_character(TrafficRight("images/car.png", self.s, 11, 14, 15))
		self.s.add_character(TrafficRight("images/car.png", self.s, 12,14 , 15))
		self.s.add_character(TrafficRight("images/car.png", self.s, 13,14 , 15))

		self.s.add_character(TrafficRight("images/car.png", self.s, 5, 14, 15))
		self.s.add_character(TrafficRight("images/car.png", self.s, 6, 14, 15))
		self.s.add_character(TrafficRight("images/car.png", self.s, 7, 14, 15))
		self.s.add_character(TrafficRight("images/car.png", self.s, 8, 14, 15))

		self.s.add_character(TrafficLeft("images/bike.png", self.s, 1, 13, 15))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 2,13 , 15))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 3,13 , 15))

		self.s.add_character(TrafficLeft("images/bike.png", self.s, 15, 13, 15))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 16, 13, 15))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 17, 13, 15))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 18, 13, 15))

		self.s.add_character(TrafficRight("images/car.png", self.s, 10, 12, 16))
		self.s.add_character(TrafficRight("images/car.png", self.s, 12,12 , 16))
		self.s.add_character(TrafficRight("images/car.png", self.s, 13,12 , 16))

		self.s.add_character(TrafficRight("images/car.png", self.s, 5, 12, 16))
		self.s.add_character(TrafficRight("images/car.png", self.s, 6, 12, 16))
		self.s.add_character(TrafficRight("images/car.png", self.s, 7, 12, 16))
		self.s.add_character(TrafficRight("images/car.png", self.s, 8, 12, 16))

		self.s.add_character(TrafficLeft("images/bike.png", self.s, 11, 11, 13))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 12, 11, 13))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 13, 11, 13))

		self.s.add_character(TrafficLeft("images/bike.png", self.s, 1, 11, 13))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 2, 11, 13))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 3, 11, 13))
		self.s.add_character(TrafficLeft("images/bike.png", self.s, 4, 11, 13))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 16, 8, 15))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 17, 8, 15))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 18, 8, 15))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 19, 8, 15))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 2, 8, 15))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 3, 8, 15))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 4, 8, 15))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 5, 8, 15))

		self.s.add_character(LogRight("images/log1.png", self.s, 12, 7, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 13, 7, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 14, 7, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 15, 7, 15))

		self.s.add_character(LogRight("images/log1.png", self.s, 2, 7, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 3, 7, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 4, 7, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 5, 7, 15))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 16, 6, 14))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 17, 6, 14))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 18, 6, 14))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 19, 6, 14))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 20, 6, 14))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 7, 6, 14))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 8, 6, 14))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 9, 6, 14))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 10, 6, 14))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 11, 6, 14))

		self.s.add_character(LogRight("images/log1.png", self.s, 16, 5, 13))
		self.s.add_character(LogRight("images/log2.png", self.s, 17, 5, 13))
		self.s.add_character(LogRight("images/log2.png", self.s, 18, 5, 13))
		self.s.add_character(LogRight("images/log2.png", self.s, 19, 5, 13))
		self.s.add_character(LogRight("images/log3.png", self.s, 20, 5, 13))

		self.s.add_character(LogRight("images/log1.png", self.s, 7, 5, 13))
		self.s.add_character(LogRight("images/log2.png", self.s, 8, 5, 13))
		self.s.add_character(LogRight("images/log2.png", self.s, 9, 5, 13))
		self.s.add_character(LogRight("images/log2.png", self.s, 10, 5, 13))
		self.s.add_character(LogRight("images/log3.png", self.s, 11, 5, 13))

		self.s.add_character(LogRight("images/log1.png", self.s, 3, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 4, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 5, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 6, 4, 16))
		self.s.add_character(LogRight("images/log3.png", self.s, 7, 4, 16))

		self.s.add_character(LogRight("images/log1.png", self.s, 10, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 11, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 12, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 13, 4, 16))
		self.s.add_character(LogRight("images/log3.png", self.s, 14, 4, 16))

		self.s.add_character(LogRight("images/log1.png", self.s, 15, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 16, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 17, 4, 16))
		self.s.add_character(LogRight("images/log2.png", self.s, 18, 4, 16))
		self.s.add_character(LogRight("images/log3.png", self.s, 19, 4, 16))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 16, 3, 12))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 17, 3, 12))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 18, 3, 12))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 19, 3, 12))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 1, 3, 12))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 2, 3, 12))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 3, 3, 12))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 4, 3, 12))

		self.s.add_character(LogLeft("images/log1stickypush.png", self.s, 10, 3, 12))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 11, 3, 12))
		self.s.add_character(LogLeft("images/log2stickypush.png", self.s, 12, 3, 12))
		self.s.add_character(LogLeft("images/log3stickypush.png", self.s, 13, 3, 12))

		self.s.add_character(LogRight("images/log1.png", self.s, 16, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 17, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 18, 2, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 19, 2, 15))

		self.s.add_character(LogRight("images/log1.png", self.s, 1, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 2, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 3, 2, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 4, 2, 15))

		self.s.add_character(LogRight("images/log1.png", self.s, 6, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 7, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 8, 2, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 9, 2, 15))

		self.s.add_character(LogRight("images/log1.png", self.s, 10, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 11, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 12, 2, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 13, 2, 15))

		self.s.add_character(LogRight("images/log1.png", self.s, 16, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 17, 2, 15))
		self.s.add_character(LogRight("images/log2.png", self.s, 18, 2, 15))
		self.s.add_character(LogRight("images/log3.png", self.s, 19, 2, 15))

		self.s.add_character(Clover("images/clover.png", self.s, 4, 1))
		self.s.add_character(Clover("images/clover.png", self.s, 8, 1))
		self.s.add_character(Clover("images/clover.png", self.s, 12, 1))
		self.s.add_character(Clover("images/clover.png", self.s, 16, 1))

		self.s.add_dummies(DummyFrog("images/dummyfrog.png", self.s, 9, 19, int(self.dummy[0])))
		self.s.add_dummies(DummyFrog("images/dummyfrog.png", self.s, 10, 19, int(self.dummy[1])))
		self.s.set_player(PlayerFrog("images/frog.png", self.s, 10, 19, int(self.pid)))


	def run(self):
		while self._can_quit == False:
			try:
				pygame.time.wait(10)
				if self.s._player is None:
					if self.s._winner is not None:
						# the game is over
						self.listener.send(EndCommand.encode('END', int(self.pid)))
					else:
						# the player is dead, so notify everyone else
						self.listener.send(PlayerDiedCommand.encode('DEAD', int(self.pid)))
					self.deadCount += 1
					self._can_quit = True
					print(self.deadCount)
					if self.deadCount == 3:
						# everyone's dead
						pygame.quit()
						sys.exit()
				else:

					# check to see if theres a winner
					if self.s._winner == None:
						
						for event in pygame.event.get():
							# if the game event is QUIT, then exit
							if event.type == pygame.QUIT:
								self._can_quit = True
								pygame.quit()
								sys.exit()

							if event.type == pygame.KEYDOWN:
								# On keydown, notify everyone of the move thats been made
								if self.s._player is not None:
									self.listener.send(MoveCommand.encode('MOVE', self.s._player.get_position()[0],self.s._player.get_position()[1], self.pid))
									self.s.player_event(event.key)

						self.s.step()

						if self.s.draw() != False:
							self.timer.tick()

					else: 
						# theres a winner, tell everyone
						self._winner_pid = int(self.pid)
						self._can_quit = True
						self.listener.send(EndCommand.encode('END', int(self.pid)))
						pygame.quit()
						sys.exit()
					
			except Exception as e:
				print(e)
				print("error found")
		
	def update(self, listener):
		''' Update this instance based on the command that is recieved '''		
		if listener.data is not None:
			commands = listener.data.decode().splitlines()
			for cmd in commands:
				cmd = Command.decode(cmd)
				if cmd["CMD"].strip() == "MOVE":
				    #HANDLE move
				    pid = cmd['pid']
				    dx = cmd['dx']
				    dy = cmd['dy']
				    if self.s._dummies[0]._pid == int(pid):
				    	# move the first dummy
				    	self.s._dummies[0].move(int(dx), int(dy))
				    else: 
				    	self.s._dummies[1].move(int(dx), int(dy))				   

				elif cmd["CMD"].strip() == "DEAD":
					pid = cmd["pid"]
					print(len(self.s._dummies))

					if self.s._dummies[0]._pid == pid:
					 	# this guy is dead
					 	self.s._characters.remove(self.s._dummies[0])
					 	self.s._dummies.remove(self.s._dummies[0])
					else:
					 	self.s._characters.remove(self.s._dummies[1])
					 	self.s._dummies.remove(self.s._dummies[1])
					
				elif cmd["CMD"].strip() == "END":
					# the game is over
					if self.sendCount == 0:
						winnerPid = cmd['winnerPid']
						self.winnerPid = winnerPid
						# send a notification again to notifiy the winner
						self.listener.send(EndCommand.encode('END', winnerPid))
						while(self._can_quit==False):
							time.sleep(0.005)
						pygame.quit()
						self.send
