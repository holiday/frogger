from threading import *
from Observable import *
from Command import *
import time

class Countdown(Thread, Observable):
	'''Countdown timer thread. Once the thread 
	has started, the timer will countdown and notify 
	any observers'''

	def __init__(self, seconds):
		Thread.__init__(self, name="Countdown")
		Observable.__init__(self)
		self.seconds = seconds
		self.data = None
		self.started = False

	def run(self):
		''' run the countdown timer and notify all the observers '''
		self.started = True
		while self.seconds >=0:
			#encode the seconds in a Command
			self.data = CountdownCommand.encode('COUNT', self.seconds).encode()
			self.setChanged()
			print(self.seconds)
			#notify all observers
			self.notifyAll()
			time.sleep(1)
			self.seconds-=1
