"""a text entry box for pygame
by Jordan Ogilvy, 26/11/2015"""
#can specify size, background colour, font etc
#has a method to retrieve the content of the text box as a string

import pygame


class Entry:
	"""An entry box widget for entering text input in pygame"""
	def __init__(self, display, position, width=100, font="Helvetica", fontsize=12, default_text = "Hello World!", \
						fontcolor = (0,0,0), background = (255,255,255), border = (0,0,0), activeborder = (0,100,255), borderwidth = 1, \
						frames_per_blink = 15):
		#display is the pygame surface the entry box will be drawn on, usually the main game display.
		self.display = display
		#position is a tuple (x,y) representing the co ordinates of the entry box's TOP LEFT CORNER.
		self.position = position
		#Font is only the name of the font, as a string. 
		self.font = font
		self.fontsize = fontsize
		#width and height of the entry box in pixels
		self.width = width
		self.height = self.fontsize * 2
		#font color, border, activeborder, and background, are RGB tuples (R, G, B)
		self.fontcolor = fontcolor
		self.background = background
		self.border = border
		self.activeborder = activeborder
		#width in pixels of border around edge of entry box. 0 is no border.
		self.borderwidth = borderwidth
		#default_text is the text that will be written in the entry box when it is created.
		self.default_text = default_text
		#whether the entry box is currently selected to type in or not.
		self.active = False
		#the current contents of the entry box. When initialised, it will be the default text.
		self.__current_input = self.default_text
		#the position the cursor/ "|" thing is currently at, i.e the INDEX of current_input that the next letter will be inserted to.
		self.__bar_position = len(self.__current_input)
		self.__bar_blink_timer = 1
		self.__show_blinker = True
		self.frames_per_blink = frames_per_blink
		#create a pygame font to use for the input text. Must be a recognised system font (for now)
		self.__input_font = pygame.font.SysFont(self.font, self.fontsize)
		#create a label to use for drawing the current input
		self.__input_label = self.__input_font.render(self.__current_input, 1, self.fontcolor)
		#width and height of the actual text to be drawn based on current_input. using "somy Text" so that they are not 0.
		self.__text_width, self.__text_height = self.__input_font.size("somy Text")
		#create a surface to draw the entry box on
		self.__surface = pygame.Surface((self.width, self.height))
		#(x,y) tuple co ordinates of the position to draw the BOTTOM LEFT of the text. Leaves a bit of whitespace by default.
		self.__text_position =  (self.borderwidth + 2, self.height//2 - self.__text_height//2.2 )
			
	def update(self, events):
		"""draw the entry box to the parent window/surface so it shows up.
		should be called from the game loop, before pygame.display.update()"""
		
		#get the current input of the entry box
		self.check_is_active(events)
		
		#update the input when the user types in the box
		if self.active:
			self.check_for_keystrokes(events)
		
		#draw the background first
		self.__surface.fill(self.background)
		
		#draw the border. If border = 0, the border wont show up. If the entry box is active, use the activeborder color instead.
		if self.borderwidth > 0:
			if self.active:
				color = self.activeborder
			else:
				color = self.border
			pygame.draw.rect(self.__surface, color, (0,0,self.width,self.height), self.borderwidth) 
		
		#draw the current text in the entry box
		self.__surface.blit(self.__input_label, (self.__text_position))
		
		#draw the text cursor/bar thing, only if the user is using the entry box
		if self.active:
			self.draw_bar()
		
		#blit the whole entry box to the parent surface, so it actually shows up
		self.display.blit(self.__surface, (self.position[0], self.position[1]))			
	
	def check_is_active(self, events):
		"""checks to see if the user is using the entry box, and changes self.active accordingly,
		so the input text can be edited."""
		for event in events:
			#when the user clicks/releases mouse click
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				
				#if the mouse was over the entry box when it was released
				if self.position[0]<mouse_x<self.position[0]+self.width and self.position[1]<mouse_y<self.position[1]+self.height:
					self.active = True
					#move the cursor/bar thing to the nearest character it was clicked by
					self.move_bar_to_mouse(mouse_x)
					#allow repeated keys (first delay in milliseconds, every other delay interval in milliseconds)
					#This is done here so repeated keys are only enabled when using the text box. HOWEVER!!!!!!!!!,
					#repeated keys will need to be disabled outside of this widget.
					pygame.key.set_repeat(500, 40)
				else:
					self.active = False
					
		return self.active

	def check_for_keystrokes(self, events):
		"""Calls the update_current_input(new_character) function when a key is pressed, and 
		passes the appropriate character to insert it in the string shown in the entry box"""
		for event in events:
			if event.type == pygame.KEYDOWN:
				#if a key is pressed we want the cursor/bar thing to not blink and remain on the screen
				self.__bar_blink_timer = 0
				self.__show_blinker = True
				
				#if it was the backspace, call the backspace function
				if event.key == pygame.K_BACKSPACE:
					self.backspace()
				
				#if it was a left or right arrow, adjust the position of the text cursor bar thing accordingly
				elif event.key == pygame.K_LEFT:
					if self.__bar_position > 0:
						self.__bar_position -= 1
					
				elif event.key == pygame.K_RIGHT:
					if self.__bar_position < len(self.__current_input):
						self.__bar_position += 1
					
				#otherwise, insert the character given by the current keyboard state.	
				else:
					#event.unicode returns the character that will be output given the current state of the keyboard,
					#e.g it already takes into consideration caps lock, shift, etc
					c = event.unicode
					acceptables = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-`,./\<>?;':\"|[]{}"
					#insert the key, c,  to the input text, if it is in the acceptable characters string.
					if c in acceptables and len(c)!=0:
						self.update_current_input(c)
		
	def update_current_input(self, new_character):
		"""change the input string in the entry box and its label to reflect the addition of the new character"""
		
		#new_character is inserted at current_string[self.__bar_position].
		#if bar position is out of index range, append it to the string.
		try:
			self.__current_input = self.__current_input[:self.__bar_position] + new_character + self.__current_input[self.__bar_position:]
		except IndexError:
			self.__current_input = self.__current_input + new_character
			
		self.__bar_position += 1	
		self.__input_label = self.__input_font.render(self.__current_input, 1, self.fontcolor)
		
	def backspace(self):
		"""delete a character from the current input string and re create the text label for drawing"""
		#if trying to backspace at the start of the word, do nothing
		if self.__bar_position == 0:
			return
		#if backspacing at the end, remove the last character
		elif self.__bar_position >= len(self.__current_input):
			self.__current_input = self.__current_input[:-1]
		else:
			self.__current_input = self.__current_input[0:self.__bar_position-1] + self.__current_input[self.__bar_position:]
		
		#dont let bar_position be less than 0
		if self.__bar_position < 0:
			self.__bar_position = 0
			
		#move the bar back one index	
		self.__bar_position-=1
		#update the label to reflect the new input string
		self.__input_label = self.__input_font.render(self.__current_input, 1, self.fontcolor)
		
	def draw_bar(self):
		"""draw the bar thing that indicates where the next bit of text will be typed/inserted"""
		
		#update the timer so that the bar will blink on and off
		self.__bar_blink_timer += 1
		#the frames_per_blink is 15 by default - it could be changed to be dependent on the games frames per second
		#that would be more ideal I think, but for 30 fps, a max of 15 frames per blink is fine
		if self.__bar_blink_timer >= self.frames_per_blink:
			self.__bar_blink_timer = 0
			self.__show_blinker = not self.__show_blinker
			
		#only draw the bar if it is not currently blinking off 
		if self.__show_blinker:
			#get the height and more importantly the distance of the current input text to the bar
			text_to_bar, self.__text_height = self.__input_font.size(self.__current_input[:self.__bar_position])
			
			#The bar will be drawn immediately to the RIGHT of the character it shares an index with
			pygame.draw.line(self.__surface, self.fontcolor, (self.__text_position[0]+text_to_bar, self.height//2+self.__text_height//2),
										(self.__text_position[0]+text_to_bar, self.height//2-self.__text_height//2), 1)
										
	def move_bar_to_mouse(self, mouse_x):
		"""Gets given the position of the mouse when inside the entry box, and moves the bar to the character nearest the mouse
		"""
		self.__text_width, self.__text_height = self.__input_font.size(self.__current_input)
		#mouse_x is its x position on the display, i.e it is absolute, not relative to the entry box
		
		#we want the bar to be visible when clicked, so reset its timer
		self.__bar_blink_timer = 0
		self.__show_blinker = True
		
		#if the mouse is pressed and the entry box is empty
		if len(self.__current_input) == 0:
			self.__bar_position = 0
			
		#if the mouse is pressed after all of the text
		elif mouse_x > self.position[0] + self.__text_position[0] + self.__text_width - self.__input_font.size(self.__current_input[-1])[0]:
			self.__bar_position = len(self.__current_input)
		
		#otherwise the mouse is pressed somewhere in the middle of the text
		else:
			#basically finds the nearest gap in between two characters to the mouse and moves the bar to that index.
			#NTS: may pay to find a more efficient method of this. Could be cumbersome with long lines of text
			#FIX NOT WORKING FOR SECOND TO LAST INDEX ARGH
			for i in range(0, len(self.__current_input)):
				w, h = self.__input_font.size(self.__current_input[:i])
				if mouse_x < self.position[0] + self.__text_position[0] + w:
					a, b = self.__input_font.size(self.__current_input[:i-1])
					if abs(mouse_x - (self.position[0] + self.__text_position[0] + w)) < abs(mouse_x - (self.position[0] + self.__text_position[0] + a)):
						self.__bar_position = i
					else:
						self.__bar_position = i - 1
					return
	
	def get_input(self):
		return self.__current_input
		
		
#AN EXAMPLE WITH TWO ENTRIES, FEEL FREE TO ADD SOME MORE
if __name__ == "__main__":
	window_width = 500
	window_height = 500
	my_display = pygame.display.set_mode((window_width, window_height))
	my_clock = pygame.time.Clock()
	pygame.init()
	myentry = Entry(my_display, (50, 10), fontsize = 16, width = 200)
	myentry2 = Entry(my_display, (50, 70), fontsize = 24, border = 3, width = 350, default_text = "")
	exited = False
	while not exited:
		events = pygame.event.get()
		for event in events: 
			#quit event
			if event.type == pygame.QUIT:
				exited = True

		#redraw the display for this frame		
		my_display.fill((100,0,50))
		myentry.update(events)
		myentry2.update(events)
		pygame.display.update()
	 # how many frames per second we want
		my_clock.tick(30)
		
	pygame.quit() #quits when the game loop is broken
