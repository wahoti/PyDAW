import pydub
from pydub import AudioSegment
from pydub.playback import play

def main():
	sound1 = AudioSegment.from_file("C:\\Users\\wahed\\Desktop\\daw\\pydaw\\sounds\\level_enter.wav", format="wav")
	play(sound1)
	return 0

if __name__ == "__main__":
	main()