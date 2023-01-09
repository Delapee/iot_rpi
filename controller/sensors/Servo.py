import time
from settings import *
import RPi.GPIO as GPIO


class Servo:
    def __init__(self) -> None:
        self.channel = SERVO
        self.running = False
        self.setup()
        self.sensor = GPIO.PWM(self.channel, 50)

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

    def start(self):
        self.sensor.start(0)

    def stop(self):
        self.sensor.stop()

    def move(self):
        self.sensor.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        self.sensor.ChangeDutyCycle(5)
        time.sleep(0.5)
        self.sensor.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        self.sensor.ChangeDutyCycle(10)
        time.sleep(0.5)
        self.sensor.ChangeDutyCycle(12.5)
        time.sleep(0.2)
        self.sensor.ChangeDutyCycle(10)
        time.sleep(0.2)
        self.sensor.ChangeDutyCycle(7.5)
        time.sleep(0.2)
        self.sensor.ChangeDutyCycle(5)
        time.sleep(0.2)

    def run(self):
        self.start()
        while self.running:
            self.move()
