from grove.grove_light_sensor_v1_2 import GroveLightSensor
from settings import *


class Light:
    def __init__(self) -> None:
        self.sensor = GroveLightSensor(LIGHT)

    def take_data(self):
        return self.sensor.light

    def trigger(self, ligth):
        return ligth <= LIGHT_TRIGGER
