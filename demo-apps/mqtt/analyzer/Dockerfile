FROM python:3.8-alpine

ENV MQTT_BROKER="10.244.2.119"
ENV KAFKA_BROKER="bitnami-kafka-0.bitnami-kafka-headless.uc0.svc.cluster.local:9092"

ARG Pathdir="/fust"

RUN mkdir $Pathdir

COPY temp-analyzer.py $Pathdir
COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR $Pathdir

CMD ["python3", "temp-analyzer.py", "worker", "-l", "info"]