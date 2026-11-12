"""Deterministic-shape demo data and simulation helpers for Smart Campus IoT."""
from __future__ import annotations

import random
from datetime import datetime, timedelta

CAMPUS_BUILDINGS = ["Academic Block A", "Academic Block B", "Engineering Labs", "Library"]

def create_initial_state() -> dict:
    rooms = []
    for i in range(1, 9):
        occupied = i % 3 != 0
        temp = round(random.uniform(23.0, 29.0), 1)
        lux = random.randint(180, 650)
        devices = {
            "light": occupied and lux < 420,
            "fan": occupied and temp > 25,
            "ac": occupied and temp > 27,
        }
        power = (0.45 if devices["light"] else 0) + (0.65 if devices["fan"] else 0) + (1.8 if devices["ac"] else 0)
        rooms.append({
            "id": f"room-{i:02d}", "name": f"Classroom {100+i}",
            "occupied": occupied, "temperature": temp, "lux": lux,
            "devices": devices, "power_kw": round(power, 2),
            "mode": "Automatic",
        })
    parking = []
    for i in range(1, 21):
        status = "Occupied" if i % 4 == 0 or i % 7 == 0 else "Free"
        parking.append({"id": f"P-{i:02d}", "status": status, "reserved_by": None})
    return {
        "rooms": rooms,
        "parking": parking,
        "current_kw": round(random.uniform(58, 66), 1),
        "baseline_kw": 100.0,
        "access_events": 12,
        "alerts": [
            {"title":"Classroom 103 occupancy changed to vacant","source":"PIR · Classroom 103","severity":"Info","time":"09:42:18","acknowledged":False},
            {"title":"Energy meter heartbeat delayed","source":"Engineering Labs","severity":"Warning","time":"09:38:02","acknowledged":False},
            {"title":"Parking zone A gateway online","source":"Parking Gateway","severity":"Info","time":"09:30:41","acknowledged":True},
        ],
    }

def create_energy_history(points: int = 24):
    import pandas as pd
    now = datetime.now()
    rows = []
    for i in range(points):
        baseline = 100 + random.uniform(-4, 4)
        current = baseline * random.uniform(0.60, 0.78)
        rows.append({
            "time": now - timedelta(minutes=(points-i)*15),
            "consumption": round(current, 1),
            "baseline": round(baseline, 1),
        })
    return pd.DataFrame(rows)

def tick_simulation(state: dict) -> None:
    """Advance the demo by one simulation step."""
    for room in state["rooms"]:
        if random.random() < 0.18:
            room["occupied"] = not room["occupied"]
        room["temperature"] = round(max(19, min(34, room["temperature"] + random.uniform(-0.5, 0.5))), 1)
        room["lux"] = max(80, min(900, room["lux"] + random.randint(-35, 35)))
        if room["mode"].startswith("Auto"):
            if not room["occupied"]:
                room["devices"] = {"light":False,"fan":False,"ac":False}
            else:
                room["devices"]["light"] = room["lux"] < 350
                room["devices"]["fan"] = room["temperature"] > 25
                room["devices"]["ac"] = room["temperature"] > 27
        d = room["devices"]
        room["power_kw"] = round((0.45 if d["light"] else 0)+(0.65 if d["fan"] else 0)+(1.8 if d["ac"] else 0), 2)
    state["current_kw"] = round(random.uniform(58, 75), 1)

def get_energy_summary(state: dict) -> dict:
    baseline = state["baseline_kw"]
    current = state["current_kw"]
    return {
        "saving_pct": max(0, (baseline-current)/baseline*100),
        "saved_kw": max(0, baseline-current),
    }

def get_parking_slots(state: dict) -> list:
    return state["parking"]
