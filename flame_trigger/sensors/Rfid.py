from mfrc522 import SimpleMFRC522


class Rfid:
    def __init__(self) -> None:
        self.reader = SimpleMFRC522()

    def read(self):
        id, text = self.reader.read()
        return text
