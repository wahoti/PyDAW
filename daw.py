import os
import sys

import pydub
from pydub import AudioSegment
from pydub.playback import play

import pygame

import threading

import time

import random

import winsound

import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio     #initialize pyaudio

import numpy as np

import array

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
	
	
class T_:
	def __init__(self):
		self.name = '_'
	def display(self):
		textPrint.log(screen, "_")
	def button_down(self, button):
		print '_ button down'
	def button_release(self, button):
		print '_ button release'
		
class Tcompose:
	def __init__(self):
		self.name = 'compose'
		self.filter_count = 0
		self.Lfilter = self.test_filter
		self.Rfilter = self.test_filter
		
		self.start_bar = 0
		self.end_bar = 0
		self.start_64 = 0
		self.end_64 = 0
		
		self.threads = []
		
		self.comp = Composition()
		
		self.record = False
		
		self.sounds_path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\"
		
		self.sound_sets = [
			['jump.wav', 'kick.wav', 'land.wav', 'fireball.wav'],
			['spin.wav', 'stomp.wav', 'warp.wav', 'yoshi.wav']
		]
		
		self.init_audio_segments()
		self.init_audio_samples()
	
		#store audio segments
		
		self.sound_set_index = 0
	
	def init_audio_segments(self):
		self.audio_segments = []
		for set in self.sound_sets:
			new_set = []
			for sound in set:
				new_set.append(AudioSegment.from_file(self.sounds_path + sound, format="wav"))
			self.audio_segments.append(new_set)

		
	def init_audio_samples(self):
		self.audio_samples = []
		for set in self.audio_segments:
			new_set = []
			for sound in set:
				new_set.append(sound.get_array_of_samples())
			self.audio_samples.append(new_set)
		
		
	def display(self):
		textPrint.log(screen, "bar: {}".format(self.comp.bar) )	
		textPrint.log(screen, "beat: {}".format(self.comp._64) )	
		textPrint.log(screen, "record: {}".format(self.record) )	
		textPrint.log(screen, "sound_set: {}".format(self.sound_sets[self.sound_set_index]) )	
	
	def next_sound_set(self):
		if (self.sound_set_index + 1)  >= len(self.sound_sets):
			self.sound_set_index = 0
		else:
			self.sound_set_index += 1
	
	def prev_sound_set(self):
		if (self.sound_set_index - 1)  < 0:
			self.sound_set_index = len(self.sound_sets)-1
		else:
			self.sound_set_index -= 1
	
	def play_sound_pydub(self, segment):
		# play(segment)
		winsound.PlaySound(self.sounds_path + sound, winsound.SND_ASYNC)
		return 0
	
	def play_sound_winsound(self, sound):
		# winsound.PlaySound(r'C:\Users\wahed\Desktop\daw\pydaw\sounds\dragon_coin.wav', winsound.SND_ASYNC)
		winsound.PlaySound(self.sounds_path + sound, winsound.SND_ASYNC)
		return 0
	
	def play_sound_thread(self, segment):
		t = threading.Thread(target=self.play_sound_pydub, args=[segment])
		# t = threading.Thread(target=self.play_sound_winsound, args=[sound])
		self.threads.append(t)
		t.start()
		return 0
	
	def test_filter(self, segment, sample):
		shifted_samples = np.right_shift(sample, 1)
		shifted_samples_array = array.array(segment.array_type, shifted_samples)
		new_segment = segment._spawn(shifted_samples_array)
		return new_segment
	
	def button_down(self, button):
		if button is 9:
			self.record = not self.record
		elif button in [0,1,2,3]:
			self.start_bar = self.comp.bar
			self.start_64 = self.comp._64
			name = self.sound_sets[self.sound_set_index][button]
			segment = self.audio_segments[self.sound_set_index][button]
			sample = self.audio_samples[self.sound_set_index][button]
			filtered = False
			if controller.buttons[6]:
				filtered = True
				segment = self.Lfilter(segment, sample)
				sample = segment.get_array_of_samples()
			if controller.buttons[7]:	
				filtered = True
				segment = self.Rfilter(segment, sample)
				sample = segment.get_array_of_samples()
			if self.record:
				if filtered:
					self.filter_count += 1
					name = 'filter' + str(self.filter_count)
					self.comp.new_sound(name, segment, sample)
				self.comp.add_sound(name, self.comp.bar, self.comp._64)
			self.play_sound_thread(segment)

		elif button is 4:
			self.prev_sound_set()
		elif button is 5:
			self.next_sound_set()
		# elif button is 
			#APPLY FILTER
			#PLAY SONGS FROM MEMORY?????????
			#store audio segments
		# else:
			# self.play_sound_thread(button_map[button])
			# if self.record: self.comp.add_sound(self.sound_sets[self.sound_set_index][button], self.comp.bar, self.comp._64)
			
	def button_release(self, button):
		#put record here
		#TRIM it to corresponding time --- how?
		self.end_bar = self.comp.bar
		self.end_64 = self.comp._64
		#calculate difference?
		print self.start_bar, self.end_bar
		print self.start_64, self.end_64
		# if self.record: self.comp.add_sound(self.sound_sets[self.sound_set_index][button], self.start_bar, self.start_64)
		
		#AUDIO SEGMENT
		#can get raw data from audio segment - apply filter - plug into winsound
		#try this out in the lab and time it
		#new_sound = sound._spawn(shifted_samples_array)
		#FILE NAVIGATION
		
		#use same time function from lab to get a start and end time ?
		#if can get a second value for duration is it possible to trim the wav file to that length?
		#using something like samplewidth, number of samples
		
		winsound.PlaySound(None, winsound.SND_PURGE)
		return 0
		
