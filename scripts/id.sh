#!/bin/bash

echo $( curl -X POST -H "Content-Type: application/json" https://iot-server-nine.vercel.app/api/raspberry ) | tr -d '"' > ~/dev/iot_rpi/id_rpi.txt