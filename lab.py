import pydub
from pydub import AudioSegment
from pydub.playback import play

import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio     #initialize pyaudio

import time

import winsound

import pymedia

import wave

from StringIO import StringIO

import numpy as np

import array

def boop(BITRATE, FREQUENCY, LENGTH):
	# BITRATE = 16000     #number of frames per second/frameset.      
	# FREQUENCY = 500     #Hz, waves per second, 261.63=C4-note.
	# LENGTH = 1     #seconds to play sound
	if FREQUENCY > BITRATE: BITRATE = FREQUENCY+100
	NUMBEROFFRAMES = int(BITRATE * LENGTH)
	RESTFRAMES = NUMBEROFFRAMES % BITRATE
	WAVEDATA = ''    
	for x in xrange(NUMBEROFFRAMES):
		WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    
	for x in xrange(RESTFRAMES): 
		WAVEDATA = WAVEDATA+chr(128)
	
	p = PyAudio()
	stream = p.open(format = p.get_format_from_width(1), 
					channels = 1, 
					rate = BITRATE, 
					output = True)

	stream.write(WAVEDATA)
	stream.stop_stream()
	stream.close()
	p.terminate()

def myBoop():
	BITRATE = 16000     #number of frames per second/frameset.      
	FREQUENCY = 500     #Hz, waves per second, 261.63=C4-note.
	LENGTH = 1     #seconds to play sound
	if FREQUENCY > BITRATE: BITRATE = FREQUENCY+100
	NUMBEROFFRAMES = int(BITRATE * LENGTH)
	RESTFRAMES = NUMBEROFFRAMES % BITRATE
	WAVEDATA = ''    
	for x in xrange(NUMBEROFFRAMES):
		WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    
	for x in xrange(RESTFRAMES): 
		WAVEDATA = WAVEDATA+chr(128)
		
	p = PyAudio()
	stream = p.open(format = p.get_format_from_width(1), 
					channels = 1, 
					rate = BITRATE, 
					output = True)

	start = time.time()
	stream.write(WAVEDATA)
	end = time.time()
	print(end - start)		
	
	stream.write(WAVEDATA)
	stream.write(WAVEDATA)
	
	
	stream.stop_stream()
	stream.close()
	p.terminate()


def filter():
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	# file_on_disk = open(path, 'rb')
	# file_in_memory = StringIO(file_on_disk.read())
	# file_on_disk.seek(0)
	# file_in_memory.seek(0)
	# file_on_disk.read() == file_in_memory.read()

	# f = wave.open(file_in_memory, 'rb')
	# f= wave.open("C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav", 'rb' )
	
	# sampleRate= f.getframerate()
	# channels= f.getnchannels()
	# format= pymedia.audio.sound.AFMT_S16_LE
	# print sampleRate, channels, format
	# snd= pymedia.audio.sound.Output( sampleRate, channels, format )
	# s= f.readframes( 300000 )
	# snd.play( s )
	# while snd.isPlaying(): time.sleep( 0.05 )



	sound = AudioSegment.from_file(path, format="wav")
	
	#play sound
	play(sound)
	
	#get new audio segment that is a filter
	
	# make sound1 louder by 3.5 dB
	louder_via_method = sound.apply_gain(+100)
	
	play(sound)
	
	# louder_via_operator = sound + 3.5

	# make sound1 quieter by 5.7 dB
	# quieter_via_method = sound.apply_gain(-5.7)
	# quieter_via_operator = sound - 5.7
	
	#get raw data
	# raw_audio_data = sound.raw_data
	#play it with winsound
	# winsound.PlaySound(raw_audio_data, winsound.SND_MEMORY)
	#alter it
	#play it with winsound
	
def raw():
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	sound = AudioSegment.from_file(path)
	samples = sound.get_array_of_samples()

	start = time.time()
	
	shifted_samples = np.right_shift(samples, 1)

	# now you have to convert back to an array.array
	shifted_samples_array = array.array(sound.array_type, shifted_samples)

	new_sound = sound._spawn(shifted_samples_array)	
	end = time.time()
	print(end - start)*1000
	play(sound)
	play(new_sound)
	
def main():
	# sound1 = AudioSegment.from_file("C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav", format="wav")
	# play(sound1)
	
	
	raw()
	# filter()
	
	
	# myBoop()
	
	
	# start = time.time()
	# boop(16000, 500, 1)	
	# end = time.time()
	# print(end - start)
	
	return 0

if __name__ == "__main__":
	main()