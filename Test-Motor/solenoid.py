#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import signal
import sys
import time

GPIO_ID = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_ID, GPIO.OUT)

def exit_handler(signal, frame):
  # Ctrl+Cが押されたときにデバイスを初期状態に戻して終了する。
  print("\nExit")
  GPIO.cleanup()
  sys.exit(0)

# 終了処理用のシグナルハンドラを準備
signal.signal(signal.SIGINT, exit_handler)

while True:
  GPIO.output(GPIO_ID, True)
  time.sleep(0.5)
  GPIO.output(GPIO_ID, False)
  time.sleep(0.5)
