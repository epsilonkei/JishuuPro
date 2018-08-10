import threading
import RPi.GPIO as GPIO
from time import sleep

INAPIN = 20
INBPIN = 21
SOLENOID = 23
PulseWidth = 0.002
GPIO.setmode(GPIO.BCM)
GPIO.setup(INAPIN, GPIO.OUT)
GPIO.setup(INBPIN, GPIO.OUT)
GPIO.setup(SOLENOID, GPIO.OUT)

class Solenoid(threading.Thread):
    def __init__(self, n, t):
        super(Solenoid, self).__init__()
        self.n = n
        self.t = t

    def run(self):
        print "=== Start Solenoid Thread ==="
        for i in range(self.n):
            sleep(self.t)
            print "Solenoid worked"
            GPIO.output(SOLENOID, True)
            sleep(1)
            GPIO.output(SOLENOID, False)
            sleep(1)
        print "=== Solenoid stopped"

if __name__ == '__main__':
    sole = Solenoid(5,5)
    sole.start()
    
    sleep(1)
    
    print "*** Start Rotate Motor***"
    for i in range(5):
        sleep(10)
        print "Rotate Motor"
        for i in range(50):
            GPIO.output(INAPIN, 0)
            GPIO.output(INBPIN, 0)
            sleep(PulseWidth)
            GPIO.output(INAPIN, 1)
            GPIO.output(INBPIN, 0)
            sleep(PulseWidth)
            GPIO.output(INAPIN, 1)
            GPIO.output(INBPIN, 1)
            sleep(PulseWidth)
            GPIO.output(INAPIN, 0)
            GPIO.output(INBPIN, 1)
            sleep(PulseWidth)
    print "*** Motor Stopped ***"

    GPIO.cleanup()
