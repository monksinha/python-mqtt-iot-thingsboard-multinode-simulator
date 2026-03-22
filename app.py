import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import json
import time
import threading

THINGSBOARD_HOST = "localhost"
ACCESS_TOKEN = "i97AxAaOvM138vkJ5TL9"

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)


def get_temperature():
    return round(temp_slider.get() * 2) / 2


def get_humidity():
    return round(humidity_slider.get())


def get_co2():
    return round(co2_slider.get() / 5) * 5


def publish_data():
    data = {
        "temperature": get_temperature(),
        "humidity": get_humidity(),
        "co2": get_co2()
    }

    client.publish("v1/devices/me/telemetry", json.dumps(data))
    print("Sent:", data)


def auto_publish():
    while True:
        publish_data()
        time.sleep(5)


def update_temp(val):
    temp_value.config(text=f"{get_temperature():.1f} °C")


def update_humidity(val):
    humidity_value.config(text=f"{int(get_humidity())} %")


def update_co2(val):
    co2_value.config(text=f"{int(get_co2())} ppm")


root = tk.Tk()
root.title("IoT Sensor Simulator")
root.geometry("400x350")


ttk.Label(root, text="Temperature").pack()

temp_slider = ttk.Scale(
    root,
    from_=10,
    to=40,
    orient="horizontal",
    command=update_temp
)
temp_slider.pack(fill="x")

temp_value = ttk.Label(root, text="")
temp_value.pack()


ttk.Label(root, text="Humidity").pack()

humidity_slider = ttk.Scale(
    root,
    from_=20,
    to=100,
    orient="horizontal",
    command=update_humidity
)
humidity_slider.pack(fill="x")

humidity_value = ttk.Label(root, text="")
humidity_value.pack()


ttk.Label(root, text="CO2").pack()

co2_slider = ttk.Scale(
    root,
    from_=300,
    to=2000,
    orient="horizontal",
    command=update_co2
)
co2_slider.pack(fill="x")

co2_value = ttk.Label(root, text="")
co2_value.pack()


temp_slider.set(25)
humidity_slider.set(60)
co2_slider.set(700)

update_temp(None)
update_humidity(None)
update_co2(None)


send_btn = ttk.Button(root, text="Send Now", command=publish_data)
send_btn.pack(pady=10)


threading.Thread(target=auto_publish, daemon=True).start()

root.mainloop()