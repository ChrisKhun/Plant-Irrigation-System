# PIS GUI (SCREEN)

The GUI provides a touchscreen dashboard for monitoring and controlling the **Plant Irrigation System (PIS)**.

The dashboard will be accessible from devices such as phones, laptops, and desktop computers through a web browser.

## Responsibilities

The GUI will allow users to:

- Allow users to check status of plant (temp, humidity, moisture)
- Water configuration & watering
- Water reservoir level setting & alert

## Technology

- Python
- Tkinter

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
