import time
import threading
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import make_chunks
from pydub.effects import *

from composition import Sound
from composition import Composition

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import array

comp = Composition()
lib = comp.library

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

def chop_save(name):
	path = os.getcwd() + "\\sounds\\" + name
	out_path = os.getcwd() + "\\cuts\\"
	try:
		seg = AudioSegment.from_file(path, format="wav")
	except Exception as e:
		print e
		return
	segs = make_chunks(seg, 100)
	try:
		count = 0
		for s in segs:
			s.export(out_path + name.split('.')[0] + "_" + str(count) + ".wav", format="wav")
			count += 1
	except Exception as e:
		print e
		return
	return segs

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
		

def main():
	test_filter()
	return
	
if __name__ == "__main__":
	main()