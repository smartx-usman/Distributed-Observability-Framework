FROM python:alpine3.15

ENV SENSORS="1"
ENV MESSAGE_DELAY="1"
ENV MQTT_BROKER="mqtt-mosquitto.uc0.svc.cluster.local"
ENV MQTT_BROKER_PORT="1883"
ENV MQTT_TOPIC="mqtt/temperature"
ENV START_VALUE="1"
ENV END_VALUE="10"
ENV VALUE_TYPE="integer"
ENV INVALID_VALUE_OCCURRENCE="10"
ENV INVALID_VALUE="99"

ARG Pathdir="/mqtt"

RUN mkdir $Pathdir
RUN pip3 install paho-mqtt

COPY publish.py $Pathdir

WORKDIR $Pathdir

ENTRYPOINT ["python3", "publish.py"]