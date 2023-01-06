from settings import *
import RPi.GPIO as GPIO


class Buzzer:
    def __init__(self) -> None:
        self.channel = BUZZER

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

    def isActivate(self, output):
        GPIO.output(self.channel, output)
