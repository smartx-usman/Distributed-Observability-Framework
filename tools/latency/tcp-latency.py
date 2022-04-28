import logging
import os
import subprocess
from datetime import datetime
from kafka import KafkaProducer
from tcp_latency import measure_latency
from time import sleep

from kubernetes import client, config

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get environment variables for host where pod is running
HOST_IP = os.getenv('HOSTIP')
HOST_NAME = os.getenv('HOSTNAME')

# Start a TCP server in background
subprocess.Popen(["python3", "server.py"])

# Wait for all pods in Stateful set to start
sleep(30)

# Configs can be set in Configuration class directly or using helper utility
config.load_incluster_config()

v1 = client.CoreV1Api()
logging.info("Listing pods with their IPs:")

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='bitnami-kafka-0.bitnami-kafka-headless.monitoring.svc.cluster.local:9092')

while True:
    ret = v1.list_namespaced_pod("measurement")

    for i in ret.items:
        if "tcp-latency-3" == i.metadata.name:
            logging.info(f'Skipping Node: {i.metadata.name}')
        else:
            if "tcp-latency" in i.metadata.name:
                # logging.info(f'Kubernetes Objects [PodIP: {i.status.pod_ip} NodeIP: {i.status.host_ip} Namespace: {i.metadata.namespace} PodName: {i.metadata.name}]')

                host = f'{i.metadata.name}.tcp-latency-svc.measurement.svc.cluster.local'
                # logging.info(f'Service URL: {host}')

                # Getting the current date and time
                dt = datetime.now()

                # getting the timestamp
                measurement_timestamp = datetime.timestamp(dt)

                # print(measure_latency(host=host, port=30099, runs=1))
                tcp_latency = measure_latency(host=host, port=30099, runs=1)

                message = f'measurement_timestamp:{str(measurement_timestamp)},host_ip:{str(HOST_IP)},host_name:{str(HOST_NAME)},target_ip:{str(i.status.host_ip)},target_name:{str(i.spec.node_name)},tcp_latency:{str(tcp_latency[0])}'

                logging.info(message)

                message = message.encode()
                producer.send('tcp-latency', key=b'tcp-latency', value=message)
    # i.metadata.host_ip,
    sleep(120)

# print(measure_latency(host='google.com'))
# print(measure_latency(host='10.98.42.70', port=1883, runs=2))
# print(latency)
