''' create objects '''
import pygame, FpsClock, random, time, sys

class Character:
	''' A character is anything that is currently on the screen '''

	def __init__(self, icon, screen, x, y, delay=5):
		self._icon = pygame.image.load(icon)
		
		#location on screen
		self.set_position(x, y)
		self._screen = screen

		self._delay = delay
		self._delay_count = 0
		
		self._original_x = self._x
		self._original_y = self._y		

	def set_position(self, x, y):
		''' set the position of the character to x, y '''
		(self._x, self._y) = (x, y)

	def get_position(self):
		''' get the position of the character '''
		return (self._x, self._y)

	def get_icon(self):
		''' get the icon of the character '''
		return self._icon

	def is_dead(self):
		''' return if this character is dead '''
		return False

	def move(self, dx, dy):
		''' move the character in direction (dx, dy) '''
		self.set_position(self._x + dx, self._y + dy)

	def delay(self):
		''' speed relative to others '''
		self._delay_count = (self._delay_count+1) % self._delay
		return self._delay_count == 0

	def step(self):
		''' single step in the animation of the game '''
		# to implement in other classes
		pass


class Frog(Character):
	''' class for the player frog '''

	def __init__(self, icon, screen, x, y):
		Character.__init__(self, icon,screen ,x ,y )

	def handle_event(self, event):
		''' register the occurence of an event with self '''
		pass

class DummyFrog(Frog):
	''' A dummy frog is just a frog that is not controlled by the current player '''
	def __init__(self, icon, screen, x, y, pid=0):
		Frog.__init__(self, icon, screen, x, y)
		self.is_dead = False
		self._pid = pid

	def die(self):
		''' kill the dummy frog '''
		self.is_dead = True

	def move(self, dx, dy):
		''' set the position of the dummy frog '''
		self.set_position(dx, dy)

class PlayerFrog(Frog):
	''' A frog that handles actual keyboard events '''

	def __init__(self, icon, screen, x, y, pid=0):
		Frog.__init__(self, icon, screen, x, y)
		self._last_event = None # the last event player made
		self._is_dead = False
		self._pid = pid

	def handle_event(self, event):
		''' record the last event directed at this player '''
		self._last_event = event

	def die(self):
		''' kill this player '''
		self._screen.remove_player()
		self._screen.clear_time()
		
	def is_dead(self):
		''' check to see if the player frog is dead '''
		return self._is_dead

	def step(self):
		''' take a single step in animation '''

		if self.is_dead():
			return False # lolz im dead
		else:
			if self._last_event is not None:
				dx = None
				dy = None
				# log the last key event
				if self._last_event == pygame.K_UP:
					dx, dy = 0, -1
				if self._last_event == pygame.K_DOWN:
					dx, dy = 0, 1
				if self._last_event == pygame.K_RIGHT:
					dx, dy = 1, 0
				if self._last_event == pygame.K_LEFT:
					dx, dy = -1, 0

				if dx is not None and dy is not None:
					self.move(dx, dy)

				self._last_event = None

	def move(self, dx, dy):
		''' move the player frog to the new direction dx, dy '''
		new_x = self._x + dx
		new_y = self._y + dy

		# check for bounds here probably,
		if self._screen.is_in_bounds(new_x, new_y) == False:
			return False
		
		# also check whether if another object exists on
		# place im moving, and if there is.. then die
		anotherObj = self._screen.get_character(new_x, new_y)
		if isinstance(anotherObj, Clover):
			print("you win!")
			self._screen.set_winner(self._pid)
			Character.move(self, dx, dy)
			self.die();
			return True
		
		# make sure the frog doesnt step in the water
		if new_y < 9 and new_y > 0:
			if isinstance(anotherObj, LogRight) == False and isinstance(anotherObj, LogLeft) == False:
				self.die()
				return False
		
		if anotherObj is not None and isinstance(anotherObj, LogRight) == False and isinstance(anotherObj, LogLeft) == False and isinstance(anotherObj, DummyFrog) == False:
			self.die()
			return False

		#move
		Character.move(self, dx, dy)

