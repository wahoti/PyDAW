print 'how to interact with dualshock4 with python'

import sys
import pygame
from OpenGL.GL import *

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def log(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

def main2():
	pygame.init()
	size = [500, 700]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("My Game")
	done = False
	clock = pygame.time.Clock()
	# Initialize the joysticks
	pygame.joystick.init()
	# Get ready to print
	textPrint = TextPrint()		
	
	while done==False:
		# EVENT PROCESSING STEP
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			
			# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
			if event.type == pygame.JOYBUTTONDOWN:
				print("Joystick button pressed.")
			if event.type == pygame.JOYBUTTONUP:
				print("Joystick button released.")
				
	 
		# DRAWING STEP
		# First, clear the screen to white. Don't put other drawing commands
		# above this, or they will be erased with this command.
		screen.fill(WHITE)
		textPrint.reset()

		# Get count of joysticks
		joystick_count = pygame.joystick.get_count()

		textPrint.log(screen, "Number of joysticks: {}".format(joystick_count) )
		textPrint.indent()
		
		# For each joystick:
		for i in range(joystick_count):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
		
			textPrint.log(screen, "Joystick {}".format(i) )
			textPrint.indent()
		
			# Get the name from the OS for the controller/joystick
			name = joystick.get_name()
			textPrint.log(screen, "Joystick name: {}".format(name) )
			
			# Usually axis run in pairs, up/down for one, and left/right for
			# the other.
			axes = joystick.get_numaxes()
			textPrint.log(screen, "Number of axes: {}".format(axes) )
			textPrint.indent()
			
			for i in range( axes ):
				axis = joystick.get_axis( i )
				textPrint.log(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
			textPrint.unindent()
				
			buttons = joystick.get_numbuttons()
			textPrint.log(screen, "Number of buttons: {}".format(buttons) )
			textPrint.indent()

			for i in range( buttons ):
				button = joystick.get_button( i )
				textPrint.log(screen, "Button {:>2} value: {}".format(i,button) )
			textPrint.unindent()
				
			# Hat switch. All or nothing for direction, not like joysticks.
			# Value comes back in an array.
			hats = joystick.get_numhats()
			textPrint.log(screen, "Number of hats: {}".format(hats) )
			textPrint.indent()

			for i in range( hats ):
				hat = joystick.get_hat( i )
				textPrint.log(screen, "Hat {} value: {}".format(i, str(hat)) )
			textPrint.unindent()
			
			textPrint.unindent()

			# glPushMatrix()   
			# glRotatef(roty_scale * axis[4], 1, 0, 0)
			# glRotatef(rotx_scale * axis[5], 0, 0, 1)
			# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			# glBegin(GL_LINES)
			# for edge in edges:
				# for vertex in edge:
					# glColor3fv((1,1,1))
					# glVertex3fv(vertices[vertex])
			# glEnd()
			# glPopMatrix()		
		
		
		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
		
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

		# Limit to 20 frames per second
		clock.tick(20)
		
	# Close the window and quit.
	# If you forget this line, the program will 'hang'
	# on exit if running from IDLE.
	pygame.quit ()
		
def main():
	# pygame.joystick.init()
	# joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
	
	controller = pygame.joystick.Joystick(0)
	controller.init()
	
	axis = {}
	button = {}

	# these are the identifiers for the PS4's accelerometers
	AXIS_X = 3
	AXIS_Y = 4

	# variables we'll store the rotations in, initialised to zero
	rot_x = 0.0
	rot_y = 0.0

	# main loop
	while not True:
		# copy rot_x/rot_y into axis[] in case we don't read any
		axis[AXIS_X] = rot_x
		axis[AXIS_Y] = rot_y
		
		# retrieve any events ...
		for event in pygame.event.get():
			if event.type == pygame.JOYAXISMOTION:
				axis[event.axis] = round(event.value,2)
			elif event.type == pygame.JOYBUTTONDOWN:
				button[event.button] = True
			elif event.type == pygame.JOYBUTTONUP:
				button[event.button] = False

			rot_x = axis[AXIS_X]
			rot_y = axis[AXIS_Y]            

			print axis
			
			# do something with this ...

if __name__ == "__main__":
	main2()
		