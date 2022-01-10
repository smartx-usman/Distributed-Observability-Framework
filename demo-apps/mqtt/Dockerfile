FROM python:3.8-alpine

ENV SENSORS="1"
ENV MESSAGE_DELAY="1"
ENV MQTT_BROKER="mqtt-mosquitto.uc0.svc.cluster.local"
ENV MQTT_BROKER_PORT="1883"
ENV MQTT_SENSOR_TOPIC="mqtt/temperature-readings"
ENV MQTT_ACTUATOR_TOPIC="mqtt/temperature-actions"
ENV KAFKA_BROKER="bitnami-kafka-0.bitnami-kafka-headless.uc0.svc.cluster.local:9092"
ENV KAFKA_TOPIC="temperature-readings"
ENV START_VALUE="1"
ENV END_VALUE="10"
ENV VALUE_TYPE="integer"
ENV INVALID_VALUE_OCCURRENCE="10"
ENV INVALID_VALUE="99"

ARG Pathdir="/mqtt"

RUN mkdir $Pathdir

COPY actuator/temp-actuator.py $Pathdir
COPY analyzer/temp-analyzer.py $Pathdir
COPY publisher/publisher.py $Pathdir
COPY subscriber/subscriber.py $Pathdir

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR $Pathdir

#ENTRYPOINT ["python3", "actuate.py"]