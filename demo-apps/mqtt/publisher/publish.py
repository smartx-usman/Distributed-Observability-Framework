# python 3.6
import logging
import os
import time
from random import randint
from random import seed
from threading import Thread

from paho.mqtt import client as mqtt_client

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

mqtt_broker = os.environ['MQTT_BROKER']
mqtt_topic = os.environ['MQTT_TOPIC']
value_type = os.environ['VALUE_TYPE']
invalid_value_occurrence = int(os.environ['INVALID_VALUE_OCCURRENCE'])
mqtt_port = int(os.environ['MQTT_BROKER_PORT'])

# topic = "mqtt/temperature"
# username = 'emqx'
# password = 'public'

# Cast values from string to integer
if value_type == 'integer':
    start_value = int(os.environ['START_VALUE'])
    end_value = int(os.environ['END_VALUE'])
    invalid_value = int(os.environ['INVALID_VALUE'])


# Connect to MQTT broker
def connect_mqtt(clientID):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.critical("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(clientID)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client


# Generate integer values based on given range of values
def generate_integer_values(msg_count):
    generated_value = randint(start_value, end_value)

    if msg_count == invalid_value_occurrence:
        generated_value = invalid_value

    return generated_value


# Publish message to MQTT topic
def mqtt_publish_message(client_id, delay):
    msg_count = 1
    seed(1)
    client = connect_mqtt(client_id)
    client.loop_start()

    while True:
        time.sleep(delay)
        start_time = time.perf_counter()

        if value_type == 'integer':
            value = generate_integer_values(msg_count)
        else:
            logging.critical(
                f"Failed to create value of type {value_type}. No function is defined for {value_type} value type.")

        time_ms = round(time.time() * 1000)
        msg = f"measurement_timestamp: {time_ms} client_id: {client_id} msg_count: {msg_count} value: {value}"
        result = client.publish(mqtt_topic, msg)
        status = result[0]

        if status == 0:
            logging.info(f"Send `{msg}` to topic `{mqtt_topic}`")
        else:
            logging.error(f"Failed to send message to topic {mqtt_topic}")

        if value == invalid_value:
            msg_count = 1
        else:
            msg_count += 1

        end_time = time.perf_counter()

        logging.info(f'It took {end_time - start_time: 0.4f} second(s) to complete.')


def run():
    try:
        threads = []
        sensor_count = int(os.environ['SENSORS'])
        delay = float(os.environ['MESSAGE_DELAY'])
        logging.info(f'Number of sensors to start {sensor_count} with delay {delay}.')

        for n in range(0, sensor_count):
            t = Thread(target=mqtt_publish_message, args=(f"sensor-{n}", delay,))
            threads.append(t)
            t.start()

        # wait for the threads to complete
        for t in threads:
            t.join()
    except Exception as e:
        logging.error("Unable to start thread", exc_info=True)


if __name__ == '__main__':
    run()
