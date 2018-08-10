import RPi.GPIO as GPIO
from time import sleep

INAPIN = 20
INBPIN = 21
PulseWidth = 0.002
GPIO.setmode(GPIO.BCM)
GPIO.setup(INAPIN, GPIO.OUT)
GPIO.setup(INBPIN, GPIO.OUT)
output_A = [0,1,1,0]
output_B = [0,0,1,1]

try:
    for i in range(200):
        GPIO.output(INAPIN, output_A[i%4])
        GPIO.output(INBPIN, output_B[i%4])
        sleep(PulseWidth)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
