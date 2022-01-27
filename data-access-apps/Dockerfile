FROM python:3.8-alpine

ARG Pathdir="/querier"

RUN mkdir $Pathdir
RUN mkdir /data

COPY es-data-querier.py $Pathdir

#COPY requirements.txt .

#RUN apk update && apk add curl
RUN pip3 install requests

WORKDIR $Pathdir

#ENTRYPOINT ["python3", "actuate.py"]