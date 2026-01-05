import os
import sys
if os.name == 'nt':
    import msvcrt
if os.name != 'nt':
    import tty
    import termios

def get_key():
    """
    Halts the program until a key is pressed. (Blocking input)

    :return: The pressed key as bytes or string
    :rtype: bytes or str
    """
    if os.name == 'nt':  # For Windows
        key = msvcrt.getch()
        if key == b'\xe0':
            key += msvcrt.getch()
        return key
    else:  # For macOS and Linux
        fd = sys.stdin.fileno() # file descriptor, 0 = stdin, 1 = stdout, 2 = stderr
        old_settings = termios.tcgetattr(fd) # store old settings
        try:
            tty.setraw(sys.stdin.fileno()) # set raw mode
            key = sys.stdin.read(1) # read 1 byte
            if key == "\x1b":       # this is what arrow keys start with
                key += sys.stdin.read(2) # read 2 more bytes
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # reset settings to old settings

#   Windows
#   up      =    b'\xe0' , b'H'
#   down    =    b'\xe0' , b'P'
#   left    =    b'\xe0' , b'K'
#   right   =    b'\xe0' , b'M'
#   ESC     =    b'\x1b'
#   ENTER   =    b'\r' 
#   Windows won't print CTRL+C, so you just have to do try except KeyboardInterrupt

#   Linux
#   up      =    '\x1b[A'
#   down    =    '\x1b[B'
#   left    =    '\x1b[D'
#   right   =    '\x1b[C'
#   CTRl+C  =    '\x03'
#   ESC     =    '\x1b'
#   ENTER   =    '\r'