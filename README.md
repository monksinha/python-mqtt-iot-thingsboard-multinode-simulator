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
