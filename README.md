![Zoom2youtube showcase](http://i.imgur.com/snCLd13.gif)

# Zoom2Youtube is a utility for transferring video recordings from the Zoom.us to YouTube

At [Welltory](https://welltory.com), we hold and record 3-4 virtual meetings every day. The easiest way is to record meetings in [zoom.us](https://zoom.us), then upload them to YouTube where they can be accessed by anyone, from any device: phones, Chromecast, etc. We’ve automated video transfers from Zoom to YouTube, added notifications, and now every recording is automatically dropped into a Slack channel. We use privacy settings (**unlisted**) on YouTube to make sure people who aren’t on the team don’t have access to our meetings.

The project is written in Python and launched in Docker. This simplifies the project’s initial deployment.

# About

Disclaimer: The utility is supplied "AS IS" without any warranties.

You can reach us at github@welltory.com

# Features

- Automatically download a new Zoom video
- Upload the video to YouTube (privacy settings: unlisted)
- Drop a link to the YouTube video into a Slack channel
- Filter settings: will not upload videos under 15 minutes long to prevent uploads of accidental recordings



Quick Start Guide
=========

Step 1 - Set up Docker
------------------------

Install Docker and Docker-Compose

- Docker installation instructions: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce
- Docker-compose installation instructions: https://docs.docker.com/compose/install/#alternative-install-options

Then create a Docker image. To do this, enter the command:

```
    $ make build
```


Step 2 - set up Zoom
----------------------

You need to create a `.env` file in the root directory of the project, specifying the keys listed below:

    ZOOM_KEY
    ZOOM_SECRET
    ZOOM_HOST_ID
    ZOOM_EMAIL
    ZOOM_PASSWORD

To get the keys, follow these steps:
1. Follow the link: https://api.zoom.us/developer/api/credential
2. Enable the API
3. Enter the `API Key` in `ZOOM_KEY`, `API Secret` in `ZOOM SECRET`
4. Follow the link: https://api.zoom.us/developer/api/playground
5. In the API Endpoint field, select https://api.zoom.us/v1/chat/list
6. Enter the `Host User ID` in `ZOOM_HOST_ID`


Step 3 - Set up Youtube
-------------------------

Add the following keys to the `.env` file

    GOOGLE_REFRESH_TOKEN
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET

To get the keys, follow these steps:
1. Go to the developer console: https://console.developers.google.com/cloud-resource-manager
2. Create a new project and go to the new project
3. Follow the link: https://console.developers.google.com/apis/api/youtube.googleapis.com/overview
4. Turn on `YouTube Data API v3`
5. Follow the link: https://console.developers.google.com/apis/credentials
6. create OAuth client credentials.
7. Select Other types or `Other` (depends on localization), create
8. Enter `Client ID` in `GOOGLE_CLIENT_ID` and `Client Secret` in `GOOGLE_CLIENT_SECRET`

To get the `GOOGLE_REFRESH_TOKEN` follow these steps:

1. Follow the link: [https://accounts.google.com/o/oauth2/auth?client_id=<GOOGLE_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code](https://accounts.google.com/o/oauth2/auth?client_id=<MY_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code), **replacing** `<GOOGLE_CLIENT_ID>` with the `GOOGLE_CLIENT_ID`, you got from the previous step
2. Select the Google account you need access for
3. Get access
4. Enter the token in the .env file, in the `.env` in the `GOOGLE_CODE` field
5. Run the script in docker container
```
    $ docker-compose run app bash
    $ python3.6 src/get_google_refresh_token.py`
```
6. Enter the refresh token in the `.env` file, in the `GOOGLE_REFRESH_TOKEN` field


Step 4 - Set up Slack
-----------------------

Add the following keys to the `.env` file

    SLACK_CHANNEL
    SLACK_TOKEN

1. Enter the recipients (separated with commas) in `SLACK_CHANNEL`, for example `SLACK_CHANNEL=#my_cannel,@my_user`
2. Enter the slack token in `SLACK_TOKEN`


Step 5 - Check keys
-----------------------

To make sure all the keys were entered into the `.env` file, run the script in docker container
```
    $ docker-compose run app bash
    $ python3.6 src/check_env.py
```


Step 6 - Run the app
-------------------------

Launch the container:
```
    $ make up
```


Another way to run the app, through virtualenv
------------------------------------------------------------------------

1. Create a virtual environment
```
    $ virtualenv venv -p /usr/bin/python3 --no-site-package
```
2. Activate virtual environment
```
    $ source venv/bin/activate
```
3. Establish requirements
```
    $ pip install -r requirements.txt
```
4. Copy cron config
```
    $ sudo cp cron/crontab /etc/cron.d/zoom2youtube-cron
```
5. Restart cron
```
    $  sudo service cron restart
```

Sample .env file
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

[The MIT License (MIT)](https://en.wikipedia.org/wiki/MIT_License)
