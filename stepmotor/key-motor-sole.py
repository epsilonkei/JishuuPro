#!/usr/bin/env python

import sys, select, termios, tty

import threading
import RPi.GPIO as GPIO
from time import sleep

A1 = 17
B1 = 22
A2 = 20
B2 = 21
SOLENOID = 16
PulseWidth = 0.002
SleepTime = 0.1
GPIO.setmode(GPIO.BCM)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(B1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)
GPIO.setup(SOLENOID, GPIO.OUT)
POS_a = [0,1,1,0]
POS_b = [0,0,1,1]

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class Solenoid(threading.Thread):
    def __init__(self):
        super(Solenoid, self).__init__()

    def push(self):
        print "Push"
        GPIO.output(SOLENOID, True)
        sleep(SleepTime)

    def pull(self):
        print "Pull"
        GPIO.output(SOLENOID, False)
        sleep(SleepTime)
        
class AboveMotor(threading.Thread):
    def __init__(self):
        super(AboveMotor, self).__init__()

    def up(self, size):
        print "Up"
        for i in range(size):
            GPIO.output(A1, POS_a[i%4])
            GPIO.output(B1, POS_b[i%4])
            sleep(PulseWidth)
        sleep(SleepTime)

    def down(self, size):
        print "Up"
        for i in range(size):
            GPIO.output(A1, POS_b[i%4])
            GPIO.output(B1, POS_a[i%4])
            sleep(PulseWidth)
        sleep(SleepTime)

class BottomMotor(threading.Thread):
    def __init__(self):
        super(BottomMotor, self).__init__()

    def left(self, size):
        print "Left"
        for i in range(size):
            GPIO.output(A2, POS_a[i%4])
            GPIO.output(B2, POS_b[i%4])
            sleep(PulseWidth)
        sleep(SleepTime)

    def right(self, size):
        print "Right"
        for i in range(size):
            GPIO.output(A2, POS_b[i%4])
            GPIO.output(B2, POS_a[i%4])
            sleep(PulseWidth)
        sleep(SleepTime)
    
if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    sole = Solenoid()
    sole.start()
    above = AboveMotor()
    above.start()
    bottom = BottomMotor()
    bottom.start()

    try:
        while True:
            key = getKey()
            print key
            if key == 'w':
                above.up(40)
            elif key == 's':
                above.down(40)
            elif key == 'a':
                bottom.left(40)
            elif key == 'd':
                bottom.right(40)
            elif key == 'z':
                sole.push()
            elif key == 'x':
                sole.pull()
            elif key in ['\x1b']:
                break

    except KeyboardInterrupt:
        pass
    
    GPIO.cleanup()
