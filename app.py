from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.simulator import (
    CAMPUS_BUILDINGS, create_energy_history, create_initial_state,
    get_energy_summary, get_parking_slots, tick_simulation,
)

st.set_page_config(
    page_title="Smart Campus IoT",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1500px; }
[data-testid="stSidebar"] { border-right: 1px solid rgba(120,130,150,.18); }
.hero {
  padding: 1.45rem 1.7rem; border-radius: 18px;
  background: linear-gradient(115deg,#101f3c 0%,#173b60 55%,#087e83 100%);
  color: white; margin-bottom: 1.2rem;
}
.hero h1 { font-family: Manrope,sans-serif; font-size: 2rem; margin: 0 0 .35rem 0; color:white; }
.hero p { color:#d7e7f1; margin:0; font-size:.96rem; }
.eyebrow { color:#8de4d2; text-transform:uppercase; letter-spacing:.13em; font-size:.72rem; font-weight:700; }
.metric-card {
  border:1px solid rgba(120,130,150,.22); border-radius:15px;
  padding:1rem 1.1rem; background:rgba(120,130,150,.035); min-height:115px;
}
.metric-label { color:#718096; font-size:.82rem; font-weight:600; }
.metric-value { font-family:Manrope,sans-serif; font-size:1.8rem; font-weight:800; margin:.15rem 0; }
.metric-note { color:#718096; font-size:.76rem; }
.section-title { font-family:Manrope,sans-serif; font-weight:800; font-size:1.12rem; margin:.4rem 0 .8rem; }
.slot {
  border-radius:12px; padding:.85rem .5rem; text-align:center;
  border:1px solid rgba(120,130,150,.22); margin-bottom:.35rem;
}
.slot-free { background:rgba(22,163,74,.10); border-color:rgba(22,163,74,.4); }
.slot-occupied { background:rgba(239,68,68,.10); border-color:rgba(239,68,68,.4); }
.slot-reserved { background:rgba(234,179,8,.13); border-color:rgba(234,179,8,.45); }
.small-muted { color:#718096; font-size:.82rem; }
.stButton>button { border-radius:10px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

if "campus" not in st.session_state:
    st.session_state.campus = create_initial_state()
if "energy_history" not in st.session_state:
    st.session_state.energy_history = create_energy_history()

state = st.session_state.campus

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🏙️ Smart Campus")
    st.caption("AI • IoT • Sustainability")
    page = st.radio(
        "NAVIGATION",
        ["Overview", "Classroom Automation", "Smart Parking", "Energy Analytics", "Safety & Access", "System Settings"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("**Campus environment**")
    campus_name = st.selectbox("Campus", ["Nantong University · Main Campus", "Nantong University · North Campus", "Nantong University · East Campus", "Nantong University · West Campus"])
    st.caption("● Demo simulation active")
    if st.button("↻ Advance simulation", use_container_width=True):
        tick_simulation(state)
        st.session_state.energy_history = pd.concat(
            [st.session_state.energy_history, pd.DataFrame([{
                "time": datetime.now(), "consumption": state["current_kw"],
                "baseline": state["baseline_kw"]
            }])], ignore_index=True
        ).tail(48)
        st.rerun()
    st.caption("Prototype build · v1.0.0")

# ---------- Helpers ----------
def hero(kicker, title, subtitle):
    st.markdown(f'<div class="hero"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def metric(label, value, note="", delta=None):
    with st.container(border=True):
        st.markdown(f'<div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div>', unsafe_allow_html=True)
        if delta:
            st.caption(delta)

def status_badge(text, color="#16a34a"):
    st.markdown(f'<span style="display:inline-block;padding:4px 9px;border-radius:99px;background:{color}18;color:{color};font-size:.75rem;font-weight:700">{text}</span>', unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def make_energy_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["baseline"], name="Estimated baseline", line=dict(color="#94a3b8", dash="dot", width=2)))
    fig.add_trace(go.Scatter(x=df["time"], y=df["consumption"], name="Smart campus", line=dict(color="#0d9488", width=3), fill="tozeroy", fillcolor="rgba(13,148,136,.08)"))
    fig.update_layout(height=300, margin=dict(l=5,r=5,t=20,b=5), legend=dict(orientation="h",y=1.12), yaxis_title="Power (kW)", xaxis_title=None, hovermode="x unified")
    return fig

# ---------- Pages ----------
if page == "Overview":
    hero("CAMPUS INTELLIGENCE PLATFORM", "A smarter, safer & greener campus", f"Live operational snapshot · {campus_name}")
    energy = get_energy_summary(state)
    cols = st.columns(4)
    with cols[0]: metric("LIVE POWER LOAD", f'{state["current_kw"]:.1f} kW', "Across monitored buildings")
    with cols[1]: metric("ENERGY SAVED", f'{energy["saving_pct"]:.1f}%', "Compared with estimated baseline")
    with cols[2]: metric("PARKING AVAILABLE", f'{sum(1 for x in state["parking"] if x["status"]=="Free")}/{len(state["parking"])}', "Live slot availability")
    with cols[3]: metric("ACTIVE ALERTS", str(sum(1 for a in state["alerts"] if not a["acknowledged"])), "Unacknowledged events")
    st.write("")
    left, right = st.columns([1.55, 1])
    with left:
        section("Energy consumption · live trend")
        st.plotly_chart(make_energy_chart(st.session_state.energy_history), use_container_width=True)
    with right:
        section("Campus system health")
        health = [
            ("Classroom sensors", "Online", 96),
            ("Parking gateway", "Online", 100),
            ("Energy meters", "Online", 92),
            ("Safety network", "Online", 98),
        ]
        for name, status, pct in health:
            st.markdown(f"**{name}** <span style='float:right;color:#16a34a;font-size:.8rem'>● {status}</span>", unsafe_allow_html=True)
            st.progress(pct, text=f"{pct}%")
    section("Operational overview")
    c1, c2 = st.columns(2)
    with c1:
        section("Classroom occupancy")
        rooms = state["rooms"]
        room_df = pd.DataFrame([{"Room":r["name"],"Occupancy": "Occupied" if r["occupied"] else "Vacant","Temperature":r["temperature"]} for r in rooms])
        st.dataframe(room_df, hide_index=True, use_container_width=True)
    with c2:
        section("Recent activity")
        for alert in state["alerts"][-4:][::-1]:
            icon = "🟠" if alert["severity"] == "Warning" else "🔵"
            st.markdown(f"{icon} **{alert['title']}**  \n<small class='small-muted'>{alert['time']} · {alert['source']}</small>", unsafe_allow_html=True)
            st.divider()

elif page == "Classroom Automation":
    hero("MODULE 01 · ENERGY AUTOMATION", "Smart classroom control", "Occupancy-aware lighting, HVAC and room-level energy management.")
    rooms = state["rooms"]
    selected = st.selectbox("Select classroom", [r["name"] for r in rooms])
    room = next(r for r in rooms if r["name"] == selected)
    a,b,c,d = st.columns(4)
    with a: metric("OCCUPANCY", "Occupied" if room["occupied"] else "Vacant", "PIR motion sensor")
    with b: metric("TEMPERATURE", f'{room["temperature"]:.1f} °C', "Ambient sensor")
    with c: metric("LIGHT LEVEL", f'{room["lux"]} lux', "LDR sensor")
    with d: metric("ROOM LOAD", f'{room["power_kw"]:.2f} kW', "Smart power meter")
    left,right = st.columns([1.1,1])
    with left:
        section("Appliance controls")
        for key,label in [("light","Lights"),("fan","Fans"),("ac","Air conditioning")]:
            current = room["devices"][key]
            new_value = st.toggle(label, value=current, key=f"{room['id']}_{key}")
            if new_value != current:
                room["devices"][key] = new_value
                room["mode"] = "Manual override"
        st.caption(f"Control mode: **{room['mode']}**")
        if st.button("Apply automatic energy-saving policy", type="primary"):
            if not room["occupied"]:
                room["devices"] = {"light":False,"fan":False,"ac":False}
                room["mode"] = "Auto · vacant room"
                st.success("Room is vacant. All controllable loads switched off.")
            else:
                room["devices"]["light"] = room["lux"] < 350
                room["devices"]["ac"] = room["temperature"] > 27
                room["devices"]["fan"] = room["temperature"] > 25
                room["mode"] = "Auto · comfort policy"
                st.success("Automatic policy applied.")
            st.rerun()
    with right:
        section("Sensor telemetry")
        sensor_df = pd.DataFrame({"Sensor":["PIR motion","Temperature","Light (LDR)","Power meter"],"Reading":["Motion detected" if room["occupied"] else "No motion",f'{room["temperature"]:.1f} °C',f'{room["lux"]} lux',f'{room["power_kw"]:.2f} kW'],"Status":["Online"]*4})
        st.dataframe(sensor_df, hide_index=True, use_container_width=True)
        st.info("Design rule: when no movement is detected for 5 minutes, the automation policy can switch off lights, fans and AC. This demo uses simulated occupancy state.")
    section("All monitored classrooms")
    st.dataframe(pd.DataFrame([{"Room":r["name"],"Occupied":r["occupied"],"Lights":r["devices"]["light"],"Fan":r["devices"]["fan"],"AC":r["devices"]["ac"],"Power (kW)":r["power_kw"]} for r in rooms]), hide_index=True, use_container_width=True)

elif page == "Smart Parking":
    hero("MODULE 02 · MOBILITY", "Smart parking guidance", "Ultrasonic vehicle detection, live slot availability and reservation workflow.")
    slots = get_parking_slots(state)
    free = sum(s["status"]=="Free" for s in slots)
    reserved = sum(s["status"]=="Reserved" for s in slots)
    occupied = sum(s["status"]=="Occupied" for s in slots)
    x1,x2,x3 = st.columns(3)
    with x1: metric("AVAILABLE", str(free), "Ready to use")
    with x2: metric("OCCUPIED", str(occupied), "Vehicle detected")
    with x3: metric("RESERVED", str(reserved), "Held for a user")
    section("Live parking map")
    legend1,legend2,legend3 = st.columns(3)
    with legend1: status_badge("● FREE","#16a34a")
    with legend2: status_badge("● OCCUPIED","#dc2626")
    with legend3: status_badge("● RESERVED","#ca8a04")
    grid = st.columns(5)
    for i, slot in enumerate(slots):
        col = grid[i % 5]
        cls = {"Free":"slot-free","Occupied":"slot-occupied","Reserved":"slot-reserved"}[slot["status"]]
        symbol = {"Free":"✓","Occupied":"●","Reserved":"R"}[slot["status"]]
        with col:
            st.markdown(f'<div class="slot {cls}"><div style="font-weight:800">{slot["id"]}</div><div style="font-size:1.3rem">{symbol}</div><div style="font-size:.75rem">{slot["status"]}</div></div>', unsafe_allow_html=True)
    section("Reserve a parking slot")
    free_slots = [s["id"] for s in slots if s["status"]=="Free"]
    if free_slots:
        p1,p2 = st.columns([2,1])
        with p1:
            chosen = st.selectbox("Choose an available slot", free_slots)
        with p2:
            vehicle = st.text_input("Vehicle / student ID", placeholder="e.g. NTU-2026-001")
        if st.button("Confirm reservation", type="primary"):
            if not vehicle.strip():
                st.error("Enter a vehicle or student ID to continue.")
            else:
                next(s for s in slots if s["id"]==chosen)["status"] = "Reserved"
                next(s for s in slots if s["id"]==chosen)["reserved_by"] = vehicle.strip()
                st.success(f"{chosen} reserved for {vehicle.strip()}.")
                st.rerun()
    else:
        st.warning("No free slots are currently available.")
    with st.expander("Parking system notes"):
        st.write("In a hardware deployment, an ultrasonic sensor at each bay detects vehicle presence. The gateway publishes slot state over MQTT; the mobile client subscribes to availability updates.")

elif page == "Energy Analytics":
    hero("MODULE 03 · SUSTAINABILITY", "Energy intelligence & analytics", "Room-wise power visibility, historical consumption and estimated savings.")
    summary = get_energy_summary(state)
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric("CURRENT LOAD", f'{state["current_kw"]:.1f} kW', "Measured / simulated")
    with c2: metric("BASELINE LOAD", f'{state["baseline_kw"]:.1f} kW', "Estimated unmanaged use")
    with c3: metric("SAVINGS", f'{summary["saving_pct"]:.1f}%', "Against baseline")
    with c4: metric("ENERGY AVOIDED", f'{summary["saved_kw"]:.1f} kW', "Instantaneous difference")
    section("Consumption trend")
    st.plotly_chart(make_energy_chart(st.session_state.energy_history), use_container_width=True)
    section("Building-level consumption")
    building_df = pd.DataFrame([{"Building":b,"Current (kW)":round(random.uniform(8,22),1),"Baseline (kW)":round(random.uniform(18,30),1)} for b in CAMPUS_BUILDINGS])
    building_df["Saving (%)"] = ((building_df["Baseline (kW)"]-building_df["Current (kW)"])/building_df["Baseline (kW)"]*100).round(1)
    st.dataframe(building_df, hide_index=True, use_container_width=True)
    st.download_button("Download energy report (CSV)", building_df.to_csv(index=False).encode("utf-8"), "smart-campus-energy-report.csv", "text/csv")
    st.caption("Savings are illustrative demo estimates, not measured campus performance.")

elif page == "Safety & Access":
    hero("MODULE 04 · CAMPUS PROTECTION", "Safety & access monitoring", "RFID access events, role-aware operations and incident response.")
    alerts = state["alerts"]
    active = [a for a in alerts if not a["acknowledged"]]
    c1,c2,c3 = st.columns(3)
    with c1: metric("ACTIVE EVENTS", str(len(active)), "Requires review")
    with c2: metric("ACCESS EVENTS", str(state["access_events"]), "Simulated RFID activity")
    with c3: metric("SECURITY STATUS", "Protected", "Demo environment")
    section("Access control simulator")
    a,b = st.columns(2)
    with a:
        card_id = st.text_input("RFID card / user ID", placeholder="NTU-STUDENT-1024")
        role = st.selectbox("User role", ["Student","Faculty","Administrator","Visitor"])
        zone = st.selectbox("Access zone", ["Classroom Block A","Laboratory Zone","Server Room","Parking Gate"])
        if st.button("Authenticate access", type="primary"):
            allowed = not (zone=="Server Room" and role not in ["Administrator","Faculty"])
            state["access_events"] += 1
            if allowed:
                st.success(f"Access granted · {role} → {zone}")
                state["alerts"].append({"title":f"Access granted: {card_id or role}","source":zone,"severity":"Info","time":datetime.now().strftime("%H:%M:%S"),"acknowledged":False})
            else:
                st.error("Access denied · insufficient role permissions")
                state["alerts"].append({"title":f"Denied access attempt: {card_id or role}","source":zone,"severity":"Warning","time":datetime.now().strftime("%H:%M:%S"),"acknowledged":False})
    with b:
        section("Security principles")
        st.markdown("- **Authentication:** RFID identity verification\n- **Authorization:** role-based zone permissions\n- **Transport:** secure MQTT/TLS recommended\n- **Data protection:** AES encryption at rest/in transit\n- **Resilience:** gateway monitoring and audit logs")
        st.info("This is a role-based access demonstration. It does not connect to a real door controller or verify a physical RFID credential.")
    section("Event & incident log")
    if alerts:
        for idx, alert in enumerate(alerts[::-1]):
            original_idx = len(alerts)-1-idx
            with st.container(border=True):
                col1,col2,col3 = st.columns([4,1,1])
                with col1:
                    st.markdown(f"**{alert['title']}**")
                    st.caption(f"{alert['time']} · {alert['source']} · {alert['severity']}")
                with col2:
                    status_badge("ACKNOWLEDGED" if alert["acknowledged"] else "OPEN", "#64748b" if alert["acknowledged"] else "#d97706")
                with col3:
                    if not alert["acknowledged"] and st.button("Acknowledge", key=f"ack_{original_idx}"):
                        state["alerts"][original_idx]["acknowledged"] = True
                        st.rerun()

elif page == "System Settings":
    hero("PLATFORM CONFIGURATION", "System settings", "Configure the demo environment and review the reference architecture.")
    section("Deployment profile")
    c1,c2 = st.columns(2)
    with c1:
        st.selectbox("Operating mode", ["Simulation / Demo","Hardware integration (planned)"])
        st.selectbox("Message broker", ["Local MQTT (Mosquitto)","Cloud MQTT broker","Not connected"])
        st.selectbox("Wireless network", ["Wi-Fi + Zigbee (reference design)","Wi-Fi only","Zigbee gateway"])
    with c2:
        st.selectbox("Data storage", ["Local demo state","PostgreSQL (planned)","Cloud time-series DB (planned)"])
        st.selectbox("AI policy", ["Rule-based baseline","Predictive optimization (planned)"])
        st.selectbox("Security profile", ["Role-based demo","Production hardened (planned)"])
    section("Reference architecture")
    st.markdown("""
    ```text
    SENSOR / DEVICE LAYER
    PIR · Temperature · LDR · Smart Meter · Ultrasonic · RFID
                         │
                         ▼
    CONNECTIVITY LAYER
    Wi-Fi / Zigbee · MQTT · Central Campus Gateway
                         │
                         ▼
    PLATFORM / DATA LAYER
    API Service · Time-series Storage · Authentication
                         │
                         ▼
    APPLICATION / INTELLIGENCE LAYER
    Dashboard · Automation Rules · Analytics · Alerts
    ```
    """)
    st.warning("The current repository is a self-contained simulation. MQTT, cloud persistence, production authentication and physical relay control require hardware, credentials and deployment configuration.")
    if st.button("Reset demo data"):
        st.session_state.campus = create_initial_state()
        st.session_state.energy_history = create_energy_history()
        st.success("Demo state reset.")
        st.rerun()

st.divider()
st.caption("Smart Campus IoT · Academic prototype · Demo data is simulated and must not be treated as live campus telemetry.")
