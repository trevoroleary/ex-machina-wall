from RPi import GPIO


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

GPIO.output(21, GPIO.HIGH)
x = 1
GPIO.output(21, GPIO.LOW)
x = 1
