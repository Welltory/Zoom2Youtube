# -*- coding: utf-8 -*-

import os
import random
import time
import re
from typing import List

import httplib2
import requests

try:
    import httplib
except ImportError:
    import http.client as httplib

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import AccessTokenCredentials

from helpers import import_by_string
from settings import WEBHOOK_BACKEND_PIPELINES


# Explicitly tell the underlying HTTP transport library not to retry,
# since we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, httplib.NotConnected,
    httplib.IncompleteRead, httplib.ImproperConnectionState,
    httplib.CannotSendRequest, httplib.CannotSendHeader,
    httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError
# with one of these status codes is raised.
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


class YoutubeRecording(object):
    def __init__(self, client_id, client_sercet, refresh_token):
        self.client = YoutubeClient(client_id, client_sercet, refresh_token)

    def upload_from_dir(self, video_dir: str,
                        privacy_status='unlisted',
                        remove_file=True,
                        notify=True):

        assert os.path.isdir(video_dir), "Not found directory"
        files = self._get_files_from_dir(video_dir, 'mp4')
        for fname in files:
            fpath = os.path.join(video_dir, fname)
            if not os.path.exists(fpath):
                continue
            title = os.path.splitext(os.path.basename(fname))[0]
            options = dict(
                file=fpath,
                title=title,
                privacyStatus=privacy_status,
            )
            video_id = self.upload_video(options)
            if not video_id:
                continue

            video_url = 'https://www.youtube.com/watch?v={}'.format(video_id)
            print('File uploaded: {}'.format(video_url))

            if notify:
                match = re.search(r'\d{2}-\d{2}-\d{4}', title)
                date = match.group() if match else None
                payload = {
                    "success": True,
                    "result": {
                        "name": title,
                        "link": video_url,
                        "date": date,
                    }
                }
                self.webhooks(payload=payload)

            if remove_file:
                os.remove(fpath)

    def upload_video(self, options: dict):
        """
        Options is Dict with

        file - filepath to video
        title - title of video
        privacyStatus

        :param options:
        :return:
        """
        body = self._generate_meta_data(options)
        connector = self.client.get_authenticated_service()
        insert_request = connector \
            .videos() \
            .insert(part=",".join(body.keys()),
                    body=body,
                    media_body=MediaFileUpload(options.get('file'),
                                               chunksize=-1,
                                               resumable=True))
        try:
            return self._real_upload_video(insert_request)
        except Exception as e:
            print(str(e))

    def _generate_meta_data(self, options: dict):
        return dict(
            snippet=dict(
                title=options.get('title'),
            ),
            status=dict(
                privacyStatus=options.get('privacyStatus')
            )
        )

    def _real_upload_video(self, insert_request):
        response = None
        error = None
        retry = 0
        print('File upload in progress...', end='')
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                print('.', end='')
                if 'id' in response:
                    print()
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

    def _get_files_from_dir(self, path: str, ext: str) -> List[str]:
        """
        Return list of files with .ext
        :param path:
        :param ext:
        :return:
        """
        return [x for x in os.listdir(path) if x.endswith('.{}'.format(ext))]

    def webhooks(self, **kwargs):
        kwargs['event_name'] = 'new_video'
        for backend in WEBHOOK_BACKEND_PIPELINES:
            klass = import_by_string(backend)
            klass(kwargs=kwargs).start()
