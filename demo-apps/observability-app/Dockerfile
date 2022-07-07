FROM python:3.8-slim

ENV SENSORS="1"

ARG Pathdir="/app"

RUN apt -y update && apt -y install stress curl
RUN mkdir $Pathdir

#ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

COPY requirements.txt .
COPY app.py app2.py $Pathdir

#RUN apk update && apk add build-essential
#RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN opentelemetry-bootstrap --action=install
RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR $Pathdir

#RUN chmod +x load-testing/disk-load.sh

#ENTRYPOINT ["python3", "app.py"]