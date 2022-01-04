FROM python:latest

ENV MQTT_BROKER="10.244.2.119"
ENV KAFKA_BROKER="bitnami-kafka-0.bitnami-kafka-headless.uc0.svc.cluster.local:9092"

ARG Pathdir="/mqtt"

RUN mkdir $Pathdir
RUN pip3 install paho-mqtt
RUN pip3 install kafka-python

COPY subscribe.py $Pathdir

WORKDIR $Pathdir

ENTRYPOINT ["python3", "subscribe.py"]