import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import json
import threading
import time

# -------------------------------------------------
# CONFIG FILES
# -------------------------------------------------

relay_configs = {
    "Grow Room": "config/relay_grow.json",
    "Dark Room": "config/relay_dark.json",
    "Chamber": "config/relay_chamber.json"
}

sensor_configs = {
    "Grow Room": "config/grow.json",
    "Dark Room": "config/dark.json",
    "Chamber": "config/chamber.json"
}

# -------------------------------------------------
# STATE STORAGE
# -------------------------------------------------

relay_labels = {}
sensor_widgets = {}
mqtt_clients = {}

relay_keys = [
    "ac",
    "humidifier",
    "cooler",
    "lights",
    "wallFan",
    "exhaustFan"
]

# -------------------------------------------------
# LOAD CONFIG
# -------------------------------------------------

def load_config(path):
    with open(path) as f:
        return json.load(f)

# -------------------------------------------------
# MQTT RELAY SUBSCRIBER
# -------------------------------------------------

def create_relay_client(room):

    config = load_config(relay_configs[room])

    token = config["access_token"]
    host = config.get("host", "localhost")

    client = mqtt.Client()
    client.username_pw_set(token)

    def on_message(client, userdata, msg):

        data = json.loads(msg.payload)

        if data.get("method") == "setState":

            params = data.get("params")

            for key in params:
                value = params[key]

                label = relay_labels[room][key]

                if value:
                    label.config(bg="green")
                else:
                    label.config(bg="red")

    client.on_message = on_message

    client.connect(host, 1883, 60)
    client.subscribe("v1/devices/me/rpc/request/+")
    client.loop_start()

# -------------------------------------------------
# MQTT SENSOR PUBLISHER
# -------------------------------------------------

def create_sensor_client(room):

    config = load_config(sensor_configs[room])

    token = config["access_token"]
    host = config.get("host", "localhost")

    client = mqtt.Client()
    client.username_pw_set(token)
    client.connect(host, 1883, 60)

    mqtt_clients[room] = client

# -------------------------------------------------
# PUBLISH SENSOR DATA
# -------------------------------------------------

def publish_sensor(room):

    widgets = sensor_widgets[room]

    temp = round(widgets["temp"].get() * 2) / 2
    hum = round(widgets["hum"].get())
    co2 = round(widgets["co2"].get() / 5) * 5

    data = {
        "temperature": temp,
        "humidity": hum,
        "co2": co2
    }

    mqtt_clients[room].publish(
        "v1/devices/me/telemetry",
        json.dumps(data)
    )

    print(room, "Sent:", data)

# -------------------------------------------------
# AUTO PUBLISH THREAD
# -------------------------------------------------

def auto_publish(room):

    while True:
        publish_sensor(room)
        time.sleep(5)

# -------------------------------------------------
# GUI
# -------------------------------------------------

root = tk.Tk()
root.title("Integrated Farm Control")
root.geometry("1100x700")

rooms = ["Grow Room", "Dark Room", "Chamber"]

# headers
tk.Label(root, text="RELAYS", font=("Arial", 16, "bold")).grid(row=0,column=0)
tk.Label(root, text="SENSORS", font=("Arial", 16, "bold")).grid(row=0,column=1)

# -------------------------------------------------
# CREATE LAYOUT
# -------------------------------------------------

for i, room in enumerate(rooms):

    # ---------- RELAY FRAME ----------
    relay_frame = tk.LabelFrame(
        root,
        text=f"{room} Relay",
        width=500,
        height=200
    )

    relay_frame.grid(row=i+1, column=0, padx=10, pady=10)
    relay_frame.grid_propagate(False)

    relay_labels[room] = {}

    for j, key in enumerate(relay_keys):

        label = tk.Label(
            relay_frame,
            text=key,
            bg="red",
            width=12,
            height=2
        )

        label.grid(row=j//3, column=j%3, padx=5, pady=5)

        relay_labels[room][key] = label


    # ---------- SENSOR FRAME ----------
    sensor_frame = tk.LabelFrame(
        root,
        text=f"{room} Sensor",
        width=500,
        height=200
    )

    sensor_frame.grid(row=i+1, column=1, padx=10, pady=10)
    sensor_frame.grid_propagate(False)

    ttk.Label(sensor_frame, text="Temperature").pack()
    temp = ttk.Scale(sensor_frame, from_=10, to=40, orient="horizontal")
    temp.pack(fill="x")

    ttk.Label(sensor_frame, text="Humidity").pack()
    hum = ttk.Scale(sensor_frame, from_=20, to=100, orient="horizontal")
    hum.pack(fill="x")

    ttk.Label(sensor_frame, text="CO2").pack()
    co2 = ttk.Scale(sensor_frame, from_=300, to=2000, orient="horizontal")
    co2.pack(fill="x")

    send_btn = ttk.Button(
        sensor_frame,
        text="Send",
        command=lambda r=room: publish_sensor(r)
    )
    send_btn.pack(pady=5)

    sensor_widgets[room] = {
        "temp": temp,
        "hum": hum,
        "co2": co2
    }

# -------------------------------------------------
# START MQTT
# -------------------------------------------------

for room in rooms:
    create_relay_client(room)
    create_sensor_client(room)

# auto publish threads
for room in rooms:
    threading.Thread(
        target=auto_publish,
        args=(room,),
        daemon=True
    ).start()

root.mainloop()