import time
import threading
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import make_chunks
from pydub.effects import *

from composition import Sound
from composition import Composition
from composition import open
from composition import cut_tool

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import array

import IPython

comp = Composition()
lib = comp.library

#make samp tool
#make a beat

#frequency limits/zones
#16 to 32
#32 to 512
#512 to 2048
#2048 to 8192
#8192 to 16384

#C
#16.351
#32.703
#65.406
#130.813
#261.626
#523.251
#1046.502
#2093.005
#4186.009
#8372.018

def flatten_samp_chunks(samp_chunks):
	samp = []
	for chunk in samp_chunks:
		for c in chunk:
			samp.append(c)
	return samp

def flatten(bumpy):
	#recursive function to flatten an arbitrarily nested array into a single dimensional array
	flat_array = []
	if len(bumpy) > 0:
		for x in bumpy:
			if isinstance(x, list):
				flat_array += flatten(x)
			else:
				flat_array += [x]
	return flat_array

def rando(name):
	path = os.getcwd() + "\\sounds\\" + name	
	seg = AudioSegment.from_file(path, format="wav")
	
	seg_chunks = np.array(make_chunks(seg, 100))
	samp_chunks = []
	for chunk in seg_chunks:
		samp_chunks.append(chunk.get_array_of_samples())
	
	np.random.shuffle(samp_chunks)
	new_samp = flatten_samp_chunks(samp_chunks)
	
	arr = array.array(seg.array_type, new_samp)
	new_seg = seg._spawn(arr)
	print len(new_seg)
	return new_seg

def test_filter():

	start = time.time()
	###########################
	sound = comp.get_sound('RNDYSVGE_frog_eyes.wav')
	_sound = low_pass_filter(sound.segment, 200)
	#####################
	end = time.time()
	print(end - start)*1000
	
	octaves = [16.351, 32.703, 65.406, 130.813, 261.626, 523.251, 1046.502, 2093.005, 4186.009, 8372.018]
	for c in range(len(octaves))[1:]:
		# print octaves[c-1], octaves[c]
		# name = str(int(octaves[c-1])) + "_" + str(int(octaves[c])) + ".wav"
		name = str(int(octaves[c])) + ".wav"
		print name
		low_pass_filter(sound.segment, octaves[c]).export(name, format="wav")
		

def test_input_int():
	a = 100
	while True:
		data = input("Enter a number: ")
		print data, type(data)
		
def main():
	name = 'RNDYSVGE_frog_eyes.wav'
	
	cut_tool(name)
	
	# test_input_int()
	
	
	# test_filter()
	# s = rando('roar.wav')
	# play(s)
	return
	
if __name__ == "__main__":
	main()