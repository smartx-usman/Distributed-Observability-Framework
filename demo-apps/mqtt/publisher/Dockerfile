FROM python:latest
ENV SENSORS="1"
ENV MESSAGE_DELAY="1"
ARG Pathdir="/mqtt"
RUN mkdir $Pathdir
RUN pip3 install paho-mqtt
COPY publish.py $Pathdir
WORKDIR $Pathdir
ENTRYPOINT ["python3", "publish.py"]