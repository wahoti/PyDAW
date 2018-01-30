import sys
import sdl2
import sdl2.ext

def run():
    window = sdl2.ext.Window("hi", size=(800, 600))
    window.show()
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()
    return 0

def run2():
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
	sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
	joystick = sdl2.SDL_JoystickOpen(0)
	sdl2.ext.init()
	window = sdl2.ext.Window("test", size=(800,600),position=(0,0),flags=sdl2.SDL_WINDOW_SHOWN)
	window.refresh()
	while True:
		for event in sdl2.ext.get_events():
			if event.type==sdl2.SDL_KEYDOWN:
				print sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
			elif event.type==sdl2.SDL_JOYAXISMOTION:
				print [event.jaxis.axis,event.jaxis.value]
	return 0
	
if __name__ == "__main__":
	sys.exit(run2())
    # sys.exit(run())