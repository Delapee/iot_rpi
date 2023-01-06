from settings import *
import RPi.GPIO as GPIO


class Led:
    def __init__(self) -> None:
        self.channel = LED

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

    def isActivate(self, output):
        GPIO.output(self.channel, output)
