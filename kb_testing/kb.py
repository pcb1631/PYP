import os
import sys
if os.name != 'nt':
    import tty
    import termios
    import select
from time import sleep   

x = 0
while True:
    if os.name == 'nt':
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':
                key += msvcrt.getch()
            if key == b'w':
                x += 1
            elif key == b's':
                x -= 1
        else:
            print(x)
    else:
        dr,dw,de = select.select([sys.stdin], [], [], 0)
        print(dr,dw,de)
        sleep(0.1)
        if dr != []:
            exit()
        else:
            pass