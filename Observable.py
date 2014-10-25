from Observer import Observer

class Observable:
	'''Implementation of an Observable object'''

	def __init__(self):
		self.observers = []
		self.changed = False

	def addObserver(self, observer):
		'''Add observer if it is of type Observer. Return true on
		success, false otherwise'''
		if(isinstance(observer, Observer) and observer not in self.observers):
			self.observers.append(observer)
			return True
		return False

	def removeObserver(self, observer):
		'''Removes an Observer'''
		try:
			self.observers.remove(observer)
			return True
		except Exception as e:
			return False

	def removeObservers(self):
		self.observers = []

	def getObservers(self):
		return self.observers

	def notifyAll(self):
		'''Notifies all Observers listening on this object'''
		for o in self.observers:
			o.update(self)

	def notify(self, observer):
		'''Notifies the specific Observer of the change'''
		observer.update(self)

	def hasChanged(self):
		'''Return true if the object has changed, false otherwise'''
		return self.changed

	def setChanged(self):
		'''Set this object's state to changed'''
		self.changed = True

	def clearChanged(self):
		'''Set this object's state as unchanged'''
		self.changed = False

	def numObservers(self):
		'''Return the number of Observers listening'''
		return len(self.observers)