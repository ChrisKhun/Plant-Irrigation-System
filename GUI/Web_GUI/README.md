# PIS GUI (WEB-BASED)

The GUI provides a web-based dashboard for monitoring and controlling the **Plant Irrigation System (PIS)**.

The dashboard will be accessible from devices such as phones, laptops, and desktop computers through a web browser.

## Responsibilities

The GUI will allow users to:

- Monitor soil moisture
- Monitor temperature and humidity
- Monitor and set water reservoir level
- Display plant statistics on a physical LCD/OLED screen
- Manually activate watering with physical buttons
- Remotely check plant status using the Raspberry Pi
- Remotely activate the water pump
- Notification system to notify user on any actions or updates
- Automatically water the plant when soil moisture becomes too low
- Prevent the pump from running when the water reservoir is empty
- Log sensor readings and watering events
- Support notifications for watering events and low reservoir levels

## Technology

- React
- TypeScript
- HTML
- CSS

## Backend Communication

The GUI communicates with the C# backend through its REST API.

For example:

```text
GET /api/status
```

can retrieve the current system status, while:

```text
POST /api/water
```

can request that the plant be watered.

## Planned Dashboard

The initial dashboard will display:
```text
PISS
Plant Irrigation Support System

Soil Moisture: 42%
Water Level:   75%
Temperature:   75F (or celcius)
Pump:          OFF

Settings:
Notification Settings - Adjust how often to get status updates or to opt in, adjust water level notification.
Pump Settings - Adjust amount of water pumped or length of time
Accessibility Settings - Theme Change, Language, 

```

Additional monitoring and configuration features may be added as the project develops.
