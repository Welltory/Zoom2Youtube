from urllib.parse import urljoin

from webhooks.backends.base import WebHookBase
from settings import SLACK_CHANNEL, SLACK_TOKEN, SLACK_CHANNELS_UNIQUE_SETTINGS, NOT_SEND_MSG_TO_PUBLIC_CHANNEL_FOR_MEETINGS


class SlackClient(WebHookBase):

    BASE_URL = 'https://slack.com/api/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_url = urljoin(self.BASE_URL, 'chat.postMessage')
        self.channels = [ch.strip() for ch in SLACK_CHANNEL.split(',') if ch]
        self.channels_unique_settings = SLACK_CHANNELS_UNIQUE_SETTINGS
        self.bot_name = 'zoom2youtube'
        self.token = SLACK_TOKEN

    def get_url(self, event_name, **kwargs) -> str:
        return self.chat_url

    def get_request_method(self, event_name, **kwargs) -> str:
        return 'post'

    def send(self, event_name: str, **kwargs):
        data = self.get_data_for_event(event_name, **kwargs)
        url = self.get_url(event_name, **kwargs)
        method = self.get_request_method(event_name, **kwargs)
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        if self.payload['result']['name'] not in NOT_SEND_MSG_TO_PUBLIC_CHANNEL_FOR_MEETINGS:
            for channel in self.channels:
                data['channel'] = channel
                self._request(url, method=method, payload=data, headers=headers)

        for video_name, channels in self.channels_unique_settings.items():
            if video_name in self.payload['result']['name']:
                for channel in channels:
                    data['channel'] = channel
                    self._request(
                        url, method=method, payload=data, headers=headers
                    )

    def new_video(self, **kwargs):
        name = self.payload['result']['name']
        link = self.payload['result']['link']
        text = '{} - {}'.format(name, link)
        data = {'text': text, 'token': self.token}
        if self.bot_name:
            data['username'] = self.bot_name
        return data
