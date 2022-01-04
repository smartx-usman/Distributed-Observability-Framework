# python3.6
import os
import random

from kafka import KafkaProducer
from paho.mqtt import client as mqtt_client

# Change broker IP
#broker = '10.244.2.119'
mqtt_broker = os.environ['MQTT_BROKER']
kafka_broker = os.environ['KAFKA_BROKER']
mqtt_port = 1883
topic = "mqtt/temperature"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client

def connect_kafka(kafka_broker):
    producer = KafkaProducer(bootstrap_servers=kafka_broker)
    return producer;

def subscribe(client: mqtt_client, producer):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        message = message.encode()
        producer.send('temperature', value=message)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    producer = connect_kafka(kafka_broker)
    subscribe(client, producer)
    client.loop_forever()


if __name__ == '__main__':
    run()
