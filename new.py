from pyo import *

def main():
	s = server_start()
	###################
	
	
	# a = Sine(220, 0, 0.1).out()
	# a = hello_audio(s)
	# a = hello_audio_plus(s)
	
	###################
	s.start()
	time.sleep(60)
	s.stop()
	
	
def config_info():
	print("Default input device: %i" % pa_get_default_input())
	print("Default output device: %i" % pa_get_default_output())
	print pa_list_host_apis()
	print pa_list_devices()
	print pa_get_default_devices_from_host('wasapi')

	# s = Server(sr=48000, nchnls=1, buffersize=512, duplex=0, winhost="asio").boot()
	# s = Server(sr=48000, buffersize=512, duplex=0, winhost="WASAPI").boot()
	# s = Server(sr=48000, buffersize=512, duplex=0, winhost="MME").boot()
	# s = Server(sr=48000, buffersize=512, duplex=0, winhost="Windows DirectSound").boot()
	# s = Server(sr=48000, buffersize=512, duplex=0, audio='pa', winhost="Windows WDM-KS").boot()

	#default
	#(self, sr=44100, nchnls=2, buffersize=256, duplex=1, audio='portaudio', 
	#jackname='pyo', ichnls=None, winhost="wasapi", midi="portmidi"):

def server_start():
	host_apis = ["mme", "directsound", "asio", "wasapi", "wdm-ks"]
	s = Server(sr=48000, buffersize=512, duplex=0, winhost=host_apis[3])
	s.verbosity = 8
                    # - 1 = error
                    # - 2 = message
                    # - 4 = warning
                    # - 8 = debug
	# s.deactivateMidi()
	#- setMidiOutputDevice(x): Set the MIDI output device number. See `pm_list_devices()
	s.setOutputDevice(8)
	s.setInputDevice(9)

	s.boot()
	return s

def hello_audio_plus(s):
	# Drops the gain by 20 dB.
	s.amp = 0.1

	# Creates a sine wave as the source to process.
	a = Sine()

	# Passes the sine wave through an harmonizer.
	hr = Harmonizer(a).out()

	# Also through a chorus.
	ch = Chorus(a).out()

	# And through a frequency shifter.
	sh = FreqShift(a).out()

	return [hr, ch, sh]
	# return sh
	
	# s.gui(locals())	
	
def hello_audio(s):
	# Drops the gain by 20 dB.
	s.amp = 0.1

	# Creates a sine wave player.
	# The out() method starts the processing
	# and sends the signal to the output.
	return Sine().out()

def gen1(s):
	# Sets fundamental frequency.
	freq = 187.5

	# Impulse train generator.
	lfo1 = Sine(.1).range(1, 50)
	osc1 = Blit(freq=freq, harms=lfo1, mul=0.3)

	# RC circuit.
	lfo2 = Sine(.1, mul=0.5, add=0.5)
	osc2 = RCOsc(freq=freq, sharp=lfo2, mul=0.3)

	# Sine wave oscillator with feedback.
	lfo3 = Sine(.1).range(0, .18)
	osc3 = SineLoop(freq=freq, feedback=lfo3, mul=0.3)

	# Roland JP-8000 Supersaw emulator.
	lfo4 = Sine(.1).range(0.1, 0.75)
	osc4 = SuperSaw(freq=freq, detune=lfo4, mul=0.3)

	# Interpolates between input objects to produce a single output
	sel = Selector([osc1, osc2, osc3, osc4]).out()
	# sel.ctrl(title="Input interpolator (0=Blit, 1=RCOsc, 2=SineLoop, 3=SuperSaw)")

	# Displays the waveform of the chosen source
	# sc = Scope(sel)

	# Displays the spectrum contents of the chosen source
	# sp = Spectrum(sel)

	# s.gui(locals())

def gen2():
	wav = SquareTable()
	env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
	met = Metro(.125, 12).play()
	amp = TrigEnv(met, table=env, mul=.1)
	pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
	out = Osc(table=wav, freq=pit, mul=amp).out()

if __name__ == "__main__":
	main()

#N O T E S
	
#oscillator: generates a repeating sound waveform
#	has a controllable parameter for frequency it repeats

#envelope generator: generates an audio signal in the range of 0 to 1,
#	volume control

#amplifiercode: simply multiplies, oscillator output with envelope generator output
#	sample by sample

#filter: shape the frequency content of the oscillator before it gets to the amplifier.

#Many synthesis algorithms depend on more than one oscillator,
#	either in parallel (e.g., additive synthesis, rich sound by adding many simple waveforms)
#	or through modulation (e.g., frequency modulation, one oscillator modulates the pitch of another).


