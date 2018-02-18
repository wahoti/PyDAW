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

import copy

import pickle

#whats next?

#based on how many sounds are stacked it increases the delay time
#figure out how to account for this
#it may be neglible for amounts less than a lot of stacked sounds
#maybe

#more filters
	#change pitch
	#change volume
	#get value of r2 l2??
	
#R3/L3 will switch what filter
	
#cut/sampling tool - chop, grab frequency range, save samples
#synth

#backlog

#bar manipulation feels a little clunky - its prob fine for now tho
#sound cut change? to save memory store length in ms or chunks instead of copying the segment data

#notes

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

def next_list(index, list):
	if (index + 1) >= len(list):
		return 0
	else:
		return index + 1
		
def prev_list(index, list):
	if (index - 1) < 0:
		return len (list)-1
	else:
		return index - 1
	
	
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
		self.modes = ['nav', 'bar']
		self.mode_index = 0
		self.filter_count = 0
		self.cut_count = 0
		self.Lfilter = self.test_filter
		self.Rfilter = self.reverse_filter
		self.tempo = 64
		self.velocity = 1.0
		self.pitch = 1.0
		
		self.start_bars = [0,0,0,0,0,0]
		self.start_64s = [0,0,0,0,0,0]
		self.end_bars = [0,0,0,0,0,0]
		self.end_64s = [0,0,0,0,0,0]
		self.sound_stack = [0,0,0,0,0,0]
		
		self.threads = []
		self.comp = Composition()
		self.record = False
		
	def display(self):
		textPrint.log(screen, "sub-mode: {}".format(self.modes[self.mode_index]) )	
		textPrint.log(screen, "bar: {}".format(self.comp.bar) )	
		textPrint.log(screen, "beat: {}".format(self.comp._64) )	
		textPrint.log(screen, "record: {}".format(self.record) )	
		textPrint.log(screen, "sound_set: {}".format(controller.sound_sets[controller.sound_set_index[0]][controller.sound_set_index[1]]) )	
		
		if (abs(controller.R3[0]) < .15):
			self.pitch = 1.0 if controller.R3[0] > 0 else -1.0
		else:
			self.pitch = controller.R3[0] + 1.0 if controller.R3[0] > 0 else controller.R3[0] - 1.0
		
		if (abs(controller.R3[1]) < .05):
			self.velocity = 1.0 if controller.R3[1] > 0 else -1.0
		else:
			self.velocity = controller.R3[1] + 1.0 if controller.R3[1] > 0 else controller.R3[1] - 1.0
			
		textPrint.log(screen, "velocity: {}".format(self.velocity))
		textPrint.log(screen, "pitch?: {}".format(self.pitch))
		
		angle = controller.Langle
		if (abs(controller.L3[0]) < .15) and (abs(controller.L3[1]) < .15):
			self.tempo = 64
		else:
			if angle < 20:
				self.tempo = 1
			elif angle > 80:
				self.tempo = 2
			if controller.L3[1] > 0:
				if (angle > 20) and (angle < 50):
					self.tempo = 8
				elif (angle > 50) and (angle < 80):
					self.tempo = 4
			else:
				if (angle > 20) and (angle < 50):
					self.tempo = 32
				elif (angle > 50) and (angle < 80):
					self.tempo = 16
		textPrint.log(screen, "tempo: 1/{}".format(self.tempo))
	
	def next_mode(self):
		if (self.mode_index + 1) >= len(self.modes):
			self.mode_index = 0
		else:
			self.mode_index += 1
			
	def reverse_filter(self, segment, sample):
		print 'reverse_filter'
		return segment.reverse()
			
	def velocity_filter(self, segment, sample):
		new_segment = segment + (self.velocity) if self.velocity > 0 else segment + (self.velocity / 2)
		# new_segment = segment.apply_gain(self.velocity)
		return new_segment
		
	def pitch_filter(self, segment, sample):
		# if self.pitch > 1.15:
			# new_segment = segment.set_sample_width(2)
		# elif self.pitch < -1.15:
			# new_segment = segment.set_sample_width(4)
		# else:
		new_segment = segment
		return new_segment
	
	def test_filter(self, segment, sample):
		shifted_samples = np.right_shift(sample, 1)
		shifted_samples_array = array.array(segment.array_type, shifted_samples)
		new_segment = segment._spawn(shifted_samples_array)
		return new_segment
	
	def tempo_template(self, interval, _64):
		intervals = []
		distances = []
		x = 0
		while (x+interval) < 64:
			x += interval
			intervals.append(x)
		for i in intervals:
			distances.append(abs(i - _64))
		print intervals
		return intervals[distances.index(min(distances))]
	
	def button_down(self, button):
		if button is 8:
			self.next_mode()
		if button is 9:
			self.record = not self.record
		elif button in [0,1,2,3,4,5]:
			self.start_bars[button] = self.comp.bar
			self.start_64s[button] = self.comp._64
			name = controller.sound_sets[controller.sound_set_index[0]][controller.sound_set_index[1]][button]
			self.sound_stack[button] = name
			segment = controller.audio_segments[name]
			sample = controller.audio_samples[name]
			filtered = False
			if controller.buttons[6]:
				filtered = True
				segment = self.Lfilter(segment, sample)
				sample = segment.get_array_of_samples()
			if controller.buttons[7]:	
				filtered = True
				segment = self.Rfilter(segment, sample)
				sample = segment.get_array_of_samples()
			if abs(self.velocity) > 1.01:
				filtered = True
				segment = self.pitch_filter(segment, sample)
				sample = segment.get_array_of_samples()
			if abs(self.pitch) > 1.01:
				filtered = True
				segment = self.velocity_filter(segment, sample)
				sample = segment.get_array_of_samples()				
			if self.record:
				if filtered:
					self.filter_count += 1
					name = 'filter' + str(self.filter_count)
					controller.new_sound(name, segment, sample)
					self.sound_stack[button] = name
				#add full length immediately mode?
				# self.comp.add_sound(name, self.comp.bar, self.comp._64)
			controller.play_sound_thread(segment, button)
		elif button in [14,15,16,17]:
			if self.modes[self.mode_index] is 'nav':
				if button is 14:
					controller.sound_set_left()
				elif button is 15:
					controller.sound_set_right()
				elif button is 16:
					controller.sound_set_down()
				elif button is 17:
					controller.sound_set_up()
			elif self.modes[self.mode_index] is 'bar':
				if button is 14:
					self.comp.del_bar()
				elif button is 15:
					self.comp.copy_bar()
				elif button is 16:
					self.comp.cut_bar()
				elif button is 17:
					self.comp.add_bar()
			
	def button_release(self, button):
		if button in [0,1,2,3,4,5]:
			if self.record:
				self.end_bars[button] = self.comp.bar
				self.end_64s[button] = self.comp._64
				
				diff_bar = self.end_bars[button] - self.start_bars[button]
				diff_64s = self.end_64s[button] - self.start_64s[button]
				
				segment = controller.audio_segments[self.sound_stack[button]]
				samples =  controller.audio_samples[self.sound_stack[button]]
				chunks = controller.make_chunks(segment, 1)
				
				#chop of audio at last bar
				if diff_bar < 0:
					num_64s = diff_64s if diff_64s >= 0 else (64 - abs(diff_64s))
				else:
					num_64s = (diff_bar * 64) + diff_64s if diff_64s >= 0 else (diff_bar * 64) + (64 - abs(diff_64s))
					
				#if button released early chop the sound
				if num_64s < len(segment):
					index = self.comp.len64 * num_64s
					new_segment = segment[:index]
					new_sample = new_segment.get_array_of_samples()
				
					self.cut_count += 1
					name = 'cut' + str(self.cut_count)
					controller.new_sound(name, new_segment, new_sample)

				#place sound according to tempo
				print self.tempo
				if self.tempo is 64:
					print '1/64'
					self.comp.add_sound(name, self.start_bars[button], self.start_64s[button])
				elif self.tempo is 32:
					print '1/32'
					spot = self.tempo_template(2, self.start_64s[button])
					self.comp.add_sound(name, self.start_bars[button], spot)
				elif self.tempo is 16:
					print '1/16'
					spot = self.tempo_template(4, self.start_64s[button])
					self.comp.add_sound(name, self.start_bars[button], spot)
				elif self.tempo is 8:
					print '1/8'
					spot = self.tempo_template(8, self.start_64s[button])
					self.comp.add_sound(name, self.start_bars[button], spot)
				elif self.tempo is 4:
					print '1/4'
					spot = self.tempo_template(16, self.start_64s[button])
					self.comp.add_sound(name, self.start_bars[button], spot)
				elif self.tempo is 2:
					print '1/2'
					spot = self.tempo_template(32, self.start_64s[button])
					self.comp.add_sound(name, self.start_bars[button], spot)
				elif self.tempo is 1:
					print '1/1'
					self.comp.add_sound(name, self.start_bars[button], 0)
					# print ((controller.L3[0]), (controller.L3[1]))
					# if (abs(controller.L3[0]) < .15) and (abs(controller.L3[1]) < .15):
						# self.comp.add_sound(name, self.start_bars[button], self.start_64s[button])
					# else:
						# # v1 = [0.0, -1.0]
						# # v2 = [controller.L3[1], controller.L3[0]] 
						# # dot = (v1[0] * v2[0]) + (v1[1] * v2[0])
						# # angle = (math.acos(dot) / math.pi) * 100
						# angle = controller.Langle
						# #need 1/1 1/2 1/4 1/8 1/16 1/32
						# print angle
						# if angle < 20:
							# print 'whole note'
							# #whole note 1/1
							# self.comp.add_sound(name, self.start_bars[button], 0)
						# elif angle > 80:
							# print 'eighth note'
							# #eighth note 1/8
							# spot = self.tempo_template(8, self.start_64s[button])
							# self.comp.add_sound(name, self.start_bars[button], spot)
						# if controller.L3[1] > 0:
							# if (angle > 20) and (angle < 50):
								# #half note
								# print 'half note'
								# spot = self.tempo_template(32, self.start_64s[button])
								# self.comp.add_sound(name, self.start_bars[button], spot)
							# elif (angle > 50) and (angle < 80):
								# #quarter note
								# print 'quarter note'
								# spot = self.tempo_template(16, self.start_64s[button])
								# self.comp.add_sound(name, self.start_bars[button], spot)
						# else:
							# if (angle > 20) and (angle < 50):
								# #32 note
								# print '32 note'
								# spot = self.tempo_template(2, self.start_64s[button])
								# self.comp.add_sound(name, self.start_bars[button], spot)
							# elif (angle > 50) and (angle < 80):
								# #16 note
								# print '16 note'
								# spot = self.tempo_template(4, self.start_64s[button])
								# self.comp.add_sound(name, self.start_bars[button], spot)
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

