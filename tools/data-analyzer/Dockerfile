FROM python:3.8-slim

ARG Pathdir="/telegraf"
RUN mkdir $Pathdir

RUN apt update && \
      apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl

ADD data-analyzer.py $Pathdir

WORKDIR $Pathdir