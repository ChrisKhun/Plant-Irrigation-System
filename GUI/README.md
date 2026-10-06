# PISS GUI

The GUI provides a web-based dashboard for monitoring and controlling the **Plant Irrigation Support System (PISS)**.

The dashboard will be accessible from devices such as phones, laptops, and desktop computers through a web browser.

## Responsibilities

The GUI will allow users to:

- View the current soil moisture level.
- View the water reservoir level.
- Check whether the water pump is running.
- Manually water the plant.
- Enable or disable automatic watering.
- Configure the soil moisture threshold.
- View previous watering activity and sensor readings.

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
Pump:          OFF

[ WATER NOW ]

Automatic Watering: ON
Moisture Threshold: 30%
```

Additional monitoring and configuration features may be added as the project develops.