class Tsetsoundset:
	def __init__(self):
		self.name = 'setsoundset'
		self.sound_index = 0
		self.listen = False
		
	def display(self):
		textPrint.log(screen, "setsoundset")
		textPrint.log(screen, "listen? {}".format(self.listen))
		textPrint.log(screen, "selected_sound: {}".format(controller.library[self.sound_index]))
		textPrint.log(screen, "sound_set {}:".format(controller.sound_set_index))
		for x in range(6):
			textPrint.log(screen, "\t{}".format(controller.sound_sets[controller.sound_set_index[0]][controller.sound_set_index[1]][x]))
			
	def next_sound(self):
		self.sound_index = next_list(self.sound_index, controller.library)
		
	def prev_sound(self):
		self.sound_index = prev_list(self.sound_index, controller.library)
		
	def button_down(self, button):	
		if button is 14:
			controller.sound_set_left()
		elif button is 15:
			controller.sound_set_right()
		elif button is 16:
			controller.sound_set_down()
		elif button is 17:
			controller.sound_set_up()
		elif button is 6:
			self.prev_sound()
		elif button is 7:
			self.next_sound()
		elif button is 8:
			controller.save_sound_set()
		elif button is 13:
			segment = controller.audio_segments[controller.library[self.sound_index]]
			controller.play_sound_thread(segment, button)
		elif button in [0,1,2,3,4,5]:
			if self.listen:
				name = controller.sound_sets[controller.sound_set_index[0]][controller.sound_set_index[1]][button]
				segment = controller.audio_segments[name]
				controller.play_sound_thread(segment, button)
			else:
				controller.sound_sets[controller.sound_set_index[0]][controller.sound_set_index[1]][button] = controller.library[self.sound_index]
		return 0
	def button_release(self, button):
		winsound.PlaySound(None, winsound.SND_PURGE)
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
		self.threads = []
	
		self.width = 3
		self.height = 3
		self.sound_sets = []
		for x in range(self.width):
			row = []
			for y in range(self.height):
				column = ['jump.wav', 'kick.wav', 'land.wav', 'fireball.wav', 'coin.wav', 'brick_shatter.wav']
				row.append(column)
			self.sound_sets.append(row)
		self.sound_set_index = [1,1]
		
		self.num_buttons = 14
		self.dpad = [0,0]
		self.buttons = {}
		self.L3 = [0, 0]
		self.R3 = [0, 0]
		self.Langle = 0
		self.init_buttons()
		
		self.sounds_path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\"
		self.init_library()
		self.init_audio_segments()
		
		self.modes = ['compose', 'cut', 'synth', 'setsoundset']
		self.mode_handlers = [Tcompose(), Tsetsoundset(), Tcut(), Tsynth()]
		self.mode_index = 0
		self.mode = self.modes[self.mode_index]
		#MODES: 'compose', 'cut', 
		#settings for individual tools?
		#mode controls the button layout and functionality
		
		self.load_sound_set()
		
	def init_buttons(self):
		for x in range(self.num_buttons):
			#was down - is down
			self.buttons[x] = False
		
	def load_sound_set(self):
		print "loading sound sets"
		with open('soundset.pkl') as f:
			self.sound_sets = pickle.load(f)
	
	def save_sound_set(self):
		print "saving sound sets"
		with open('soundset.pkl', 'w') as f:
			pickle.dump(self.sound_sets, f)
		
	def next_mode(self):
		
	
		new_index = self.mode_index + 1
		if new_index >= len(self.modes):
			self.mode_index = 0
			self.mode = self.modes[0]
		else:
			self.mode_index = new_index
			self.mode = self.modes[new_index]
		print self.mode
		
	def sound_set_up(self):
		if (self.sound_set_index[1] + 1) >= (self.height):
			self.sound_set_index[1] = 0
		else:
			self.sound_set_index[1] += 1
	def sound_set_right(self):
		if (self.sound_set_index[0] + 1) >= (self.width):
			self.sound_set_index[0] = 0
		else:
			self.sound_set_index[0] += 1
	def sound_set_down(self):
		if (self.sound_set_index[1] - 1) < 0:
			self.sound_set_index[1] = self.height - 1
		else:
			self.sound_set_index[1] -= 1
	def sound_set_left(self):
		if (self.sound_set_index[0] - 1) < 0:
			self.sound_set_index[0] = self.width - 1
		else:
			self.sound_set_index[0] -= 1
	def button_down(self, button):
		print 'down', button
		self.buttons[button] = True

		if button is 12:
			self.next_mode()
		else:
			self.mode_handlers[self.mode_index].button_down(button)
			
	def button_release(self, button):
		print 'release', button
		self.buttons[button] = False
	
		if button is not 12:
			self.mode_handlers[self.mode_index].button_release(button)
			
	def make_chunks(self, audio_segment, chunk_length):
		"""
		Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
		long.
		if chunk_length is 50 then you'll get a list of 50 millisecond long audio
		segments back (except the last one, which can be shorter)
		"""
		number_of_chunks = math.ceil(len(audio_segment) / float(chunk_length))
		return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
				for i in range(int(number_of_chunks))]
	
	def play_sound_pydub_nostop(self, seg):
		play(seg)
		return 0
	
	def play_sound_pydub(self, seg, button):
		p = pyaudio.PyAudio()
		stream = p.open(format=p.get_format_from_width(seg.sample_width),
			channels=seg.channels,
			rate=seg.frame_rate,
			output=True)

		chunks = self.make_chunks(seg, 100)
		
		for x in range(len(chunks)):
			if not controller.buttons[button]:
				break
			stream.write(chunks[x]._data)
	
		# play(segment)
		return 0
	
	def play_sound_winsound(self, sound):
		# winsound.PlaySound(r'C:\Users\wahed\Desktop\daw\pydaw\sounds\dragon_coin.wav', winsound.SND_ASYNC)
		winsound.PlaySound(self.sounds_path + sound, winsound.SND_ASYNC)
		return 0
	
	def play_sound_thread(self, segment, button):
		t = threading.Thread(target=self.play_sound_pydub, args=[segment, button])
		self.threads.append(t)
		t.start()
		return 0
		
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
	
		
	