class KillObj(Character):
	''' this will be a character that kills the frog '''

	def __init__(self, icon, screen, x, y, delay=5):
		Character.__init__(self, icon, screen, x, y, delay)

		#default movement is to the left
		self._dx = -1
		self._dy = 0

	def set_movement(self, dx, dy):
		''' set other movement, i.e. to the right '''
		self._dx = dx
		self._dy = dy

	def step(self):
		''' step the kill object '''
		if not self.delay(): return
		self.move(self._dx, self._dy)
		return True

	def move(self, dx, dy):
		''' move this object in a given direction '''
		new_x=self._x+dx
		new_y=self._y+dy

		# check for bounds here... cause we gotta put this
		# object back on the screen after it leaves
		
		if self._screen.is_in_bounds(new_x, new_y) == False:
			self.set_position(self._original_x, self._original_y)
		else:
			# check to see if we're going to kill player
			isPlayer = self._screen.get_player_place()
			if isPlayer is not None:
				if isPlayer[0] == new_x and isPlayer[1] == new_y:
					self._screen._player.die()
				
				else:
					Character.move(self, dx, dy)
			
class Log(KillObj):
	''' A Log is just a kill object that doesn't kill '''
	def __init__(self, icon, screen, x, y, delay=5):
		KillObj.__init__(self, icon, screen, x, y, delay)
		
	def isFrogOnMe(self, x, y):
		''' return true if the frop is on this particular position, false otherwise '''
		objects = self._screen.get_characters()
		for o in objects:
			if isinstance(o, PlayerFrog):
				if o.get_position()[0] == x and o.get_position()[1] == y:
					return True
		return False
		
	def move(self, dx, dy):
		''' move the log in the given direction '''
		new_x=self._x+dx
		new_y=self._y+dy
	
		# check for bounds here... cause we gotta put this
		# object back on the screen after it leaves
		
		if self._screen.is_in_bounds(new_x, new_y) == False:
			self.set_position(self._original_x, self._original_y)
			if self._screen._player is not None:
				if self._screen._player.get_position()[1] < 9 and self._screen._player.get_position()[1] > 0 and self._screen.is_player_on_log() == False:
					self._screen._player.die()			
		else:
			# check to see if we're going to kill player
			#move the player with me
			if self.isFrogOnMe(self._x, self._y):
				Character.move(self._screen._player, dx, dy)

			Character.move(self, dx, dy)

class LogRight(Log):
	''' This log moves from right to left '''
	def __init__(self, icon, screen, x, y, delay=5):
		KillObj.__init__(self, icon, screen, x, y, delay)
		self._original_x = 19	

class LogLeft(Log):
	''' This log moves from the left to the right '''
	def __init__(self, icon, screen, x, y, delay=5):
		KillObj.__init__(self, icon, screen, x, y, delay)
		self._original_x = 0
		self.set_movement(1,0)
		
class TrafficLeft(KillObj):
	''' This will be the traffic that will move from right to left '''
	def __init__(self, icon, screen, x, y, delay=5):
		KillObj.__init__(self, icon, screen, x, y, delay)
		self.set_movement(1, 0)
		self._original_x = 0
		
		
class TrafficRight(KillObj):
	''' Traffic that moves from left to right '''
	def __init__(self, icon, screen, x, y, delay = 5):
		KillObj.__init__(self, icon, screen, x, y, delay)
		self.set_movement(-1, 0)
		self._original_x = 19

class Clover(Character):
	''' A Clover is an object that is stationary '''
	def __init__(self, icon, screen, x, y):
		Character.__init__(self, icon,screen ,x ,y )
		
	def step(self):
		''' does not step '''
		return False
	
	def move(self):
		''' does not move '''
		return False
		

