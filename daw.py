import os
import sys

import pydub
from pydub import AudioSegment
from pydub.playback import play

import pygame

import threading

import time

import random

#bpm
#time measure
#The lower numeral indicates the note value that represents one beat (the beat unit).
#The upper numeral indicates how many such beats constitute a bar.

#60,000 ms in a minute

#ex
#100 bpm -> (60000 / 100 = 600) 1 beat every 600 ms
#4 4 time
#4 quarter notes per bar
#100 quarter notes every minute

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

def new_bar(tSig):
	_beats_in_bar = tSig[0]
	_64s_in_beat = 64 / tSig[1]
	_64s_in_bar = _beats_in_bar * _64s_in_beat
	bar = [[] for _ in range(_64s_in_bar)]
	return bar
	
class Composition:
	def __init__(self):
		self.threads = []
		self.timeSignature = (4,4)
		self.bpm = 100
		self.comp = []
		self.bar = 0
		self._64 = 0
		self.add_bar()
		self.add_bar()
		self.add_bar()
		self.add_bar()
		self.get_len64()
		self.add_sound('coin.wav', 0, 0)
		self.add_sound('coin.wav', 0, 15)
		self.add_sound('coin.wav', 0, 31)
		self.add_sound('coin.wav', 0, 46)
		self.start_loop()
		
	def add_sound(self, name, bar, _64s):
		self.comp[bar][_64s].append(name)
		
	def add_bar(self):
		self.comp.append(new_bar(self.timeSignature))
	
	def remove_bar(self):
		del self.comp[-1]
		
	def start_loop(self):
		t = threading.Thread(target=self.loop)
		self.threads.append(t)
		t.start()
		
	def loop(self):
		bars = range(len(self.comp))
		beats = range(len(self.comp[0]))
		for i in range(100):
			for bar in bars:
				self.bar = bar
				for beat in beats:
					self._64 = beat
					for sound in self.comp[bar][beat]:
						if sound: play_sound_thread(sound)
					#sleep for time of 1 64th note .... minus time of overhead????
					time.sleep(self.len64_sleep)
		return 0
		
		
	def stop_loop(self):
		print '??'
		
	def get_len64(self):
		ms_beat = 60000.0 / self.bpm
		_64s_beat = 64.0 / self.timeSignature[1]
		self.len64 = float(ms_beat) / _64s_beat
		self.len64_sleep = self.len64 / 1000.0
		print 'LEN64:', self.len64
		print 'LEN64_SLEEP', self.len64_sleep
		

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
		
def play_sound(name):
	sound1 = AudioSegment.from_file("C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\" + name, format="wav")
	play(sound1)
	return 0
	
def play_sound_thread(name):
	t = threading.Thread(target=play_sound, args=[name])
	threads.append(t)
	t.start()
	return 0
	
def process_button_down(event):
	joy = event.joy
	button = event.button

	
	comp.add_sound(button_map[button], comp.bar, comp._64)
	play_sound_thread(button_map[button])
	
	return 0
	
def process_button_release(event):
	joy = event.joy
	button = event.button
	return 0
	
def process_joystick(joystick):
	joystick.init()
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
	return 0
	
def main():
	done = False
	while not done:
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
			if event.type == pygame.JOYBUTTONDOWN:
				process_button_down(event)
			if event.type == pygame.JOYBUTTONUP:
				process_button_release(event)
		
		screen.fill(WHITE)
		textPrint.reset()
		
		joystick_count = pygame.joystick.get_count()
		for i in range(joystick_count):
			joystick = pygame.joystick.Joystick(i)
			process_joystick(joystick)
			
		textPrint.log(screen, "bar: {}".format(comp.bar) )	
		textPrint.log(screen, "beat: {}".format(comp._64) )	
			
		pygame.display.flip()
		# clock.tick(20)
	return 0

def get_sound_library(path_to_sounds):
	# returns a dictionary of sounds 
	# sounds are all WAV files in input folder
	sounds_list = []
	
	for filename in os.listdir(path_to_sounds):
		if filename.endswith(".wav"):
			# print(os.path.join(path_to_sounds, filename))
			sounds_list.append(filename)
	
	return sounds_list
	
def get_random_button_map():
	map = {}
	
	for i in range(num_buttons):
		map[i] = sounds[random.randint(0,num_sounds-1)]
	
	print map
	
	return map
	
if __name__ == "__main__":
	threads = []

	pygame.init()
	size = [500, 700]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("DAW")
	clock = pygame.time.Clock()
	pygame.joystick.init()
	textPrint = TextPrint()
	
	sounds_folder = "C:\Users\wahed\Desktop\daw\pydaw\sounds"
	sounds = get_sound_library(sounds_folder)
	num_sounds = len(sounds)
	num_buttons = 14
	
	button_map = get_random_button_map()
	
	comp = Composition()
	
	main()