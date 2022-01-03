# python 3.6

import time
from random import randint
from random import seed
#from random import random
from threading import Thread

from paho.mqtt import client as mqtt_client

broker = '10.244.2.119'
port = 1883
topic = "python/mqtt"
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
    client.connect(broker, port)
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

        print(f'It took {end_time - start_time: 0.3f} second(s) to complete.')

def run():
    try:
        # create and start number of threads
        threads = []
        for n in range(1, 3):
            t = Thread(target=publish, args=(f"sensor-{n}", 1,))
            threads.append(t)
            t.start()

        # wait for the threads to complete
        for t in threads:
            t.join()

    except:
        print("Error: unable to start thread")

if __name__ == '__main__':
    run()