class Composition:
	def __init__(self):
		self.threads = []
		self.timeSignature = (4,4)
		self.bpm = 80
		self.comp = []
		self.bar = 0
		self._64 = 0
		self.add_bar()
		self.get_len64()
		
		self.sound_limit = 4
		
		self.start = time.time()
		self.end = time.time()
		
		# self.test()		
		self.loop = True
		self.start_loop()
			
	def test(self):	
		self.add_sound('coin.wav', 0, 0)
		self.add_sound('coin.wav', 0, 15)
		self.add_sound('coin.wav', 0, 31)
		self.add_sound('coin.wav', 0, 46)
	
	def play_sound_pydub(self, sound):
		play(controller.audio_segments[sound])
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
		if len(self.comp[bar][_64s]) >= self.sound_limit:
			self.comp[bar][_64s] = self.comp[bar][_64s][1:]
			print 'sound limit enforced'
		
	def _new_bar(self, tSig):
		_beats_in_bar = tSig[0]
		_64s_in_beat = 64 / tSig[1]
		_64s_in_bar = _beats_in_bar * _64s_in_beat
		bar = [[] for _ in range(_64s_in_bar)]
		return bar	
		
	def add_bar(self):
		print 'add_bar'
		#add empty bar to end of composition
		self.comp.append(self._new_bar(self.timeSignature))
	
	def cut_bar(self):
		print 'cut_bar'
		#remove bar from end of composition
		if len(self.comp) is 1:
			return
		else:
			del self.comp[-1]
		
	def copy_bar(self):
		print 'copy_bar'
		#copies current bar
		bar = copy.deepcopy(self.comp[self.bar])
		self.comp.insert(self.bar, bar)
	
	def del_bar(self):
		print 'del_bar'	
		#removes current bar
		if len(self.comp) is 1:
			return
		else:
			self.comp = self.comp[:self.bar] + self.comp[self.bar+1:]
		
	def start_loop(self):
		self.loop = True
		t = threading.Thread(target=self.loop_thread)
		self.threads.append(t)
		t.start()
		
	def loop_thread(self):
		while self.loop:
			bars = range(len(self.comp))
			beats = range(len(self.comp[0]))
			for bar in bars:
				self.bar = bar
				for beat in beats:
					self._64 = beat
					try:
						sounds = range(len(self.comp[bar][beat]))
					except Exception as e:
						break
					for s in sounds:
						try:
							sound = self.comp[bar][beat][s]
						except Exception as e:
							break
						if sound: self.play_sound_thread(sound)
					self.end=time.time()
					#sleep for time of 1 64th note minus time of overhead
					sleep_time = self.len64_sleep - (self.end-self.start)
					# print self.end-self.start
					# print sleep_time
					if sleep_time < 0:
						print 'WARNING overhead throwing off clock', sleep_time, len(sounds)
					else:
						time.sleep(sleep_time)
					self.start = time.time()
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
	
	# print (joystick.get_axis( 0 ), joystick.get_axis( 1 ))
	controller.L3 = [joystick.get_axis( 1 ), joystick.get_axis( 0 )]
	controller.R3 = [joystick.get_axis( 2 ), joystick.get_axis( 3 )]
	
	v1 = [-1.0, 0.0]
	v2 = [controller.L3[0], controller.L3[1]] 
	dot = (v1[0] * v2[0]) + (v1[1] * v2[0])
	controller.Langle = (math.acos(dot) / math.pi) * 100
	
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

	#hats will be buttons 14-17
	for i in range( hats ):
		hat = joystick.get_hat( i )
		textPrint.log(screen, "Hat {} value: {}".format(i, str(hat)) )
		if (hat[0] is -1) and not (controller.dpad[0] is -1):
			controller.button_down(14)
		elif not (hat[0] is -1) and (controller.dpad[0] is -1):
			controller.button_release(14)
		if (hat[0] is 1)  and not (controller.dpad[0] is 1):
			controller.button_down(15)
		elif not (hat[0] is 1) and (controller.dpad[0] is 1):
			controller.button_release(15)
		if (hat[1] is -1)  and not (controller.dpad[1] is -1):
			controller.button_down(16)
		elif not (hat[1] is -1) and (controller.dpad[1] is -1):
			controller.button_release(16)
		if (hat[1] is 1)  and not (controller.dpad[1] is 1):
			controller.button_down(17)
		elif not (hat[1] is 1) and (controller.dpad[1] is 1):
			controller.button_release(17)
		controller.dpad[0] = hat[0]
		controller.dpad[1] = hat[1]
		
	
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
				controller.button_down(event.button)
			if event.type == pygame.JOYBUTTONUP:
				controller.button_release(event.button)
		
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
	
if __name__ == "__main__":
	threads = []

	pygame.init()
	size = [500, 700]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("DAW")
	clock = pygame.time.Clock()
	pygame.joystick.init()
	textPrint = TextPrint()
	
	controller = Controller()
	
	main()