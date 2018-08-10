#!/usr/bin/env python

import sys, select, termios, tty

import threading
import RPi.GPIO as GPIO
from time import sleep

A1 = 23
B1 = 24
A2 = 20
B2 = 21
SOLENOID = 16
PulseWidth = 0.002
SleepTime = 0.01
GPIO.setmode(GPIO.BCM)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(B1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)
GPIO.setup(SOLENOID, GPIO.OUT)
POS_a = [0,1,1,0]
POS_b = [0,0,1,1]
INI_TOP = 466
INI_LEFT = 142
STEP = 50

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
            GPIO.output(A1, POS_b[i%4])
            GPIO.output(B1, POS_a[i%4])
            sleep(PulseWidth)
        sleep(SleepTime)

    def down(self, size):
        print "Down"
        for i in range(size):
            GPIO.output(A1, POS_a[i%4])
            GPIO.output(B1, POS_b[i%4])
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

class Machine:
    def __init__(self):
        self.sole = Solenoid()
        self.above = AboveMotor()
        self.bottom = BottomMotor()
    
    def start(self):
        self.sole.start()
        self.above.start()
        self.bottom.start()
    
    def up(self):
        self.above.up(STEP)

    def down(self):
        self.above.down(STEP)
        
    def left(self):
        self.bottom.right(STEP)

    def right(self):
        self.bottom.left(STEP)
        
    def push(self):
        self.sole.push()

    def pull(self):
        self.sole.pull()

    def goto(self, x, y):
        self.above.up(INI_TOP - STEP*x)
        self.bottom.left(INI_LEFT + STEP*y)

    def back(self, x, y):
        self.above.down(INI_TOP - STEP*x)
        self.bottom.right(INI_LEFT + STEP*y)
    
if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    machine = Machine()
    machine.start()
    
    try:
        while True:
            key = getKey()
            print key
            if key == 'w':
                machine.up()
            elif key == 's':
                machine.down()
            elif key == 'a':
                machine.left()
            elif key == 'd':
                machine.right()
            elif key == 'z':
                machine.push()
            elif key == 'x':
                machine.pull()
            elif key == 'g':
                machine.goto(1,3)
            elif key == 'b':
                machine.back(1,3)
            elif key in ['\x1b']:
                break

    except KeyboardInterrupt:
        pass
    
    GPIO.cleanup()
