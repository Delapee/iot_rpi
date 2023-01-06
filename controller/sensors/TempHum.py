from seeed_dht import DHT
from settings import *


class TempHum:
    def __init__(self) -> None:
        self.sensor = DHT("11", TEMP_HUM)

    def take_data(self):
        return self.sensor.read()
