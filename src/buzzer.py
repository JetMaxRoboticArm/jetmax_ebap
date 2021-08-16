import Jetson.GPIO as GPIO

PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)


def on():
    GPIO.output(23, 1)


def off():
    GPIO.output(23, 0)
