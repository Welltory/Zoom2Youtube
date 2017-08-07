from urllib.parse import urljoin
import requests


class SlackClient(object):
    BASE_URL = 'https://slack.com/api/'

    def __init__(self, token, bot_name=''):
        self.token = token
        self.bot_name = bot_name

    def _request(self, method, params):
        url = urljoin(SlackClient.BASE_URL, method)
        data = {'token': self.token}
        if self.bot_name:
            data['username'] = self.bot_name
        params.update(data)
        return requests.post(
            url,
            data=params,
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )

    def chat_post_message(self, channel, text, **params):
        """https://api.slack.com/methods/chat.postMessage"""
        method = 'chat.postMessage'
        params.update({
            'channel': channel,
            'text': text,
        })
        return self._request(method, params)
