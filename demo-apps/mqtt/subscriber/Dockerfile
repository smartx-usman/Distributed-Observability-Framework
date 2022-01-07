FROM python:alpine3.15

ENV MQTT_BROKER="mqtt-mosquitto.uc0.svc.cluster.local"
ENV MQTT_BROKER_PORT="1883"
ENV KAFKA_BROKER="bitnami-kafka-0.bitnami-kafka-headless.uc0.svc.cluster.local:9092"
ENV KAFKA_TOPIC="temperature"

ARG Pathdir="/mqtt"

RUN mkdir $Pathdir

COPY subscribe.py $Pathdir
COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR $Pathdir

ENTRYPOINT ["python3", "subscribe.py"]