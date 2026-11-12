# 🏙️ Smart Campus IoT — AI-Powered Campus Intelligence Platform

> A professional academic prototype for intelligent classroom automation, campus energy analytics, smart parking and safety/access monitoring.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Academic%20Prototype-teal)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

Smart Campus IoT demonstrates how an educational campus can use connected sensors, a central gateway and an intelligent dashboard to improve operational visibility, reduce avoidable energy use and simplify parking management.

The concept is based on the **Smart Campus IoT System** project presentation for Nantong University. The presentation describes four campus locations, 1,500+ active classrooms and more than 40,000 students as project context. Those figures are presentation-provided context, not live data connected to this software.

This repository delivers a working **simulation-first dashboard**. You can explore the workflows without purchasing sensors or configuring a cloud service. Hardware and cloud integrations are documented as future deployment work.

## Features

### 1. Smart Classroom Automation
- Room-level occupancy state based on simulated PIR readings.
- Temperature and ambient-light telemetry.
- Individual light, fan and AC controls.
- Automatic energy-saving policy: when a room is vacant, controllable loads are switched off in the demo.
- Room-wise device and power overview.

### 2. Smart Parking
- Interactive 20-slot parking map.
- Free, occupied and reserved states.
- Reservation flow with a vehicle/student identifier.
- MQTT integration topic plan documented for future hardware.

### 3. Energy Analytics
- Live-style current load and estimated baseline comparison.
- Historical consumption trend chart.
- Building-level illustrative comparison.
- CSV export for the displayed building report.

### 4. Safety & Access
- RFID-style access event simulator.
- Role-based access demonstration for restricted zones.
- Event log and acknowledgement workflow.
- Security principles and production-hardening guidance.

### 5. Platform & Configuration
- Campus selector and simulation controls.
- Four-layer reference architecture.
- Planned deployment settings and integration notes.

## Application preview

The app contains a responsive Streamlit interface with:
- Dark blue/teal dashboard hero panels
- KPI cards and telemetry tables
- Plotly energy trend visualizations
- Parking status grid
- Interactive controls and event workflows

## Technology stack

| Layer | Technology |
|---|---|
| Application | Python 3.11+ |
| UI | Streamlit |
| Data processing | Pandas |
| Charts | Plotly |
| Testing | Pytest |
| Packaging | Docker / Docker Compose |
| Planned IoT transport | MQTT over TLS |
| Reference connectivity | Wi-Fi + Zigbee |
| Planned persistence | PostgreSQL / time-series database |

## Project structure

```text
smart-campus-iot/
├── app.py                      # Streamlit application and page routing
├── src/
│   ├── __init__.py
│   └── simulator.py             # Demo telemetry and simulation logic
├── tests/
│   └── test_simulator.py        # Unit tests
├── docs/
│   ├── architecture.md          # Four-layer architecture and data flow
│   └── hardware-integration.md  # MQTT topics, payloads and deployment plan
├── .streamlit/
│   └── config.toml              # Dashboard theme and server settings
├── .env.example                 # Optional integration environment variables
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
└── requirements.txt
```

## Quick start

### Requirements
- Python 3.11 or newer
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-campus-iot.git
cd smart-campus-iot
```

### 2. Create and activate a virtual environment

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (normally `http://localhost:8501`).

## Run with Docker

```bash
docker compose up --build
```

Open `http://localhost:8501`.

To stop:

```bash
docker compose down
```

## Run tests

```bash
pytest -q
```

## How to use the dashboard

1. Open **Overview** to inspect campus KPIs, energy trend and recent activity.
2. Open **Classroom Automation**, select a room and toggle appliances or apply the automatic policy.
3. Open **Smart Parking** and reserve a free slot with a vehicle/student ID.
4. Open **Energy Analytics** to review the simulated trend and download a CSV report.
5. Open **Safety & Access** to test role-based access and acknowledge events.
6. Open **System Settings** to review the reference architecture and reset the demo state.

Use **Advance simulation** in the sidebar to generate another telemetry step.

## Automation logic in this prototype

The reference presentation describes a scenario where a PIR sensor detects no movement for five minutes and the system switches off lights, fans and AC.

This application demonstrates the resulting vacant-room control behavior using a simulated occupancy state. It does **not** currently implement a real five-minute sensor timer or physical relay command. A production controller must validate sensor freshness, debounce events, support manual override and use safe HVAC shutdown rules.

## Architecture

The project follows a four-layer reference model:

1. **Sensing:** PIR, temperature, LDR, smart power meter, ultrasonic sensor, RFID and relays.
2. **Connecting:** Wi-Fi, Zigbee and a central gateway; MQTT is the planned messaging protocol.
3. **Platform:** API, authentication, data storage and automation rules.
4. **Application:** admin dashboard, energy analytics, parking guidance and safety alerts.

See [`docs/architecture.md`](docs/architecture.md) and [`docs/hardware-integration.md`](docs/hardware-integration.md).

## Important: demo data and project claims

- All readings, parking states, alerts and energy comparisons in the current app are simulated.
- No real campus, student, vehicle, RFID or sensor data is collected.
- The presentation mentions 35% average classroom energy loss, 55% estimated annual electricity savings and an 18-month payback claim. These are **claims in the source presentation**, not measured or independently validated by this software.
- The dashboard's current energy-saving percentage is generated from illustrative demo values and should not be presented as a verified result.
- This repository does not yet include trained AI models, a live MQTT client, production login, cloud storage or physical device drivers.

## Roadmap

- [ ] MQTT subscriber/publisher service with TLS and topic ACLs
- [ ] Persistent database and historical telemetry API
- [ ] Device registry and gateway health monitoring
- [ ] Real sensor adapters for PIR, temperature, LDR and ultrasonic modules
- [ ] Relay command service with audit log and physical override
- [ ] Production authentication and role-based authorization
- [ ] Mobile-friendly parking client and route guidance
- [ ] Forecasting model evaluated on real, consented campus data
- [ ] Deployment monitoring, backups and security testing

## Security and safety

This project is an academic demonstration, not a production building-management or life-safety system. Do not connect real electrical loads or control access hardware using this prototype. A real deployment requires qualified electrical installation, certified devices, secure credential management, network segmentation, audit logging, fail-safe behavior and institutional approval.

## Contributing

Pull requests are welcome for bug fixes, accessibility improvements, tests and clearly scoped integrations.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Add or update tests.
4. Run `pytest -q`.
5. Open a pull request describing the change and any hardware assumptions.

## License

Released under the MIT License. See [`LICENSE`](LICENSE).

## Acknowledgement

Concept and project framing adapted from the **Smart Campus IoT System** presentation prepared for the Internet of Things Final Presentation 2026, Nantong University.
