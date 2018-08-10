import RPi.GPIO as GPIO
from time import sleep

INAPIN = 20
INBPIN = 21
PulseWidth = 0.002
GPIO.setmode(GPIO.BCM)
GPIO.setup(INAPIN, GPIO.OUT)
GPIO.setup(INBPIN, GPIO.OUT)

try:
#    while True:
    print("***Rotate Motor***")
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
    sleep(5.0)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
