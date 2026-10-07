# PIS Backend

The Backend contains the main application logic for the **Plant Irrigation System (PISS)** and runs on the Raspberry Pi.

It acts as the bridge between the Arduino controller and the web-based GUI.

## Responsibilities

The backend will:

-
-

## Technology - C# .NET
- ASP.NET Core
- SQLite
- Raspberry Pi / Linux

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
