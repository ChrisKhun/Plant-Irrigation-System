# PIS GUI

The GUI provides a web-based dashboard for monitoring and controlling the **Plant Irrigation System (PIS)**.

The dashboard will be accessible from devices such as phones, laptops, and desktop computers through a web browser.

## Responsibilities

The GUI will allow users to:

-
-


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
