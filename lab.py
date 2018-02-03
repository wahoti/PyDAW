import pydub
from pydub import AudioSegment
from pydub.playback import play

import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio     #initialize pyaudio

import time

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

	
def main():
	# sound1 = AudioSegment.from_file("C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav", format="wav")
	# play(sound1)
	
	myBoop()
	
	
	# start = time.time()
	# boop(16000, 500, 1)	
	# end = time.time()
	# print(end - start)
	
	return 0

if __name__ == "__main__":
	main()