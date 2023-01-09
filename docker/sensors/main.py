import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import random
from settings import *


def ligt_sensor_job():
    data = {
        "raspberryId": rpi_id,
        "value": random.randint(30, 100),
        "timestamp": round(time.time() * 1000),
    }
    requests.post(url=LIGHT_ENDPOINT, json=data)


def th_sensor_job():
    data = {
        "raspberryId": rpi_id,
        "temperature": random.randint(5, 20),
        "humidity": random.randint(40, 60),
        "timestamp": round(time.time() * 1000),
    }
    requests.post(url=TEMP_ENDPOINT, json=data)


def jobs(sched):
    sched.add_job(ligt_sensor_job, "interval", seconds=10)
    sched.add_job(th_sensor_job, "interval", seconds=10)


def set_id():
    id = requests.post(url=RPI_ENDPOINT).json()

    data = {
        "raspberryId": id,
        "content": "Docker conectado",
        "type": "Good",
    }
    requests.post(url=MSG_ENDPOINT, json=data)

    return id


if __name__ == "__main__":
    rpi_id = set_id()

    sched = BackgroundScheduler(daemon=True)
    jobs(sched)

    try:
        sched.start()

        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()
