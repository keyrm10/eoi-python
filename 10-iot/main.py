import network
import utime
import ujson as json
from credenciales import ssid, password
from machine import Pin, unique_id
from ubinascii import hexlify
from umqtt.simple import MQTTClient

import settings


led = Pin(2, Pin.OUT)


def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        print("\nConnecting to WLAN...", end="")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Network config:", wlan.ifconfig())


def mqtt_callback(topic, msg):
    msg = json.loads(msg)
    topic = topic.decode()
    if topic == TOPIC:
        if msg.get("id") == ID and msg.get("value") == 1:
            led.value(0)
            print("Encendiendo LED")
        if msg.get("id") == ID and msg.get("value") == 0:
            led.value(1)
            print("Apagando LED")
        else:
            pass
    print("Me llego por '{}' el siguiente mensaje: {}".format(topic, msg))


wifi_connect()

id_cliente = hexlify(unique_id())
client = MQTTClient(id_cliente, MQTT_SERVER)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(b"proyectoEOI")


while True:
    client.check_msg()