class Screen:
	''' A screen is the main game area where all the game elements live '''
	def __init__(self, width, height, icon_dim, timer):
		self._characters = [] # list of characters
		self._dummies = [] # list of dummy characters
		self._player = None
		self._winner = None # keep track of the winner

		self._width, self._height = width, height
		self._icon_dimension=icon_dim

		self._pixel_width = self._icon_dimension * self._width
		self._pixel_height = self._icon_dimension * self._height
		self._pixel_size = self._pixel_width, self._pixel_height

		self._screen = pygame.display.set_mode(self._pixel_size)
		self._timer = timer

	def is_in_bounds(self, x,y):
		''' returns if stage is in bounds. '''
		return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

	def is_in_bounds_x(self, x):
		''' returns if x is in bounds of the width of the stage. '''
		return 0<=x and x<self._width
	
	def clear_time(self):
		''' clear the timer '''
		self._timer.end()

	def is_in_bounds_y(self, y):
		''' returns if y is in bounds of the height of the stage. '''
		return 0<=y and y<self._height

	def get_width(self):
		return self._width

	def get_height(self):
		return self._height

	def set_player(self, player):
		''' set the player '''
		self._player = player
		self.add_character(self._player)

	def remove_dummy(self, pid):
		''' remove the dummy based on the player id '''
		if self.s._dummies[0]._pid == pid:
			#self.remove_character(self.s._dummies[0])
			self._characters.remove(self.s._dummies[0])
			self._dummies.remove(self.s._dummies[0])
		else:
			self._characters.remove(self.s._dummies[1])
			self._dummies.remove(self.s._dummies[1])

	def remove_player(self):
		''' remove the player '''
		self.remove_character(self._player)
		self._player = None

	def player_event(self, event):
		if self._player is not None:
			self._player.handle_event(event)

	def add_character(self, char):
		''' add the character to the list '''
		self._characters.append(char)

	def add_dummies(self, char):
		''' add the dummy to the list '''
		self._dummies.append(char)
		self._characters.append(char)

	def remove_character(self, char):
		''' remove character from list '''
		self._characters.remove(char)

	def get_characters(self):
		''' return the list of characters '''
		return self._characters

	def get_character(self, x, y):
		''' return character at x, y '''
		if self._player is not None:
			for a in self._characters:
				if a.get_position() == (x,y):
					return a
		return None
	
	def get_player_place(self):
		''' get the player's position '''
		if self._player is not None:
			return self._player.get_position()
	
	def is_player_on_log(self):
		''' return true if player is on a log, false otherwise '''
		if self._player is not None:
			player_pos = self._player.get_position()
			for a in self._characters:
				if a.get_position()[0] == player_pos[0] and a.get_position()[1] == player_pos[1]:
					if isinstance(a, LogRight) or isinstance(a, LogLeft):
						return True
				
		return False

	def step(self):
		''' step all the characters '''
		if self._player is not None:
			for a in self._characters:
				a.step()

	def set_winner(self, pid):
		''' set the winner to the pid given '''
		self._winner = pid

	def draw(self):
		''' draw an instance of the game on the screen '''
		self._screen.fill((0,0,0))
		khaki = (189, 183, 107)
		blue = (30, 144, 255)
		red = (255, 0, 0)
		d = self._icon_dimension
		#start platform
		pygame.draw.rect(self._screen, khaki, (0, 19 * d, 600, 25))
		
		#middle platform
		pygame.draw.rect(self._screen, khaki, (0, 9 * d, 600, 25))
		
		#end platform
		pygame.draw.rect(self._screen, khaki, (0, 1 * d, 600, 25))

		#river
		pygame.draw.rect(self._screen, blue, (0, 2 * d, 600, 25))
		pygame.draw.rect(self._screen, blue, (0, 3 * d, 600, 25))
		pygame.draw.rect(self._screen, blue, (0, 4 * d, 600, 25))
		pygame.draw.rect(self._screen, blue, (0, 5 * d, 600, 25))
		pygame.draw.rect(self._screen, blue, (0, 6 * d, 600, 25))
		pygame.draw.rect(self._screen, blue, (0, 7 * d, 600, 25))
		pygame.draw.rect(self._screen, blue, (0, 8 * d, 600, 25))

		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(str(self._timer.get_frame_duration()), 1, (255,255,0))
		self._screen.blit(label, (0, 7))
		
		for a in self._characters:
			icon = a.get_icon()
			if a is not None:
				(x,y) = a.get_position()
			d = self._icon_dimension
			rect = pygame.Rect(x*d, y*d, d, d)
			self._screen.blit(icon, rect)

		pygame.display.flip()
		
		if self._player is None and len(self._dummies) == 0:
			return False
		