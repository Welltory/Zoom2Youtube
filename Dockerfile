FROM python:3.7.3-slim-stretch

RUN apt-get update && apt-get install -y python3-dev build-essential curl jq && pip install -U pip && pip install -U pip-tools
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/ffmpeg-4
RUN apt-get install -y ffmpeg

RUN apt-get install -y cron

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /opt/app

RUN touch /var/log/cron.log
