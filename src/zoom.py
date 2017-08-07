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

    def join_url(self, path):
        if path.startswith('/'):
            path = path[1:]
        return urljoin(ZoomClient.BASE_URL, path)

    def post(self, api_url, **kwargs):
        data = {'api_key': self.api_key, 'api_secret': self.api_secret}
        if kwargs:
            data.update(kwargs)
        url = self.join_url(api_url)
        response = requests.post(url, data)
        return response

    def session(self, email, password):
        session = requests.Session()
        session.headers.update(
            {'content-type': 'application/x-www-form-urlencoded'}
        )
        response = session.post(
            ZoomClient.SIGNIN_URL, data={'email': email, 'password': password}
        )
        return session, response


class ZoomRecording(object):
    def __init__(self, api_key, api_secret, host_id):
        self.client = ZoomClient(api_key, api_secret)
        self.host_id = host_id

    def list(self):
        response = self.client.post("/recording/list", host_id=self.host_id)
        return response.json()

    def delete(self, meeting_id):
        response = self.client.post("/recording/delete", meeting_id=meeting_id)
        return response.json()

    def get_meetings(self):
        meetings = self.list().get('meetings', [])
        meetings = filter(
            lambda item: item.get('duration', 0) <= 15, meetings
        )
        return meetings

    def download_meetings(self, email, password, save_dir):
        session, response = self.client.session(email, password)
        if response.status_code == 200:
            for meeting in self.get_meetings():
                recording_files = meeting.get('recording_files', [])
                for i, rfile in enumerate(recording_files):
                    if rfile.get('file_type') == 'MP4':
                        prefix = i or ''
                        fname = self.get_file_name(meeting, prefix)
                        save_path = ZoomRecording.get_save_path(fname, save_dir)
                        result = ZoomRecording.download_file(
                            session, rfile.get('download_url'), save_path
                        )
                        if result:
                            self.delete(meeting.get('uuid'))
        session.close()

    def get_file_name(self, meeting, prefix=''):
        start_time = datetime.strptime(
            meeting.get('start_time'), '%Y-%m-%dT%H:%M:%SZ'
        ).strftime('%d-%m-%Y')
        fname = '{}{} {}.mp4'.format(meeting.get('topic'), prefix, start_time)
        return fname

    @staticmethod
    def get_save_path(fname, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return os.path.join(save_dir, fname)

    @staticmethod
    def download_file(session, url, fpath):
        response = session.get(url)
        if response.status_code == 200:
            with open(fpath, 'wb') as f:
                f.write(response.content)
            return True
        return False