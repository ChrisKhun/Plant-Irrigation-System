# PIS Backend

The Backend contains the main application logic for the **Plant Irrigation Support System (PISS)** and runs on the Raspberry Pi.

It acts as the bridge between the Arduino controller and the web-based GUI.

## Responsibilities

The backend will:

- Communicate with the Arduino over USB serial.
- Receive soil moisture and water-level readings.
- Send pump commands to the Arduino.
- Handle automatic watering logic.
- Store sensor readings and watering history.
- Manage user-configurable settings.
- Provide a REST API for the GUI.

## Technology

- C#
- .NET
- ASP.NET Core
- SQLite
- Raspberry Pi / Linux
- Serial communication

## API

The backend will provide REST API endpoints that allow the GUI to retrieve information and control the irrigation system.

Planned endpoints include:

```text
GET  /api/status
GET  /api/history
GET  /api/settings

POST /api/water

PUT  /api/settings
```

For example, `GET /api/status` may return:

```json
{
    "moisture": 42,
    "waterLevel": 75,
    "pumpOn": false
}
```

The API allows the GUI to interact with the irrigation system without communicating directly with the Arduino.
