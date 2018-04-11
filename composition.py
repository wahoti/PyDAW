import time
import threading
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import make_chunks
from pydub.effects import *

class Sound:
	def __init__(self, name, samples, segments):
		self.name = name
		self.samples = samples
		self.segment = segments

class Composition:
	#composition class
	#stores and loops sounds

	def __init__(self, sounds_path="def"):
		if sounds_path == "def":
			self.sounds_path = os.getcwd() + "\\sounds\\"
			print self.sounds_path
		else:	
			self.sounds_path = sounds_path
		self.init_library()
	
		self.threads = []
		self.timeSignature = (4,4)
		self.bpm = 80
		self.comp = []
		self.bar = 0
		self._64 = 0
		self.new_bar()
		self.get_len64()
		
		self.sound_limit = 4
		
		self.start = time.time()
		self.end = time.time()
		
		# self.test()		
		self.loop = False
		# self.start_loop()
			
	def help(self):
		print "library"
		print "add_sound(name, bar, 64s)"
		print "play_sound(name)"
		print "add_bar(bar_index)"
		print "copy_bar(bar_index)"
		print "delete_bar(bar_index)"
		print "note: no arguments to bar_index will default to current location"
		print "new_bar() adds bar to the end"
		print "cut_bar() removes bar from end"
		print "start_loop()"
		print "stop_loop()"
		print "get_len64()"	
		
	def init_library(self): 
		#library is an array of wav file names
		self.library = []
		
		#audio_segments is a dict of audio segments (pydub)
		#keys are wav filenames from library
		self.audio_segments = {}
		
		#audio_segments is a dict of audio samples (raw)
		#keys are wav filenames from library
		self.audio_samples = {}
		
		for filename in os.listdir(self.sounds_path):
			if filename.endswith(".wav"):
				# print(os.path.join(path_to_sounds, filename))
				self.library.append(filename)

		for sound in self.library:
			#will this overload memory?
			self.audio_segments[sound] = AudioSegment.from_file(self.sounds_path + sound, format="wav")
			self.audio_samples[sound] = self.audio_segments[sound].get_array_of_samples()
	
	def library_add_sound(self, name, segment):
		self.library.append(name)
		self.audio_segments[name] = segment
		self.audio_samples[name] = segment.get_array_of_samples()
	
	def get_sound(self, name):
		return Sound(
			name,
			self.audio_samples[name],
			self.audio_segments[name]
		)
			
	def add_sound(self, name, bar, _64s):
		#adds sound to composition at specified bar# and 64#
		self.comp[bar][_64s].append(name)
		if len(self.comp[bar][_64s]) >= self.sound_limit:
			self.comp[bar][_64s] = self.comp[bar][_64s][1:]
			print 'sound limit enforced'
	
	def play_sound(self, sound):
		#plays sound with pydub
		play(self.audio_segments[sound])
		return 0
	
	def play_sound_winsound(self, sound):
		# winsound.PlaySound(r'C:\Users\wahed\Desktop\daw\pydaw\sounds\dragon_coin.wav', winsound.SND_ASYNC)
		winsound.PlaySound(self.sounds_path + sound, winsound.SND_ASYNC)
		return 0
	
	def play_sound_thread(self, sound):
		#plays sounds concurrently
		t = threading.Thread(target=self.play_sound, args=[sound])
		# t = threading.Thread(target=self.play_sound_winsound, args=[sound])
		self.threads.append(t)
		t.start()
		return 0
		
	def _new_bar(self, tSig):
		#returns a bar array used for storing and looping sounds
		_beats_in_bar = tSig[0]
		_64s_in_beat = 64 / tSig[1]
		_64s_in_bar = _beats_in_bar * _64s_in_beat
		bar = [[] for _ in range(_64s_in_bar)]
		return bar	

	def add_bar(self, bar="def"):
		print 'add_bar'
		
		if bar=="def":
			#add empty bar to current position
			self.comp.insert(self.bar, self._new_bar(self.timeSignature))
		else:
			#add empty bar to input position
			self.comp.insert(bar, self._new_bar(self.timeSignature))
			
		
	def copy_bar(self, bar="def"):
		print 'copy_bar'
		if bar=="def":
			#copies current bar
			bar = copy.deepcopy(self.comp[self.bar])
			self.comp.insert(self.bar, bar)
		else:
			#copies input bar
			if bar >= 0 and bar < len(self.comp):
				bar_copy = copy.deepcopy(self.comp[bar])
				self.comp.insert(bar, bar_copy)
	
	def delete_bar(self, bar="def"):
		print 'delete_bar'	
		if bar=="def":
			#removes current bar
			if len(self.comp) is 1:
				return
			else:
				self.comp = self.comp[:self.bar] + self.comp[self.bar+1:]
		else:
			#removes input bar
			if bar >= 0 and bar < len(self.comp):
				self.comp = self.comp[:bar] + self.comp[bar+1:]
	
	def new_bar(self):
		print 'new_bar'
		#add empty bar to end of composition
		self.comp.append(self._new_bar(self.timeSignature))	
	
	def cut_bar(self):
		print 'cut_bar'
		#remove bar from end of composition
		if len(self.comp) is 1:
			return
		else:
			del self.comp[-1]
		
	def start_loop(self):
		self.loop = True
		t = threading.Thread(target=self.loop_thread)
		self.threads.append(t)
		t.start()
		
	def stop_loop(self):
		self.loop = False
		
	def loop_thread(self):
		#loop while loop trigger is set
		while self.loop:
			#iterate through bars
			bars = range(len(self.comp))
			#iterate through 64s
			beats = range(len(self.comp[0]))
			for bar in bars:
				self.bar = bar
				for beat in beats:
					self._64 = beat
					try:
						#try to get the sounds located at this bear and this beat
						sounds = range(len(self.comp[bar][beat]))
					except Exception as e:
						break
					for s in sounds:
						try:
							#try to get the sound
							sound = self.comp[bar][beat][s]
						except Exception as e:
							break
						#if successful play the sound!
						if sound: self.play_sound_thread(sound)
					self.end=time.time()
					#sleep for time of 1 64th note minus time of overhead
					sleep_time = self.len64_sleep - (self.end-self.start)
					# print self.end-self.start
					# print sleep_time
					if sleep_time < 0:
						print 'WARNING overhead throwing off clock', sleep_time, len(sounds)
					else:
						#busy waiting better?
						#while clock something pass
						time.sleep(sleep_time)
					self.start = time.time()
		return 0
		
	def get_len64(self):
		#number of ms in a beat
		#60000 ms in a minute
		#bpm beats per minute
		#ex 60000ms / 100 bpm = 600 ms per beat
		ms_beat = 60000.0 / self.bpm
		
		#time signature: beats in bar / value of one beat
		# 4 / 4 = 4 quarter notes in 1 bar
		# 3 / 4 = 3 quarter notes in 1 bar
		# 8 / 8 = 8 eighth notes in 1 bar
		# 64 / value of one beat = number of 64 notes in a beat
		# 64 / 4 = 16 sixty-fourth notes in a quarter note
		_64s_beat = 64.0 / self.timeSignature[1]
		
		# #ms in a beat / #64s in a beat = #ms in a 64
		self.len64 = float(ms_beat) / _64s_beat
		
		# seconds to sleep between 64 notes
		self.len64_sleep = self.len64 / 1000.0
		
		
		print 'LEN64:', self.len64
		print 'LEN64_SLEEP', self.len64_sleep
		
		return self.len64
		
	def test(self):	
		self.add_sound('coin.wav', 0, 0)
		self.add_sound('coin.wav', 0, 15)
		self.add_sound('coin.wav', 0, 31)
		self.add_sound('coin.wav', 0, 46)