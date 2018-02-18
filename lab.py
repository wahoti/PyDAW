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

import threading

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

def pitch_test_wave():	
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	
	#wave (stackoverflow)
	#https://stackoverflow.com/questions/43963982/python-change-pitch-of-wav-file
	wr = wave.open(path, 'r')
	# Set the parameters for the output file
	par = list(wr.getparams())
	par[3] = 0  # The number of samples will be set by writeframes.
	par = tuple(par)
	ww = wave.open('pitch1.wav', 'w')
	ww.setparams(par)
	fr = 20
	sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
	# A larger number for fr means less reverb.
	c = int(wr.getnframes()/sz)  # count of the whole file
	shift = 100//fr  # shifting 100 Hz
	# for num in range(c):
	
	da = np.fromstring(wr.readframes(sz), dtype=np.int16)
	left, right = da[0::2], da[1::2]  # left and right channel
	lf, rf = np.fft.rfft(left), np.fft.rfft(right)
	lf, rf = np.roll(lf, shift), np.roll(rf, shift)
	lf[0:shift], rf[0:shift] = 0, 0
	nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
	ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
	ww.writeframes(ns.tostring())
	wr.close()
	ww.close()
	
def pitch_test_pydub(octaves, hi):
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	
	sound = AudioSegment.from_file(path, format="wav")
	
	start = time.time()	
	
	# shift the pitch up by half an octave (speed will increase proportionally)
	# octaves = .5

	new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

	# keep the same samples but tell the computer they ought to be played at the 
	# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
	hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
	
	# now we just convert it to a common sample rate (44.1k - standard audio CD) to 
	# make sure it works in regular audio players. Other than potentially losing audio quality (if
	# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
	# hipitch_sound = hipitch_sound.set_frame_rate(44100)

	slow_sample_rate = int(sound.frame_rate / (2.0 ** octaves))
	lopitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': slow_sample_rate})
	# lopitch_sound = lopitch_sound.set_frame_rate(44100)
	
	end = time.time()
	print(end - start)*1000
	
	#Play pitch changed sound
	# play(sound)
	if hi:
		play(hipitch_sound)
	else:
		play(lopitch_sound)

	#export / save pitch changed sound
	# hipitch_sound.export("out.wav", format="wav")

def pitch_test():
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	
	#pydub
	sound = AudioSegment.from_file(path, format="wav")
	samples = sound.get_array_of_samples()
	play(sound)
	
	start = time.time()
	
	fr = 20
	shift = 100//fr  # shifting 100 Hz
	
	
	print sound.channels
	print sound.array_type
	
	if sound.channels is 1:
		f = np.fft.rfft(samples)
		f = np.roll(f, shift)
		f[0:shift] = 0
		n = np.fft.irfft(f)
		n = np.column_stack(f).ravel().astype(np.int16)
	elif sound.channels is 2:
		left, right = samples[0::2], samples[1::2]
		lf, rf = np.fft.rfft(left), np.fft.rfft(right)	
		lf, rf = np.roll(lf, shift), np.roll(rf, shift)
		lf[0:shift], rf[0:shift] = 0, 0
		nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
		n = np.column_stack((nl, nr)).ravel().astype(np.int16)
	
	new_samples_array = array.array(sound.array_type, n)
	new_sound = sound._spawn(new_samples_array)
	
	end = time.time()
	print(end - start)*1000
	
	play(new_sound)
	
	
def chord_test():
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	sound = AudioSegment.from_file(path, format="wav")

	octaves = [0] * 1
	
	start = time.time()
	
	for octave in octaves:
		new_sample_rate = int(sound.frame_rate * (2 ** octave))
		new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
		play_sound_thread(new_sound)
	
	end = time.time()
	print(end - start)*1000

def play_sound_pydub(sound):
	play(sound)
	return 0

def play_sound_thread(sound):
	t = threading.Thread(target=play_sound_pydub, args=[sound])
	t.start()
	return 0
	
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
	
def make_chunks(audio_segment, chunk_length):
    """
    Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
    long.
    if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    segments back (except the last one, which can be shorter)
    """
    number_of_chunks = math.ceil(len(audio_segment) / float(chunk_length))
    return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
            for i in range(int(number_of_chunks))]
	
def hm():
	path = "C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav"
	sound = AudioSegment.from_file(path)
	samples = sound.get_array_of_samples()
	raw_audio_data = sound.raw_data
	# winsound.PlaySound(raw_audio_data, winsound.SND_MEMORY)

	seg = sound

	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(seg.sample_width),
		channels=seg.channels,
		rate=seg.frame_rate,
		output=True)

	chunks = make_chunks(seg, 100)
	print len(chunks)
		
		
	# break audio into half-second chunks (to allows keyboard interrupts)
	for x in range(len(chunks)):
		if x == 5:
			break
		stream.write(chunks[x]._data)

	stream.stop_stream()
	stream.close()

	p.terminate()
	
def main():
	# sound1 = AudioSegment.from_file("C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav", format="wav")
	# play(sound1)
	# hm()
	
	# pitch_test()
	# pitch_test_wave()
	# pitch_test_pydub()
	
	# for x in range(9)[1:]:
		# octaves = x * .125
		# print octaves
		# pitch_test_pydub(octaves, False)
	chord_test()
	
	# raw()
	# filter()
	
	
	# myBoop()
	
	
	# start = time.time()
	# boop(16000, 500, 1)	
	# end = time.time()
	# print(end - start)
	
	return 0

if __name__ == "__main__":
	main()