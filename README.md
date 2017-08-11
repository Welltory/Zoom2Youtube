# Zoom2Youtube is a utility for transfer video recordings from the Zoom.us to YouTube

В Welltory(https://welltory.com) мы проводим и записываем 3-4 видео встречи команд каждый день.
Удобнее всего записывать встречи в Zoom.us(https://zoom.us), а потом перекладывать их в YouTube
и там просматривать, ведь каждый из нас по разному потребляет видео - кто со смартфона, кто с Chromecast или с ПК.
Мы автоматизировали рутину трансфера видео из Zoom в YouTube, добавили к ней уведомления и теперь запись каждого
митинга автоматически попадает к нам в Slack. Чтобы видео не было публичным на YouTube, мы всегда используем приватности - unlisted.

Проект написан на Python и запускается в Docker. Это упрощает первичное развертывание проекта.

# About

Disclaimer: The utility is supplied "AS IS" without any warranties.

You can reach us at github@welltory.com

# Features

- автоматически скачать новое видео из Zoom
- закачать это видео в YouTube с правами доступа unlisted
- cкинуть ссылку на загруженное видео в Slack канал
- имеет фильтр на скачку - не выгржуает видео короче 15 минут, чтобы не переливать случайные записи


Quick Start Guide
=========

Шаг 1 - установка Docker
------------------------

Для использования утилиты необходимо установить Docker и Docker-Compose

- Инструкция по установке docker: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
- Инструкция по установке docker-compose: https://docs.docker.com/compose/install/#alternative-install-options

Затем собрать Docker образ. Для этого необходимо выполнить команду

```
    $ make build
```


Шаг 2 - настройка Zoom
----------------------

Для работы приложения необходимо создать `.env` файл в корне проекта, указав в нем ключи, описанные ниже:

    ZOOM_KEY
    ZOOM_SECRET
    ZOOM_HOST_ID
    ZOOM_EMAIL
    ZOOM_PASSWORD

Для получения этих ключей необходимо выполнить следующие шаги:
- перейти по ссылке https://api.zoom.us/developer/api/credential
- активировать API
- записать `API Key` в `ZOOM_KEY`, `API Secret` в `ZOOM SECRET`

- перейти по ссылке https://api.zoom.us/developer/api/playground
- в поле API Endpoint выбрать https://api.zoom.us/v1/chat/list
- записать `Host User ID` в `ZOOM_HOST_ID`

Шаг 3 - настройка Youtube
-------------------------

В файл `.env` добавить ключи

    GOOGLE_REFRESH_TOKEN
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET

Для получения этих ключей необходимо выполнить следующие шаги:
- перейти в консоль разработчика https://console.developers.google.com/cloud-resource-manager
- создать новый проект и перейдите в созданный проект
- перейти по сслылке https://console.developers.google.com/apis/api/youtube.googleapis.com/overview
- активировать `YouTube Data API v3`

- перейти по ссылке https://console.developers.google.com/apis/credentials
- создать учетные данные для клиента OAuth.
- выбрать `Другие типы` или `Other`(зависит от локализации), создать
- записать `Client ID` в `GOOGLE_CLIENT_ID` и `Client Secret` в `GOOGLE_CLIENT_SECRET`

Для получения `GOOGLE_REFRESH_TOKEN` выполнить следующие действия:

- открыть ссылку [https://accounts.google.com/o/oauth2/auth?client_id=<GOOGLE_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code](https://accounts.google.com/o/oauth2/auth?client_id=<MY_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code),
  заменив в ссылке `<GOOGLE_CLIENT_ID>` на `GOOGLE_CLIENT_ID`, полученный на предыдущем шаге
- выбрать нужный google акканут для которого нужно получить доступ
- принять доступ
- записать полученный токен в `.env` в параметр `GOOGLE_CODE`
- запустить скрипт в docker контейнере
```
    $ docker-compose run app bash
    $ python3.6 src/get_google_refresh_token.py`
```
- полученный refresh token записать в файла `.env` в параметр `GOOGLE_REFRESH_TOKEN`

Шаг 4 - настройка Slack
-----------------------

В файл `.env` добавить ключи

    SLACK_CHANNEL
    SLACK_TOKEN

- записать через запятую получателей в `SLACK_CHANNEL`, например `SLACK_CHANNEL=#my_cannel,@my_user`
- записать slack token в `SLACK_TOKEN`



Шаг 5 - Проверка ключей
-----------------------

Для проверки, что все ключи были записаны в `.env` файл необходимо запустить скрипт в docker контейнере
```
    $ docker-compose run app bash
    $ python3.6 src/check_env.py
```


Шаг 6 - запуск приложения
-------------------------

Запустить контейнер:
```
    $ make up
```


Шаг 6 - альтернативный способ запуска приложения, через virtualenv
------------------------------------------------------------------------

- Создать виртуальное окружение
```
    $ virtualenv venv -p /usr/bin/python3 --no-site-package
```
- Активировать виртуальное окружение
```
    $ source venv/bin/activate
```
- Установить зависимости
```
    $ pip install -r requirements.txt
```
- Скопировать cron конфиг
```
    $ sudo cp cron/crontab /etc/cron.d/zoom2youtube-cron
```
- Перезапустить крон
```
    $  sudo service cron restart
```

Пример .env файла
-----------------

```
ZOOM_KEY=AAAAAAAAAAAAAAA
ZOOM_SECRET=BBBBBBBBBBBB
ZOOM_HOST_ID=CCCCCCCCCCC
ZOOM_EMAIL=mail@gmail.com
ZOOM_PASSWORD=user_password

GOOGLE_CLIENT_ID=AAAAAAAAAAAAAA.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=BBBBBBBBBBBBBb
GOOGLE_REFRESH_TOKEN=CCCCCCCCCCCC
GOOGLE_CODE=DDDDDDDDDDDDDD

SLACK_CHANNEL=@user
SLACK_TOKEN=AAAAAAAAAAAAA
```


License
-------

The MIT License (MIT)