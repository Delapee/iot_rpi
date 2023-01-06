import time
import requests
import os
from dotenv import load_dotenv

from mail.mail import send_mail
from sensors.Buzzer import Buzzer
from sensors.Flame import Flame
from sensors.Rfid import Rfid
from settings import *


def send_msg(id, msg, type):
    data = {"raspberryId": id, "content": msg, "type": type}
    requests.post(url=MSG_ENDPOINT, data=data)


def set_id():
    while not os.path.exists(ID_FILE):
        pass

    time.sleep(1)

    with open(ID_FILE, "r") as fp:
        id = fp.readline().strip()

    send_msg(id, "Raspberry conectada", "Good")

    return id


if __name__ == "__main__":
    load_dotenv()

    rpi_id = set_id()

    flame = Flame()
    buzzer = Buzzer()
    rfid = Rfid()

    while True:

        if flame.activate:
            buzzer.isActivate(True)
            send_msg(rpi_id, "Se ha activado la alarma de incendios.", "Error")
            send_mail("Alarma de Incendios", "Se ha activado la alarma de incendios.")

            name = rfid.read()
            name = name.replace(" ", "")

            buzzer.isActivate(False)
            flame.activate = False
            send_msg(rpi_id, f"{name} ha desactivado la alarma de incendios.", "Advert")
            send_mail(
                "Alarma de Incendios", f"{name} ha desactivado la alarma de incendios."
            )

        time.sleep(1)
