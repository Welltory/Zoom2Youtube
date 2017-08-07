FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip

RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /opt/app

ADD cron/crontab /etc/cron.d/zoom2youtube-cron

RUN chmod 0644 /etc/cron.d/zoom2youtube-cron

RUN touch /var/log/cron.log

RUN apt-get install -y cron
