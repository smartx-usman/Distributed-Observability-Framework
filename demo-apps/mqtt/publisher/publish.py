# python 3.6
import os
import time

from random import randint
from random import seed
from threading import Thread
from paho.mqtt import client as mqtt_client

mqtt_broker = os.environ['MQTT_BROKER']
mqtt_port = 1883
topic = "mqtt/temperature"
# username = 'emqx'
# password = 'public'

def connect_mqtt(clientID):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(clientID)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client


def publish(client_id, delay):
    msg_count = 1
    seed(1)
    client = connect_mqtt(client_id)
    client.loop_start()

    while True:
        time.sleep(delay)
        start_time = time.perf_counter()
        value = randint(1, 10)

        if (value % 9) == 0:
            value = 99

        time_ms = round(time.time() * 1000)
        msg = f"measurement_timestamp: {time_ms} client_id: {client_id} msg_count: {msg_count} value: {value}"
        result = client.publish(topic, msg)
        status = result[0]

        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        msg_count += 1
        end_time = time.perf_counter()

        print(f'It took {end_time - start_time: 0.4f} second(s) to complete.')


def run():
    try:
        threads = []
        sensor_count = int(os.environ['SENSORS'])
        delay = float(os.environ['MESSAGE_DELAY'])
        print(f'Number of sensors to start {sensor_count} with delay {delay}.')

        for n in range(0, sensor_count):
            t = Thread(target=publish, args=(f"sensor-{n}", delay, ))
            threads.append(t)
            t.start()

        # wait for the threads to complete
        for t in threads:
            t.join()
    except:
        print("Error: unable to start thread")


if __name__ == '__main__':
    run()
