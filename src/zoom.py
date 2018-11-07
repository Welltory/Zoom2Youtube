# -*- coding: utf-8 -*-

import os.path
from datetime import datetime
from urllib.parse import urljoin

import requests


class ZoomClient(object):
    BASE_URL = 'https://api.zoom.us/v1/'
    SIGNIN_URL = 'https://api.zoom.us/signin'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def post(self, api_url, **kwargs):
        data = {'api_key': self.api_key, 'api_secret': self.api_secret}
        if kwargs:
            data.update(kwargs)
        url = self._join_url(api_url)
        response = requests.post(url, data)
        return response

    def session(self, email, password):
        session = requests.Session()
        session.headers.update({
            'content-type': 'application/x-www-form-urlencoded'
        })
        response = session.post(
            ZoomClient.SIGNIN_URL, data={'email': email, 'password': password}
        )
        return session, response

    def _join_url(self, path):
        if path.startswith('/'):
            path = path[1:]
        return urljoin(ZoomClient.BASE_URL, path)


class ZoomRecording(object):
    def __init__(self, api_key, api_secret, host_id, **kwargs):
        self.client = ZoomClient(api_key, api_secret)
        self.host_id = host_id

        self.duration_min = kwargs.get('duration_min', 10)

    def list(self):
        response = self.client.post("/recording/list", host_id=self.host_id)
        return response.json()

    def delete(self, meeting_id):
        response = self.client.post("/recording/delete", meeting_id=meeting_id)
        return response.json()

    def get_meetings(self):
        meetings = self.list().get('meetings', [])
        return filter(
            lambda item: item.get('duration', 0) > self.duration_min, meetings
        )

    def download_meetings(self, email, password, save_dir, downloaded_files):
        session, response = self.client.session(email, password)
        if response.status_code != 200:
            session.close()
            return

        for meeting in self.get_meetings():
            recording_files = meeting.get('recording_files', [])
            for i, video_data in enumerate(recording_files):
                rid = video_data.get('id')

                if video_data.get('file_type') != 'MP4':
                    continue

                if not self._is_downloaded(downloaded_files, rid):
                    continue

                prefix = i or ''
                filename = self._get_output_filename(meeting, prefix)
                save_path = self._get_output_path(filename, save_dir)
                self._real_download_file(session,
                                         video_data.get('download_url'),
                                         save_path)
                print('Downloaded the file: {}'.format(video_data.get('download_url')))
                self._save_to_db(downloaded_files, rid)
                # TODO Remove video processing

        session.close()

    def _is_downloaded(self, downloaded_files, recording_id):
        if not os.path.exists(downloaded_files):
            return True

        with open(downloaded_files, 'r') as f:
            ids = [x.strip() for x in f.readlines() if x]

        if recording_id in ids:
            return False

        return True

    def _get_output_filename(self, meeting, prefix=''):
        start_time = datetime.strptime(
            meeting.get('start_time'), '%Y-%m-%dT%H:%M:%SZ'
        ).strftime('%d-%m-%Y')
        topic = meeting.get('topic').replace('/', '.')
        return '{}{} {}.mp4'.format(topic, prefix, start_time)

    def _get_output_path(self, fname, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return os.path.join(save_dir, fname)

    def _real_download_file(self, session, url, fpath):
        response = session.get(url)
        if response.status_code == 200:
            with open(fpath.encode('utf-8'), 'wb') as f:
                f.write(response.content)
            return True
        return False

    def _save_to_db(self, downloaded_files, recording_id):
        with open(downloaded_files, 'a+') as f:
            f.write('{}\n'.format(recording_id))
