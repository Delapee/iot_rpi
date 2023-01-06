import concurrent.futures
import time
from sensors.Buzzer import Buzzer
from sensors.Flame import Flame
from sensors.Rfid import Rfid


# def send_data(activate):
#     print(activate)


def deactivate(rfid):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(rfid.read())
        name = future.result()

        return name


if __name__ == "__main__":
    flame = Flame()
    buzzer = Buzzer()
    rfid = Rfid()

    # id

    while True:

        if flame.activate:
            buzzer.isActivate(True)
            # send_data("Se ha activado la alarma de incendios.", "Advert")

            name = rfid.read()

            # send_data(f"{name} ha desactivado la alarma", "Good")
            buzzer.isActivate(False)
            flame.activate = False

        time.sleep(1)
