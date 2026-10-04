# Plant Irrigation System

The Plant Irrigation System is an Arduino and Raspberry Pi-based plant monitoring and automated watering system.

The system is designed to monitor important plant conditions and make plant care easier by providing both automatic and manual watering controls.

## Features

- Monitor soil moisture
- Monitor temperature and humidity
- Monitor water reservoir level
- Display plant statistics on a physical LCD/OLED screen
- Manually activate watering with physical buttons
- Remotely check plant status using the Raspberry Pi
- Remotely activate the water pump
- Automatically water the plant when soil moisture becomes too low
- Prevent the pump from running when the water reservoir is empty
- Log sensor readings and watering events
- Support notifications for watering events and low reservoir levels

## Hardware

- Raspberry Pi
- Arduino-compatible board
- Soil moisture sensor
- DHT11 temperature and humidity sensor
- Water level sensor
- 3-5V mini water pump
- LCD/OLED display
- Push buttons
- Breadboard
- Jumper wires
- Water tubing

## System Overview

The Arduino handles the physical hardware, including sensor readings, buttons, the display, and water pump control.

The Raspberry Pi handles higher-level functions such as remote commands, data logging, notifications, and communication with the Arduino.
