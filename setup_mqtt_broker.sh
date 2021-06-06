#!/bin/bash

docker run -d -p 1883:1883 --name wii-broker -v /home/pi/Desktop/Mounts/MQTT/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /home/pi/Desktop/Mounts/MQTT/log:/mosquitto/log eclipse-mosquitto:2.0.10