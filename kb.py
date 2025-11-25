import os
import sys
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
    return None