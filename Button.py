import pygame
import os

#HOW IT WORKS
#Create the button in a Scene class and add it to the scenes button list
#THe scene will take care of checking if it is pressed, hovered over, etc
#However this may (and should) change.


class Button:
	"""A Button widget for pygame. Draws user specified text over custom sprites, 
	and calls a function when it is pressed."""
	def __init__(self, display, position, normal, depressed, hover, message, action, fontcolor = (0,0,0), font = "Helvetica"):
		#the pygame display the button is on, usually the main game display/window
		self.display = display
		#state indicates whether the button is currently pressed down or not, or if the mouse is hovering over it.
		self.normal_image = normal
		self.depressed_image = depressed
		self.hover_image = hover
		#the button state is either "normal", "hover", or "pressed"
		self.state = "normal"
		self.current_state_sprite = self.normal_image
		self.directory = os.path.dirname(os.path.abspath(__file__)) 
		self.sprite= pygame.image.load(self.current_state_sprite)
		#font for the text, the text must be blitted in the game loop
		self.fontcolor = fontcolor
		self.font = font
		self.button_font = pygame.font.SysFont(self.font, self.sprite.get_height()//3)
		#position is a tuple (x,y), x and y give the co ordinates of the TOP LEFT CORNER of the button
		#top left corner of screen is (0,0)
		self.position = position
		#text co ordinates give the center of the button.
		self.text = message
		self.text_x = self.position[0] + self.sprite.get_width()//2 - self.button_font.size(self.text)[0]//2
		self.text_y = self.position[1] + self.sprite.get_height()//2 - self.button_font.size(self.text)[1]//2
		#label must be blitted
		self.text_label = self.button_font.render(self.text, 1, self.fontcolor)
		
		#the function, NOT a call of the function, to be called when the button is pressed.
		self.command = action
	
	def check_mouse_hover(self, mouse_x, mouse_y):
		#return True if the mouse is hovering over the button
		if self.position[0] < mouse_x < self.position[0] + self.sprite.get_width() and self.position[1] < mouse_y < self.position[1] + self.sprite.get_height():
			#Only change to the hover state if the mouse button is not held down on the button
			if not self.state == "pressed":
				self.change_state("hover")
			return True
		else:
			self.change_state("normal")
			return False
			
	def change_state(self, new_state):
		self.state = new_state
		if self.state == "normal": 
			self.current_state_sprite = self.normal_image
		elif self.state == "hover":
			self.current_state_sprite = self.hover_image
		else:
			self.current_state_sprite = self.depressed_image
		
		self.sprite = pygame.image.load(self.current_state_sprite)
		
	def depress(self):
		"""change the button so that it is being pressed down"""
		self.change_state("pressed")
		
	def update(self, events):
		"""check all of the events to see how the buttons state is changed, then blit the button to the game display
		"""
		
		#check the events
		for event in events:
			#check if the mouse moves over the button
			if event.type == pygame.MOUSEMOTION:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				self.check_mouse_hover(mouse_x, mouse_y)
			
			#check if the mouse clicks on the button
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#ADD: CHECK IF ITS THE LEFT MOUSE BUTTON!!
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if self.check_mouse_hover(mouse_x, mouse_y):
					self.depress()
					
			#check if the mouse is released over the button, i.e if the button has been clicked
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if self.state == "pressed" and self.check_mouse_hover(mouse_x, mouse_y):
					self.change_state("hover")
					self.perform_command()	
					
		#get the position of the text incase the user manually changes button.position(x,y)			
		self.text_x = self.position[0] + self.sprite.get_width()//2 - self.button_font.size(self.text)[0]//2
		self.text_y = self.position[1] + self.sprite.get_height()//2 - self.button_font.size(self.text)[1]//2			
			
		#draw the button in its current state to the display
		self.display.blit(self.sprite, (self.position[0], self.position[1]))
		self.display.blit(self.text_label, (self.text_x, self.text_y))
				
		
	#call the buttons command fuction, the function its meant to perform when clicked on
	def perform_command(self):
		return self.command()
