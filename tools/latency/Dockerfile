FROM python:3.8-slim

ARG Pathdir="/latency"

RUN pip3 install tcp-latency
RUN pip3 install kubernetes
RUN pip3 install kafka-python

RUN mkdir $Pathdir

ADD tcp-latency.py $Pathdir
ADD server.py $Pathdir

WORKDIR $Pathdir