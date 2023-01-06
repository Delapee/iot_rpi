import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler

from sensors.Servo import Servo
from sensors.Light import Light
from sensors.Led import Led
from sensors.TempHum import TempHum


def ligt_sensor_job():
    m = light.take_data()
    led.isActivate(light.trigger(m))
    print(m)


def th_sensor_job():
    hum, temp = th.take_data()
    print(temp, hum)


def jobs(sched):
    sched.add_job(ligt_sensor_job, "interval", seconds=10)
    sched.add_job(th_sensor_job, "interval", seconds=10)


if __name__ == "__main__":
    light = Light()
    led = Led()
    th = TempHum()
    servo = Servo()

    sched = BackgroundScheduler(daemon=True)
    jobs(sched)

    thread_running = False

    try:
        sched.start()
        while True:
            # llamada a la api para saver si se enciende o se apagado
            active = True

            if active and not servo.running:
                servo.running = True
                servo_thread = threading.Thread(target=servo.run)
                servo_thread.start()
            else:
                servo.running = False

            time.sleep(2)

    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()
