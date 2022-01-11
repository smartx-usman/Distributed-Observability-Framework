# python3.6
import logging
import os
import time

from paho.mqtt import client as mqtt_client

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

mqtt_broker = os.environ['MQTT_BROKER']
mqtt_port = int(os.environ['MQTT_BROKER_PORT'])
mqtt_topic = os.environ['MQTT_ACTUATOR_TOPIC']
clientID = f'python-mqtt-actuator'


# Connect to MQTT broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info('Connected to MQTT Broker!')
        else:
            logging.critical(f'Failed to connect, return code {rc}.')

    try:
        client = mqtt_client.Client(clientID)
        client.on_connect = on_connect
        client.connect(mqtt_broker, mqtt_port)
    except Exception as ex:
        logging.critical('Exception while connecting MQTT.', exc_info=True)
    return client


# Subscribe messages from MQTT topic
def mqtt_subscribe_message(client: mqtt_client):
    def on_message(client, userdata, msg):
        time_ms = round(time.time() * 1000)
        logging.debug(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        logging.info(f'Current_ts:{time_ms} {message}')
        split_message = message.split()
        total_delay = (time_ms - int((split_message[1].split(':'))[1]))

        logging.info(f'{split_message[3]} is going to be processed by {split_message[2]}')
        logging.info(f'Total delay (reading_ts - current_time): {total_delay}ms')

    client.subscribe(mqtt_topic)
    client.on_message = on_message


def run():
    mqtt_subscriber = connect_mqtt()
    mqtt_subscribe_message(mqtt_subscriber)
    mqtt_subscriber.loop_forever()


if __name__ == '__main__':
    run()
