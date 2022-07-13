FROM python:3.8-slim

#ENV FLASK_APP=app.py
#ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

ARG Pathdir="/app"

RUN apt -y update && apt -y install --no-install-recommends build-essential stress curl vim default-libmysqlclient-dev
RUN mkdir $Pathdir

COPY requirements.txt .
#RUN apk update && apk add build-essential
#RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN opentelemetry-bootstrap --action=install
#RUN /usr/local/bin/python -m pip install --upgrade pip

COPY app.py $Pathdir


WORKDIR $Pathdir

#RUN chmod +x load-testing/disk-load.sh

#ENTRYPOINT ["python3", "app.py"]