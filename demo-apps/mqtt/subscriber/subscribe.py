# python3.6
import os
import random
import json

from kafka import KafkaProducer
from paho.mqtt import client as mqtt_client

mqtt_broker = os.environ['MQTT_BROKER']
kafka_broker = os.environ['KAFKA_BROKER']
mqtt_port = 1883
mqtt_topic = "mqtt/temperature"
kafka_topic = "temperature"
kafka_key = "server-room"
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

    try:
        client = mqtt_client.Client(client_id)
        #client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(mqtt_broker, mqtt_port)
    except Exception as ex:
        print('Exception while connecting MQTT')
        print(ex)
    return client

def connect_kafka_producer(kafka_broker):
    _producer = None
    try:
      _producer = KafkaProducer(bootstrap_servers=kafka_broker)
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(ex)
    return _producer

def kafka_publish_message(producer_instance, message):
    try:
        key_bytes = bytes(kafka_key, encoding='utf-8')
        split_message = message.split();
        json_message = {
            'reading_ts': split_message[1],
            'sensor': split_message[3],
            'value': split_message[7]
        }

        message_dump = json.dumps(json_message)
        value_bytes = bytes(message_dump, encoding='utf-8')
        producer_instance.send(kafka_topic, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(ex)

def mqtt_subscribe_message(client: mqtt_client, producer):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        #message = message.encode()
        kafka_publish_message(producer, message)
        #producer.send('temperature', value=message)

    client.subscribe(mqtt_topic)
    client.on_message = on_message


def run():
    mqtt_subscriber = connect_mqtt()
    kafka_producer = connect_kafka_producer(kafka_broker)
    mqtt_subscribe_message(mqtt_subscriber, kafka_producer)
    mqtt_subscriber.loop_forever()


if __name__ == '__main__':
    run()
