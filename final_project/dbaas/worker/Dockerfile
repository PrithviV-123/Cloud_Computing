FROM ubuntu:latest
RUN apt-get update
RUN apt-get -y install python3 python3-pip mongo-tools

WORKDIR /worker
COPY . /worker

ENV TEAM_NAME=CC_2394_0716_2374_2376

RUN pip3 install -r requirements.txt
