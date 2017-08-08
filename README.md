# zoom2youtube

Для работы приложения необходимо создать `.env` файл в корне проекта, указав в нем ключи, описанные ниже:

Ключи для zoom.us:
------------------

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


Ключи для youtube:
------------------

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
- открыть ссылку https://accounts.google.com/o/oauth2/auth?client_id=<MY_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code
- выбрать нужный google акканут для которого нужно получить доступ
- принять доступ
- записать полученный токен в `.env` в параметре `GOOGLE_CODE`
- запустить скрипт `python3.6 src/get_token.py`
- полученный refresh token записать в `GOOGLE_REFRESH_TOKEN`

Ключи для slack:
----------------

    SLACK_CHANNEL
    SLACK_TOKEN

- записать через запятую получателей в `SLACK_CHANNEL`, например `SLACK_CHANNEL=#my_cannel,@my_user`
- записать slack token в `SLACK_TOKEN`


Проверка ключей:
----------------
Для проверки, что все ключи были записаны в `.env` файл необходимо запустить скрипт `python3.6 src/check_keys.py`


Установка docker:
-----------------
Инструкция по установке docker: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
Инструкция по установке docker-compose: https://docs.docker.com/compose/install/#alternative-install-options


Запуск
------
Собрать докер образ командой:
```
    $ make build
```
Запустить контейнер:
```
    $ make up
```

Альтернативный запуск через virtualenv
--------------------------------------

- создать виртуальное окружение
```
    $ virtualenv venv -p /usr/bin/python3 --no-site-package
```
- активировать виртуальное окружение
```
    $ source venv/bin/activate
```
- установить зависимости
```
    $ pip install -r requirements.txt
```
- скопировать cron конфиг
```
    $ sudo cp cron/crontab /etc/cron.d/zoom2youtube-cron
```
- перезапустить крон
```
    $  sudo service cron restart
```


License
-------

The MIT License (MIT)