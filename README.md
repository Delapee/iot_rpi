# Sistema de control y alarma

Este proyecto proporciona un controlador, un sistema de alarma y un contenedor Docker escalable. Todo ello esta preparado para funcionar en una Raspberry PI de forma automática cuando se inicie el sistema.

## Prerequisitos

* [Python 3.9](https://www.python.org/downloads/)
* Raspberry Pi Model 3B+
* [Grove Hat](https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/)
* Sensores:
    * Analógicos:
        * [Light Sensor v1.2](https://seeeddoc.github.io/Grove-Light_Sensor_v1.2/)
        * Servo
    * MCU:
        * Sensor [RFID-RC522](https://pimylifeup.com/raspberry-pi-rfid-rc522/)
    * Digitales:
        * [Temperature&Humidity v1.2](https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
        * [Led Socket v1.5](https://wiki.seeedstudio.com/Grove-LED_Socket_Kit/)
        * [Flame Sensor v1.1](https://wiki.seeedstudio.com/Grove-Flame_Sensor/)
        * Buzzer
* (Opcional) [Docker](https://docs.docker.com/engine/install/debian/)

> Docker es opcional, debido a que no es necesario para el funcionamiento normal de los sensores y actuadores conectados a la Raspberry Pi. El objetivo de este es mostrar la escalabilidad y adaptabiliad de la [web](https://github.com/Betagmr/iot-server) creada para este proyecto.

## Caracteristicas

### Controlador
El controlador se encarga de la lectura, procesamiento y envío de datos generados por los diferentes sensores, y del control del sistema de riego y alumbrado. 

En cuanto a los sensores y actuadores, en primer lugar, tenemos el sensor de [Temperature&Humidity v1.2](https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/) del cual extraemos los valores ambientales de temperatura y humedad, grados y porcentaje respectivamente,  para posteriormente poder ser visualizados desde la web. A continuación, tenemos el [Light Sensor v1.2](https://seeeddoc.github.io/Grove-Light_Sensor_v1.2/), el cual nos proporciona, en lúmenes, la intensidad de luz en el ambiente. Este valor es procesado antes de su envío y en caso de que èste sea menor al valor estipulado, se encenderá de forma automática el sistema de alumbrado que en nuestro caso es simulado por un [Led Socket v1.5](https://wiki.seeedstudio.com/Grove-LED_Socket_Kit/). Finalmente, el controlador posee un módulo para el control remoto del activado y desactivado del sistema de riego, cuyos movimientos están simulados por un servo analógico.


### Sistema de alarma
El sistema de alarma está compuesto por un detector de llamas ([Flame Sensor v1.1](https://wiki.seeedstudio.com/Grove-Flame_Sensor/)), un buzzer, un sensor RFID ([RFID-RC522](https://pimylifeup.com/raspberry-pi-rfid-rc522/)) y un módulo de envío de emails.

El funcionamiento es el siguiente: si se detectan llamas, el buzzer empieza a sonar indefinidamente y se envía un mensaje de alerta a la web y vía email. Una vez que alguien autorizado desactive la alarma usando el lector RFID, el buzzer dejará de sonar y se notificará tanto en la web, como vía email.


### Docker
Este sistema posee un archivo docker-compose encargado de simular Raspberrys Pi independientes, los cuales envían datos de temperatura, humedad y luminosidad.


> Para más información sobre cómo visualizar los de datos de la Raspberry Pi o de los contenedores, sobre el control del sistema de riego o sobre el sistema de notificaciones web en este [link](https://github.com/Betagmr/iot-server).

## Instalación

### Sensores y actuadores

Previo a la instalación, debemos tener los sensores y actuadores conectados al Grove Hat en los conectores que se especifican a continuación:
* Light Sensor -> D0
* Servo -> PWD
* Temperature&Humidity Sensor -> D18
* Led Socket -> D5
* Flame Sensor -> D22
* Buzzer -> D16
* RFID-RC522 sensor -> conectar como en la imagen de abajo

<img src="https://i.stack.imgur.com/VzdSh.jpg" alt="drawing" width="350"/>

> Si se conecta alguno de los sensores o actuadores a otro puerto deberá ser reflejado en el archivo settings.py correspondiente.

### Raspberry Pi

Descargamos el repositorio:

```
git clone https://github.com/Delapee/iot_rpi.git
```

#### Controlador y sistema de alarma

Una vez descargado el repositorio instalamos las dependecias:
```
pip3 install -r iot_rpi/requirements.txt
```

Configuramos los tres servicios de arranque del sistema.
Nos movemos al la carpeta /etc/systemd/system:
```
cd /etc/systemd/system
```

Creamos el servico para la descarga de la id:
```
nano iot.service
```

```
[Unit]
Description=IoT service
After=network.target

[Service]
ExecStart=/bin/bash id
WorkingDirectory=FILE_FOLDER_PATH
StandardOutput=inherit
StandardError=inherit
Restart=on-failure
User=USER

[Install]
WantedBy=multi-user.target
```

Creamos el servicio para el controlador:
```
nano iot.controller.service
```
```
[Unit]
Description=Controller init service
After=network.target

[Service]
ExecStart=/usr/bin/python3 activate_controller
WorkingDirectory=FILE_FOLDER_PATH
StandardOutput=inherit
StandardError=inherit
Restart=on-failure
User=USER

[Install]
WantedBy=multi-user.target
```

Creamos el servico par el sistema de alarma:
```
nano iot.flame.service 
```
```
[Unit]
Description=Flame trigger init service
After=network.target

[Service]
ExecStart=/usr/bin/python3 activate_flame
WorkingDirectory=FILE_FOLDER_PATH
StandardOutput=inherit
StandardError=inherit
Restart=on-failure
User=USER

[Install]
WantedBy=multi-user.target
```

Finalmente activamos los servicios y reiniciamos para comprobar que se ejecutan al arrancar el sistema:
```
sudo systemctl enable iot.service
sudo systemctl enable iot.controller.service
sudo systemctl enable iot.flame.service

sudo reboot now
```

#### Docker

Nos movemos a la carpeta docker del proyecto:
```
cd iot_rpi/docker
```

Ejecutamos el docker compose:
```
docker compose up -d --scale app=N_SIMULATIONS
```
