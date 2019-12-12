FROM python:3.7.3-slim-stretch

RUN apt-get update && apt-get install -y build-essential curl python3.7-dev python3-pip
RUN python3.7 -m pip install pip --upgrade
RUN python3.7 -m pip install wheel

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/ffmpeg-4
RUN apt-get install -y ffmpeg

RUN apt-get install -y cron

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /opt/app

RUN touch /var/log/cron.log
