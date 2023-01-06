from settings import *
import RPi.GPIO as GPIO


class Flame:
    def __init__(self) -> None:
        self.channel = FLAME
        self.activate = False

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)
        GPIO.add_event_detect(self.channel, GPIO.BOTH, bouncetime=300)
        GPIO.add_event_callback(self.channel, self.callback)

    def callback(self, channel):
        self.activate = not self.activate
