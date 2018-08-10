#!/usr/bin/env python

import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
    
if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    try:
        while True:
            key = getKey()
            print key
            if key in ['\x1b']:
                break

    except KeyboardInterrupt:
        pass
