# Hardware Integration Guide

This repository is currently a software simulation. The following is an integration plan, not a claim that hardware connectivity is already implemented.

## Reference devices from the project brief

| Device | Purpose | Suggested event |
|---|---|---|
| PIR motion sensor | Room occupancy | `campus/rooms/{room_id}/occupancy` |
| Temperature sensor | Ambient temperature | `campus/rooms/{room_id}/temperature` |
| LDR | Ambient light level | `campus/rooms/{room_id}/lux` |
| Smart power meter | kWh / instantaneous load | `campus/rooms/{room_id}/power` |
| Smart relay | Switch controlled loads | `campus/rooms/{room_id}/command` |
| Ultrasonic sensor | Vehicle presence | `campus/parking/{slot_id}/occupancy` |
| RFID reader | Identity event | `campus/access/events` |

## MQTT topic convention

Use a campus-scoped namespace and version payloads. Example telemetry:

```json
{
  "schema_version": 1,
  "device_id": "pir-room-101",
  "campus_id": "ntu-main",
  "room_id": "room-01",
  "occupied": true,
  "timestamp": "2026-11-13T08:00:00Z"
}
```

Example relay command:

```json
{
  "schema_version": 1,
  "command_id": "cmd-unique-id",
  "device_id": "relay-room-101",
  "target": "light",
  "state": "off",
  "requested_by": "automation-service"
}
```

## Recommended production steps

1. Select certified sensor and relay hardware suitable for the local electrical code.
2. Put relay control behind a gateway; never expose relay devices directly to the public internet.
3. Use MQTT over TLS, unique device credentials, topic ACLs and credential rotation.
4. Add a persistent database, audit trail, retry policy and device health monitoring.
5. Require human approval for safety-critical actions and provide a physical override.
6. Validate the five-minute no-motion policy against occupancy edge cases before enabling it.
7. Conduct a security review and electrical safety inspection before any real deployment.

## Important safety note

Do not connect mains-powered lighting, fans or HVAC to an unqualified DIY relay installation. Use appropriately rated, certified equipment and a qualified electrician.
