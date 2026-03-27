import tkinter as tk
import paho.mqtt.client as mqtt
import json

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
import sys
import json

# ------------------------------------
# READ CONFIG FILE
# ------------------------------------

try:
    config_file = sys.argv[1]
except Exception:
    config_file = "config/relay_dark.json"

print("Using config:", config_file)

try:
    with open(config_file) as f:
        config = json.load(f)
except Exception as e:
    print("Error reading config:", e)
    exit(1)

THINGSBOARD_HOST = config.get("host", "localhost")
ACCESS_TOKEN = config.get("access_token")
DEVICE_NAME = config.get("device_name", "Relay Simulator")

# -------------------------------------------------
# DEVICE LIST (these must match dashboard RPC names)
# -------------------------------------------------

devices = [
    "AC",
    "Humidifier",
    "Cooler",
    "Light",
    "WallFan",
    "Exhaust"
]


# -------------------------------------------------
# STATE STORAGE
# dictionary to remember ON/OFF status
# -------------------------------------------------

states = {}

for device in devices:
    states[device] = False


# -------------------------------------------------
# GUI LABEL STORAGE
# we store references to GUI boxes so we can update them later
# -------------------------------------------------

device_labels = {}


# -------------------------------------------------
# FUNCTION: UPDATE GUI
# -------------------------------------------------

def update_gui(device_name):

    label = device_labels[device_name]

    if states[device_name] == True:
        label.config(bg="green", text="ON")
    else:
        label.config(bg="red", text="OFF")


# -------------------------------------------------
# MQTT CALLBACK: WHEN MESSAGE ARRIVES
# -------------------------------------------------

def on_message(client, userdata, msg):

    print("Message received from ThingsBoard:")
    print(msg.payload)

    data = json.loads(msg.payload)

    method = data.get("method")
    params = data.get("params")

    # We only care about setState commands
    if method == "setState":

        # params is a dictionary like {"ac": True}
        for key in params:

            value = params[key]

            # Convert dashboard key to GUI key
            # because dashboard uses lowercase
            normalized_key = None

            if key == "ac":
                normalized_key = "AC"
            elif key == "humidifier":
                normalized_key = "Humidifier"
            elif key == "cooler":
                normalized_key = "Cooler"
            elif key == "lights":
                normalized_key = "Light"
            elif key == "wallFan":
                normalized_key = "WallFan"
            elif key == "exhaustFan":
                normalized_key = "Exhaust"

            if normalized_key in states:

                states[normalized_key] = value

                update_gui(normalized_key)

# -------------------------------------------------
# MQTT SETUP
# -------------------------------------------------

client = mqtt.Client()

client.username_pw_set(ACCESS_TOKEN)

client.on_message = on_message

client.connect(THINGSBOARD_HOST, 1883, 60)

# Subscribe to RPC commands from ThingsBoard
client.subscribe("v1/devices/me/rpc/request/+")

# Start MQTT loop in background
client.loop_start()


# -------------------------------------------------
# GUI SETUP
# -------------------------------------------------

root = tk.Tk()

root.title(f"{DEVICE_NAME} Status Viewer")

root.geometry("400x400")

frame = tk.Frame(root)

frame.pack(pady=20)


# -------------------------------------------------
# CREATE GRID OF RELAY BOXES
# -------------------------------------------------

row = 0
col = 0

for device in devices:

    # Create colored status box
    label = tk.Label(
        frame,
        text="OFF",
        bg="red",
        width=12,
        height=4
    )

    label.grid(
        row=row,
        column=col,
        padx=10,
        pady=10
    )

    # Save label reference
    device_labels[device] = label

    # Device name below box
    name_label = tk.Label(frame, text=device)

    name_label.grid(
        row=row + 1,
        column=col
    )

    # move to next column
    col = col + 1

    # after 2 columns move to next row
    if col == 2:
        col = 0
        row = row + 2


# -------------------------------------------------
# START GUI
# -------------------------------------------------

root.mainloop()