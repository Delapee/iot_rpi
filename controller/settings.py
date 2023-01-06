# Digital
LED = 5  # D5
TEMP_HUM = 18  # D18

# Analog
LIGHT = 0  # A0

# PWM
SERVO = 12

# Triggers
LIGHT_TRIGGER = 40

# ID file
ID_FILE = "/home/papaia/dev/iot_rpi/id_rpi.txt"

# API
URL = "192.168.1.34:3000"
MSG_ENDPOINT = f"http://{URL}/api/sensor/message"
TEMP_ENDPOINT = f"http://{URL}/api/sensor/temperature"
LIGHT_ENDPOINT = f"http://{URL}/api/sensor/ligth"
RPI_ENDPOINT = f"http://{URL}/api/raspberry"
