FROM python:alpine3.15

ENV MQTT_BROKER="10.244.2.119"
ENV KAFKA_BROKER="bitnami-kafka-0.bitnami-kafka-headless.uc0.svc.cluster.local:9092"

ARG Pathdir="/mqtt"

RUN mkdir $Pathdir

COPY subscribe.py $Pathdir
COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR $Pathdir

ENTRYPOINT ["python3", "subscribe.py"]