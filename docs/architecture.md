# System Architecture

The reference concept is organized as a four-layer IoT foundation.

```mermaid
flowchart TB
  subgraph S["1. Sensing & Device Layer"]
    PIR["PIR motion"] --- TEMP["Temperature"]
    LDR["LDR light"] --- METER["Smart power meter"]
    ULTRA["Ultrasonic parking"] --- RFID["RFID reader"]
    RELAY["Smart relay"]
  end
  subgraph N["2. Network & Communication Layer"]
    WIFI["Wi-Fi"] --- ZIG["Zigbee"]
    MQTT["MQTT broker / campus gateway"]
  end
  subgraph P["3. Platform & Data Layer"]
    API["Application API"]
    DB["Time-series / relational storage"]
    RULES["Automation rules"]
  end
  subgraph A["4. Application & Intelligence Layer"]
    DASH["Admin dashboard"]
    PARK["Parking guidance"]
    ALERT["Alerts & access"]
    ANALYTICS["Energy analytics"]
  end
  S --> N --> P --> A
```

## Data flow

1. Sensors measure occupancy, temperature, ambient light, power, vehicle presence and credential events.
2. Edge gateways normalize device payloads and publish telemetry through MQTT.
3. Platform services validate, timestamp and persist events.
4. Automation rules evaluate occupancy and comfort policies before issuing commands to relays.
5. Dashboard modules expose room status, energy trends, parking occupancy and security events.

## Prototype boundary

The checked-in application simulates telemetry and control state in Streamlit session state. It does not connect to campus infrastructure, physical relays, real RFID readers, a broker or a production database.
