# PIS Controller

The Controller contains the Arduino code responsible for interacting directly with the hardware used by the **Plant Irrigation System (PIS)**.

## Responsibilities

The Arduino controller will:

- Read the soil moisture sensor.
- Monitor the water reservoir level.
- Control the water pump.
- Send sensor readings to the Raspberry Pi.
- Receive commands from the Raspberry Pi, such as turning the water pump on or off.

## Technology

- Arduino
- C/C++
- Arduino IDE

## Communication

The Arduino communicates with the Raspberry Pi through USB serial communication.

Example sensor data sent to the Raspberry Pi:

```text
MOISTURE:42
WATER_LEVEL:75
PUMP:OFF
```

Example commands received from the Raspberry Pi:

```text
PUMP_ON
PUMP_OFF
```

The Raspberry Pi backend is responsible for processing this information and determining when watering should occur.
