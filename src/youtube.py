import os
import random
import time

import requests
import httplib2

try:
    import httplib
except ImportError:
    import http.client as httplib

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import AccessTokenCredentials

from slack import SlackClient
from settings import SLACK_TOKEN, SLACK_CHANNEL


# Explicitly tell the underlying HTTP transport library not to retry, since we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, httplib.NotConnected,
    httplib.IncompleteRead, httplib.ImproperConnectionState,
    httplib.CannotSendRequest, httplib.CannotSendHeader,
    httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status codes is raised.
RETRIABLE_STATUS_CODES = (500, 502, 503, 504)


class YoutubeClient(object):
    def __init__(self, client_id, client_sercet, refresh_token):
        self.client_id = client_id
        self.client_secret = client_sercet
        self.refresh_token = refresh_token

    def get_auth_code(self):
        """ Get access token for connect to youtube api """
        oauth_url = 'https://accounts.google.com/o/oauth2/token'
        data = dict(
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='refresh_token',
        )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        response = requests.post(oauth_url, data=data, headers=headers)
        response = response.json()
        return response.get('access_token')

    def get_authenticated_service(self):
        """ Create youtube oauth2 connection """
        credentials = AccessTokenCredentials(
            access_token=self.get_auth_code(),
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        )
        return build(
            'youtube', 'v3', http=credentials.authorize(httplib2.Http())
        )

    def get_authenticated_service_by_key(self, api_key):
        return build(
            'youtube', 'v3', developerKey=api_key
        )


class YoutubeRecording(object):
    def __init__(self, client_id, client_sercet, refresh_token):
        self.client = YoutubeClient(client_id, client_sercet, refresh_token)
        self.slack_client = SlackClient(SLACK_TOKEN, 'zoom2youtube')

    def youtube_meta_data(self, options: dict):
        return dict(
            snippet=dict(
                title=options.get('title'),
            ),
            status=dict(
                privacyStatus=options.get('privacyStatus')
            )
        )

    def initialize_upload(self, options: dict):
        body = self.youtube_meta_data(options)
        connector = self.client.get_authenticated_service()
        insert_request = connector.videos().insert(
            part=",".join(body.keys()), body=body,
            media_body=MediaFileUpload(options.get('file'), chunksize=-1, resumable=True))
        return self.resumable_upload(insert_request)

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if 'id' in response:
                    return response['id']
            except HttpError as err:
                if err.resp.status in RETRIABLE_STATUS_CODES:
                    error = True
                else:
                    raise
            except RETRIABLE_EXCEPTIONS:
                error = True

            if error:
                retry += 1
                if retry > MAX_RETRIES:
                    raise Exception('Maximum retry are fail')

                sleep_seconds = random.random() * 2 ** retry
                time.sleep(sleep_seconds)

    def uploads_videos(self, video_dir):
        files = YoutubeRecording.get_video_files(video_dir, 'mp4')
        for fname in files:
            fpath = os.path.join(video_dir, fname)
            if not os.path.exists(fpath):
                continue
            options = dict(
                file=fpath,
                title=os.path.splitext(os.path.basename(fname))[0],
                privacyStatus='unlisted',
            )
            video_id = self.initialize_upload(options)
            video_url = 'https://www.youtube.com/watch?v={}'.format(video_id)
            print(video_url)
            self.notify(video_url)
            os.remove(fpath)

    def notify(self, video_url):
        try:
            self.slack_client.chat_post_message(SLACK_CHANNEL, video_url)
        except Exception as e:
            print('Sending error to slack: {}'.format(str(e)))

    @staticmethod
    def get_video_files(path: str, ext: str) -> list:
        return [x for x in os.listdir(path) if x.endswith('.{}'.format(ext))]