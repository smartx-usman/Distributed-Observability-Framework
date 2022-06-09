FROM python:3.8-slim

ARG Pathdir="/telegraf"
RUN mkdir $Pathdir

ADD data-analyzer.py $Pathdir

WORKDIR $Pathdir