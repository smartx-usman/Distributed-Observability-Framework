FROM openjdk:slim-buster

#ENV FLASK_APP=app.py

ARG Pathdir="/app"

RUN apt -y update && apt -y install --no-install-recommends wget vim python3 python3-pip ca-certificates \
         curl python3-setuptools python3-wheel

RUN mkdir $Pathdir
RUN wget https://dlcdn.apache.org/cassandra/4.0.4/apache-cassandra-4.0.4-bin.tar.gz && \
    tar zxvf apache-cassandra-4.0.4-bin.tar.gz && \
    rm -rf apache-cassandra-4.0.4-bin.tar.gz && \
    mv apache-cassandra-4.0.4 $Pathdir
#RUN apache-cassandra-4.0.4/tools/bin/cassandra-stress

RUN pip3 install cassandra-driver
RUN apt -y remove --purge wget

COPY app.py $Pathdir
COPY stress.yaml $Pathdir

WORKDIR $Pathdir

#RUN chmod +x load-testing/disk-load.sh

#ENTRYPOINT ["python3", "app.py"]