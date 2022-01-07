#!/usr/bin/env python3
import logging
import os
import time

import faust
from paho.mqtt import client as mqtt_client

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

mqtt_broker = os.environ['MQTT_BROKER']
mqtt_port = int(os.environ['MQTT_BROKER_PORT'])
mqtt_topic = os.environ['MQTT_ACTUATOR_TOPIC']
mqtt_client_id = f'mqtt-faust-analyzer'
kafka_broker = 'kafka://' + os.environ['KAFKA_BROKER']
kafka_topic = os.environ['KAFKA_TOPIC']
kafka_key = "server-room"
temperature_file = open("/analyzer/temperature-data.csv", "a")
invalid_data_file = open("/analyzer/temperature-invalid-data.csv", "a")
actuator_id = 'actuator-0'
actuator_actions = ['power-on', 'pause', 'shutdown']


# Connect to MQTT broker
def connect_to_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info('Connected to MQTT Broker!')
        else:
            logging.critical(f'Failed to connect, return code {rc}.')

    try:
        client = mqtt_client.Client(mqtt_client_id)
        client.on_connect = on_connect
        client.connect(mqtt_broker, mqtt_port)
    except Exception as ex:
        logging.critical('Exception while connecting MQTT.', exc_info=True)
    return client


# Publish message to MQTT topic
def mqtt_publish_message(mqtt_publisher, message):
    time_ms = round(time.time() * 1000)
    message = f'processed_ts: {time_ms} {message}'
    result = mqtt_publisher.publish(mqtt_topic, message)
    status = result[0]

    if status == 0:
        logging.info(f"Send `{message}` to topic `{mqtt_topic}`")
    else:
        logging.error(f"Failed to send message to topic {mqtt_topic}")


client = connect_to_mqtt()

# Parse message for MQTT
def parse_message_for_actuator(reading_ts, actuator, action):
    logging.info(f'{action} heating system.')
    message = f"reading_ts: {reading_ts} actuator_id: {actuator} action: {action}"
    mqtt_publish_message(client, message)


# Create a class to parse message from Kafka
class Temperature(faust.Record, serializer='json'):
    reading_ts: int
    sensor: str
    value: int


app = faust.App('temp-analyzer', broker=kafka_broker, )
topic = app.topic(kafka_topic, value_type=Temperature)


# Create worker to process incoming streaming data
@app.agent(topic)
async def check(temperatures):
    async for temperature in temperatures:
        start_time = time.perf_counter()
        logging.info(f'Reading {temperature.value} at ts {temperature.reading_ts} from {temperature.sensor}')

        if int(temperature.value) == 99:
            logging.info('Anomalous value found. Discarded and recorded in file.')
            invalid_data_file.write(temperature.reading_ts + "," + temperature.sensor + "," + temperature.value + "\n")
        else:
            temperature_file.write(temperature.reading_ts + "," + temperature.sensor + "," + temperature.value + "\n")
            if int(temperature.value) < 3:
                parse_message_for_actuator(temperature.reading_ts, actuator_id, actuator_actions[0])
            elif int(temperature.value) > 8:
                parse_message_for_actuator(temperature.reading_ts, actuator_id, actuator_actions[2])
            else:
                logging.info('No action required.')

        end_time = time.perf_counter()
        time_ms = (end_time - start_time) * 1000
        logging.info(f'It took {time_ms} ms to process the message.')


if __name__ == '__main__':
    app.main()
