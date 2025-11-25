import os
import sys
if os.name != 'nt':
    import tty
    import termios

def get_key():
    if os.name == 'nt':  # For Windows
        import msvcrt
        if msvcrt.kbhit():  # Check if key pressed
            key = msvcrt.getch()
            return key
    else:  # For macOS and Linux
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            if key == "\x1b":
                key += sys.stdin.read(2)
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 

while True: #   for debugging (wont run if imported)
    key = get_key()

    if os.name == 'nt': #   Windows is a bit weird because it will return a constant stream of 'None' even if i try to prevent it in get_key(), 
        if key != None: #   so you have to do this manually everytime you call it
            if key == b'\xe0':
                key = key + get_key()
            print(key)
    else:
        print(key) #    For linux, get_key() only return a key if its pressed


#   Windows
#   up =    b'\xe0' , b'H'
#   down =  b'\xe0' , b'P'
#   left =  b'\xe0' , b'K'
#   right = b'\xe0' , b'M'

#   Linux
#   up =
#   down =
#   left =
#   right =