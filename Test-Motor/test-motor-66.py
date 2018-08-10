import RPi.GPIO as GPIO
from time import sleep

INAPIN = 23
INBPIN = 24
PulseWidth = 5.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(INAPIN, GPIO.OUT)
GPIO.setup(INBPIN, GPIO.OUT)

try:
    while True:
        for i in range(180):
            GPIO.output(INAPIN, GPIO.HIGH)
            GPIO.output(INBPIN, GPIO.HIGH)
            sleep(PulseWidth)
            GPIO.output(INAPIN, GPIO.LOW)
            GPIO.output(INBPIN, GPIO.HIGH)
            sleep(PulseWidth)
            GPIO.output(INAPIN, GPIO.LOW)
            GPIO.output(INBPIN, GPIO.LOW)
            sleep(PulseWidth)
            GPIO.output(INAPIN, GPIO.HIGH)
            GPIO.output(INBPIN, GPIO.LOW)
            sleep(PulseWidth)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
