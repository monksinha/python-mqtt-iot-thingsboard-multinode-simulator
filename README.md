## Relay + Sensor Multi-Room Simulation (Branch: relay-simulator)

This branch extends the multi-room sensor simulator by adding **relay GUI simulators** that listen to ThingsBoard RPC commands and visually display ON/OFF states.

### Architecture Overview

Each room now has:

* Sensor simulator (Python GUI → sends telemetry)
* Relay simulator (Python GUI → listens to RPC)
* OR real NodeMCU relay (Grow Room)

| Room      | Sensor           | Relay              |
| --------- | ---------------- | ------------------ |
| Grow Room | Python Simulator | NodeMCU (Physical) |
| Dark Room | Python Simulator | Python Relay GUI   |
| Chamber   | Python Simulator | Python Relay GUI   |

---

### Project Structure

```
thingsboard-simulator/
│
├── app.py                     # Sensor simulator
├── relay_gui.py               # Relay listener GUI
│
├── config/
│   ├── grow.json
│   ├── dark.json
│   ├── chamber.json
│   ├── relay_dark.json
│   └── relay_chamber.json
```

---

### Sensor Simulator

Run three terminals:

Grow Room:

```
python app.py config/grow.json
```

Dark Room:

```
python app.py config/dark.json
```

Chamber:

```
python app.py config/chamber.json
```

---

### Relay GUI Simulator

Run two terminals:

Dark Room Relay:

```
python relay_gui.py config/relay_dark.json
```

Chamber Relay:

```
python relay_gui.py config/relay_chamber.json
```

These GUIs **do not send commands**.
They **listen to ThingsBoard RPC** and update color indicators.

---

### RPC Format Expected from ThingsBoard

```
{
  "method": "setState",
  "params": {
    "ac": true
  }
}
```

Mapping performed internally:

| Dashboard key | GUI device |
| ------------- | ---------- |
| ac            | AC         |
| humidifier    | Humidifier |
| cooler        | Cooler     |
| lights        | Light      |
| wallFan       | WallFan    |
| exhaustFan    | Exhaust    |

---

### Full System Simulation

Running components:

* 3 Sensor Simulators
* 2 Relay Simulators
* 1 Physical NodeMCU Relay
* 3 ThingsBoard Dashboards
* Alias-based device mapping

---

### Workflow to Reproduce

1. Start ThingsBoard Docker
2. Run all sensor simulators
3. Run relay GUI simulators
4. Open dashboards
5. Toggle relays → GUI updates
6. Move sliders → telemetry updates

---

### Branch Purpose

This branch introduces:

* Config-driven relay simulator
* MQTT RPC listener
* GUI state visualization
* Multi-room relay simulation

Base branch: `multi-room-simulator`




















# ThingsBoard Multi-Room Sensor Simulator

This project simulates sensor telemetry for multiple rooms in ThingsBoard using a single Python GUI application and separate configuration files.

## Overview

We use:

* One Python simulator (`app.py`)
* Multiple JSON config files
* Each config file represents one device (room)
* The simulator is run multiple times with different configs

This allows running:

* Grow Room simulator
* Dark Room simulator
* Integrated Chamber simulator

---

## Project Structure

```
thingsboard-simulator/
│
├── app.py
├── config/
│   ├── grow.json
│   ├── dark.json
│   └── chamber.json
└── README.md
```

---

## Config File Format

Each config file contains:

```
{
  "device_name": "Grow Room",
  "access_token": "YOUR_DEVICE_TOKEN"
}
```

Fields:

* `device_name` → used for window title
* `access_token` → ThingsBoard device token

---

## How It Works

The simulator reads config file using command line argument:

```
python app.py config/grow.json
```

Internally:

* `sys.argv` reads file path
* JSON is loaded into Python dictionary
* token + device name are applied dynamically

---

## Running Simulators

Open **three terminals** and run:

### Grow Room

```
python app.py config/grow.json
```

### Dark Room

```
python app.py config/dark.json
```

### Integrated Chamber

```
python app.py config/chamber.json
```

You should see three GUI windows.

Each sends telemetry to its respective ThingsBoard device.

---

## Telemetry Sent

Every 5 seconds:

```
{
  "temperature": value,
  "humidity": value,
  "co2": value
}
```

---

## Default Behavior

If no config is passed:

```
python app.py
```

Default config used:

```
config/grow.json
```

---

## Git Workflow Used

Feature branch:

```
multi-room-simulator
```

Steps:

1. Create branch
2. Add config support
3. Run multiple simulators
4. Update README
5. Commit and push

---

## Future Extensions

* Add relay simulator GUI
* Add auto mode simulation
* Add noise/random telemetry
* Add environment profiles

---

















# ThingsBoard Python Sensor Simulator

A lightweight Python GUI simulator to send **Temperature**, **Humidity**, and **CO₂** telemetry to **ThingsBoard** via MQTT.
Useful for testing dashboards, rule chains, and automation logic without real hardware.

---

# Features

* GUI sliders for Temperature, Humidity, CO₂
* Configurable step resolution
* Live value display
* Auto publish (every 5 seconds)
* Manual "Send Now" button
* MQTT integration with ThingsBoard
* Docker support
* Volume mounting for live code updates

---

# Architecture

GUI Simulator → MQTT → ThingsBoard → Dashboard / Rule Engine → NodeMCU

---

# Requirements (Local Run)

* Python 3.9+
* ThingsBoard running (MQTT port 1883)
* pip

Install dependencies:

```bash
pip install paho-mqtt
```

---

# Run Locally (No Docker)

1. Clone repo
2. Edit `app.py` and set:

```python
THINGSBOARD_HOST = "localhost"
ACCESS_TOKEN = "YOUR_DEVICE_TOKEN"
```

3. Run:

```bash
python app.py
```

GUI will open and start sending telemetry.

---

# Telemetry Format

```json
{
  "temperature": 25.5,
  "humidity": 65,
  "co2": 635
}
```

---

# Docker Version

## Build Image

```bash
docker build -t tb-simulator .
```

---

## Run Container

```bash
docker run -e TOKEN=YOUR_DEVICE_TOKEN \
           -e HOST=thingsboard \
           tb-simulator
```

---

# Docker Volume Mount (Live Code Editing)

This allows modifying code without rebuilding image.

```bash
docker run \
-e TOKEN=YOUR_DEVICE_TOKEN \
-e HOST=thingsboard \
-v $(pwd):/app \
tb-simulator
```

Now:

* Edit `app.py`
* Restart container
* Changes applied instantly

No rebuild required.

---

# Docker Networking

If ThingsBoard runs in Docker:

```bash
docker network ls
```

Then run:

```bash
docker run --network <network_name> \
-e TOKEN=YOUR_DEVICE_TOKEN \
-v $(pwd):/app \
tb-simulator
```

---

# Environment Variables

| Variable | Description              | Default   |
| -------- | ------------------------ | --------- |
| TOKEN    | ThingsBoard device token | required  |
| HOST     | MQTT host                | localhost |

---

# Development Workflow

Recommended:

```bash
docker run \
-e TOKEN=... \
-v $(pwd):/app \
tb-simulator
```

Edit → Save → Restart container → Done

---

# Dashboard Keys

Create widgets using:

* temperature
* humidity
* co2

---

# Future Improvements

* Web-based simulator (Flask)
* Multiple device simulation
* Random mode
* Scenario playback
* Grafana integration
* Rule engine automation

---


# License

MIT
