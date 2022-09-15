FROM python:3.8-slim

#ENV FLASK_APP=app.py

ARG Pathdir="/app"

RUN apt -y update && apt -y install --no-install-recommends vim sysbench

RUN mkdir $Pathdir

COPY app.py $Pathdir
COPY test_strategy.lua $Pathdir

WORKDIR $Pathdir

#RUN chmod +x load-testing/disk-load.sh

#ENTRYPOINT ["python3", "app.py"]