import os.path

from datetime import datetime
from datetime import timedelta
from urllib.parse import urljoin

import requests

from jwt_auth import make_http_headers
from jwt_auth import generate_access_token


class ZoomJWTClient(object):

    BASE_URL = 'https://api.zoom.us/v2/'

    def __init__(
            self,
            api_key: str,
            api_secret: str,
            token_exp_delta: int
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_exp_delta = token_exp_delta

        self._setup()

    def _setup(self):
        self.access_token = generate_access_token(
            self.api_key,
            self.api_secret,
            self.token_exp_delta
        )
        self.http_headers = make_http_headers(self.access_token)

    def _join_url(self, path):
        if path.startswith('/'):
            path = path[1:]
        return urljoin(self.BASE_URL, path)

    def get(self, uri: str, **kwargs):
        url = self._join_url(uri)
        resp = requests.get(url, headers=self.http_headers, timeout=60)
        return resp


class ZoomRecording(object):
    def __init__(
            self,
            client,
            email,
            duration_min=10,
            filter_meeting_by_name=False,
            only_meeting_names=None,
            from_day_delta=7,
            page_size=10,
    ):

        self.client = client
        self.email = email

        self.duration_min = duration_min
        self.filter_meeting_by_name = filter_meeting_by_name
        self.only_meeting_names = only_meeting_names or []
        self.from_day_delta = from_day_delta

    def get_meetings(self):
        uri = "users/{}/recordings?from={}&page_size={}".format(
            self.email,
            (datetime.utcnow() - timedelta(days=self.from_day_delta)).strftime("%Y-%m-%d"),
            page_size
        )
        resp = self.client.get(uri)
        if resp.status_code != 200:
            print(
                "Get meeting status error: {}. Detail: {}".format(
                    resp.status_code, resp.content
                )
            )
            return None

        data = resp.json()
        return data.get('meetings', [])

    def filter_meetings(self, meetings):
        for m in meetings:
            if m.get("duration", 0) < self.duration_min:
                continue

            if self.filter_meeting_by_name and m.get("topic").strip() not in self.only_meeting_names:
                continue

            yield m

    def download_meetings(self, save_dir, downloaded_files):
        meetings = self.get_meetings()
        if not meetings:
            print("Does not exists meetings.")
            return

        meetings = self.filter_meetings(meetings)
        for meeting in meetings:
            recording_files = filter(
                lambda x: x.get("file_type") == "MP4",
                meeting.get('recording_files', [])
            )
            for i, video_data in enumerate(recording_files):
                rid = video_data.get('id')

                if not self._is_downloaded(downloaded_files, rid):
                    continue

                prefix = i or ''
                filename = self._get_output_filename(meeting, prefix)
                save_path = self._get_output_path(filename, save_dir)

                download_url = video_data.get('download_url')
                download_url += "?access_token={}".format(self.client.access_token)
                self._real_download_file(
                    download_url,
                    save_path
                )

                print('Downloaded the file: {}'.format(video_data.get('download_url')))
                self._save_to_db(downloaded_files, rid)
                # TODO Remove video processing

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

    def _real_download_file(self, url, fpath):
        response = requests.get(url)
        if response.status_code == 200:
            with open(fpath.encode('utf-8'), 'wb') as f:
                f.write(response.content)
            return True
        return False

    def _save_to_db(self, downloaded_files, recording_id):
        with open(downloaded_files, 'a+') as f:
            f.write('{}\n'.format(recording_id))