class Tcut:
	def __init__(self):
		self.name = 'cut'
		
	def display(self):
		textPrint.log(screen, "cut")
	def button_down(self, button):
		return 0
	def button_release(self, button):
		return 0
		
class Tsynth:
	def __init__(self):
		self.name = 'synth'
		
		self.stop = False
		
		self.threads = []
		
		self.wavs = []
		
		self.sounds = [
			[500, .1],
			[500, .2],
			[500, .3],
			[500, .4]
		]
		self.bitrate = 16000
		
		self.generate_wav()
		
		p = PyAudio()
		self.stream = p.open(format = p.get_format_from_width(1), 
			channels = 1, 
			rate = self.bitrate, 
			output = True)
		
	def generate_wav(self):
		self.wavs = []
		for sound in self.sounds:
			FREQUENCY = sound[0]
			LENGTH = sound[1]
			if FREQUENCY > self.bitrate:
				# BITRATE = FREQUENCY+100#???
				continue
			NUMBEROFFRAMES = int(self.bitrate * LENGTH)
			RESTFRAMES = NUMBEROFFRAMES % self.bitrate
			WAVEDATA = ''    
			for x in xrange(NUMBEROFFRAMES):
				WAVEDATA = WAVEDATA+chr(int(math.sin(x/((self.bitrate/FREQUENCY)/math.pi))*127+128))    
			for x in xrange(RESTFRAMES): 
				WAVEDATA = WAVEDATA+chr(128)
			self.wavs.append(WAVEDATA)
		
	def display(self):
		textPrint.log(screen, "synth")

	def synth_thread(self, wav):
		# while not self.stop:
			# self.stream.write(self.wavs[wav])
		# self.stop = False
		winsound.PlaySound(r'C:\Users\wahed\Desktop\daw\pydaw\sounds\dragon_coin.wav', winsound.SND_ASYNC)

	def button_down(self, button):
		# winsound.Beep(1500, 100)
		# winsound.PlaySound('sounds\\bird.wav', winsound.SND_FILENAME)
		
		butt = 0
		if button is 0:
			butt = 0
		elif button is 1:
			butt = 1
		elif button is 2:
			butt = 2
		elif button is 3:
			butt = 3
		
		t = threading.Thread(target=self.synth_thread, args=[butt])
		self.threads.append(t)
		t.start()
		return 0
		
	def button_release(self, button):
		print 'synth button release'
		# winsound.PlaySound(r'C:\Users\wahed\Desktop\daw\pydaw\sounds\dragon_coin.wav', winsound.SND_ASYNC)
		winsound.PlaySound(None, winsound.SND_PURGE)
		# self.stop = True
	
		return 0

