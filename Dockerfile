FROM python:3.7.4-stretch

RUN apt-get update
RUN apt-get install -y cron

# RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:jonathonf/ffmpeg-4
# RUN apt-get install -y ffmpeg

RUN python3.7 -m pip install pip --upgrade

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkfifo --mode 0666 /var/log/cron.log

WORKDIR /opt/app

CMD ["/bin/bash", "-c", "crontab cron/crontab && service cron start && tail -f /var/log/cron.log & wait $!"]
