FROM python:3.8-slim

ARG Pathdir="/"

#RUN apt update && \
#      apt install -y software-properties-common curl && \
#      add-apt-repository ppa:deadsnakes/ppa && \
#      apt install -y python3.9 && \
#      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
#      chmod +x ./kubectl && \
#      mv ./kubectl /usr/local/bin/kubectl

RUN apt update && \
      apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl

RUN pip3 install pika

ADD data-analyzer.py $Pathdir

WORKDIR $Pathdir