class Controller:
	def __init__(self):
		self.modes = ['compose', 'cut', 'synth']
		self.mode_handlers = [Tcompose(), Tcut(), Tsynth()]
		self.mode_index = 0
		self.mode = self.modes[self.mode_index]
		#MODES: 'compose', 'cut', 
		#settings for individual tools?
		#mode controls the button layout and functionality
		
		self.num_buttons = 14
		self.hats = []
		self.buttons = {}
		self.axis = []
		self.init_buttons()
		
	def init_buttons(self):
		for x in range(self.num_buttons):
			#was down - is down
			self.buttons[x] = False
		
	def next_mode(self):
		
	
		new_index = self.mode_index + 1
		if new_index >= len(self.modes):
			self.mode_index = 0
			self.mode = self.modes[0]
		else:
			self.mode_index = new_index
			self.mode = self.modes[new_index]
		print self.mode
		
		
	def button_down(self, button):
		self.buttons[button] = True

		if button is 12:
			self.next_mode()
		else:
			self.mode_handlers[self.mode_index].button_down(button)
			
	def button_release(self, button):
		self.buttons[button] = False
	
		if button is not 12:
			self.mode_handlers[self.mode_index].button_release(button)
	
		
	
class Composition:
	def __init__(self):
		self.threads = []
		self.timeSignature = (4,4)
		self.bpm = 100
		self.comp = []
		self.bar = 0
		self._64 = 0
		self.add_bar()
		self.get_len64()
		
		self.sounds_path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\"
		self.init_library()
		self.init_audio_segments()
		
		# self.test()		
		self.loop = True
		self.start_loop()
		
	def init_library(self):
		self.library = []		
		for filename in os.listdir(self.sounds_path):
			if filename.endswith(".wav"):
				# print(os.path.join(path_to_sounds, filename))
				self.library.append(filename)
		
	def init_audio_segments(self):
		self.audio_segments = {}
		self.audio_samples = {}
		for sound in self.library:
			#will this overload memory?
			self.audio_segments[sound] = AudioSegment.from_file(self.sounds_path + sound, format="wav")
			self.audio_samples[sound] = self.audio_segments[sound].get_array_of_samples()
			
	def new_sound(self, name, segment, sample):
		if name in self.library:
			return
		
		self.library.append(name)
		self.audio_segments[name] = segment
		self.audio_samples[name] = sample
			
	def test(self):	
		self.add_sound('coin.wav', 0, 0)
		self.add_sound('coin.wav', 0, 15)
		self.add_sound('coin.wav', 0, 31)
		self.add_sound('coin.wav', 0, 46)
	
	def play_sound_pydub(self, sound):
		play(self.audio_segments[sound])
		return 0
	
	def play_sound_winsound(self, sound):
		# winsound.PlaySound(r'C:\Users\wahed\Desktop\daw\pydaw\sounds\dragon_coin.wav', winsound.SND_ASYNC)
		winsound.PlaySound(self.sounds_path + sound, winsound.SND_ASYNC)
		return 0
	
	def play_sound_thread(self, sound):
		t = threading.Thread(target=self.play_sound_pydub, args=[sound])
		# t = threading.Thread(target=self.play_sound_winsound, args=[sound])
		self.threads.append(t)
		t.start()
		return 0
	
	def add_sound(self, name, bar, _64s):
		self.comp[bar][_64s].append(name)
		
	def add_bar(self):
		self.comp.append(new_bar(self.timeSignature))
	
	def remove_bar(self):
		del self.comp[-1]
		
	def start_loop(self):
		self.loop = True
		t = threading.Thread(target=self.loop_thread)
		self.threads.append(t)
		t.start()
		
	def loop_thread(self):
		bars = range(len(self.comp))
		beats = range(len(self.comp[0]))
		while self.loop:
			for bar in bars:
				self.bar = bar
				for beat in beats:
					self._64 = beat
					for sound in self.comp[bar][beat]:
						if sound: self.play_sound_thread(sound)
					#sleep for time of 1 64th note .... minus time of overhead????
					time.sleep(self.len64_sleep)
		return 0
		
		
	def stop_loop(self):
		self.loop = False
		
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
	print event.button
	
	controller.button_down(event.button)
	
	return 0
	
def process_button_release(event):
	joy = event.joy
	button = event.button
	
	controller.button_release(event.button)
	
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
			
		textPrint.log(screen, "mode: {}".format(controller.mode) )	
		controller.mode_handlers[controller.mode_index].display()
			
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
	
	controller = Controller()
	
	main()