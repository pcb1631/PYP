import os

def get_key():
    if os.name == 'nt':  # For Windows
        import msvcrt
        if msvcrt.kbhit():  # Check if key pressed
            key = msvcrt.getch()
            return key
    else:  # For macOS and Linux
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
    return None