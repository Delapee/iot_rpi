import time
import threading
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from settings import *
from sensors.Servo import Servo
from sensors.Light import Light
from sensors.Led import Led
from sensors.TempHum import TempHum


def ligt_sensor_job():
    m = light.take_data()
    led.isActivate(light.trigger(m))

    data = {
        "raspberryId": rpi_id,
        "value": m,
        "timestamp": round(time.time() * 1000),
    }
    requests.post(url=LIGHT_ENDPOINT, json=data)


def th_sensor_job():
    hum, temp = th.take_data()

    data = {
        "raspberryId": rpi_id,
        "temperature": temp,
        "humidity": hum,
        "timestamp": round(time.time() * 1000),
    }
    requests.post(url=TEMP_ENDPOINT, json=data)


def jobs(sched):
    sched.add_job(ligt_sensor_job, "interval", seconds=10)
    sched.add_job(th_sensor_job, "interval", seconds=10)


def set_id():
    while not os.path.exists(ID_FILE):
        pass

    time.sleep(1)

    with open(ID_FILE, "r") as fp:
        id = fp.readline().strip()

    data = {
        "raspberryId": id,
        "content": "Raspberry controller service, conectada",
        "type": "Good",
    }
    requests.post(url=MSG_ENDPOINT, json=data)

    return id


if __name__ == "__main__":
    rpi_id = set_id()

    light = Light()
    led = Led()
    th = TempHum()
    servo = Servo()

    sched = BackgroundScheduler(daemon=True)
    jobs(sched)

    thread_running = False

    try:
        sched.start()
        rpi_url = f"{RPI_ENDPOINT}/{rpi_id}"

        while True:
            active = requests.get(url=rpi_url).json()["activator"]

            if active and not servo.running:
                servo.running = True
                servo_thread = threading.Thread(target=servo.run)
                servo_thread.start()
            elif not active:
                servo.running = False

            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        servo.stop()
        sched.shutdown()
