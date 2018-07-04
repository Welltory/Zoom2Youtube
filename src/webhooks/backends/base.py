import time

from threading import Thread

import requests


class WebHookBase(Thread):

    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        assert kwargs
        self.event_name = kwargs.get('event_name')
        self.payload = kwargs.get('payload')

        assert self.event_name, 'not specified event name'
        assert self.payload, 'not specified payload'

    def run(self):
        self.send(self.event_name, payload=self.payload)

    def get_url(self, event_name, **kwargs) -> str:
        raise NotImplementedError

    def get_request_method(self, event_name, **kwargs) -> str:
        raise NotImplementedError

    def send(self, event_name: str, **kwargs):
        data = self.get_data_for_event(event_name, **kwargs)
        url = self.get_url(event_name, **kwargs)
        method = self.get_request_method(event_name, **kwargs)
        return self._request(url, method=method, payload=data)

    def get_method_by_event_name(self, event_name):
        method = getattr(self, event_name, None)
        if not method:
            raise NotImplementedError(
                'Event {} not implemented'.format(event_name)
            )
        return method

    def get_data_for_event(self, event_name, **kwargs):
        method = self.get_method_by_event_name(event_name)
        return method(**kwargs)

    def _request(self, url, method='get', payload=None, **kwargs):
        no_answer = True
        attempt_request_limit = 5
        request_count = 0
        request_method = getattr(requests, method)

        while no_answer:
            if method.lower() == 'post':
                resp = request_method(url, data=payload, **kwargs)
            else:
                resp = request_method(url, **kwargs)

            request_count += 1

            if resp.status_code in (200, 201):
                no_answer = False
            elif (resp.status_code in (502, 503, 504, 521, 522, 523, 524)
                  and request_count < attempt_request_limit):
                time.sleep(5)
            else:
                try:
                    errors = resp.json()
                except Exception:
                    errors = resp.text

                raise Exception('{}: {}'.format(resp.status_code, errors))

        return resp
