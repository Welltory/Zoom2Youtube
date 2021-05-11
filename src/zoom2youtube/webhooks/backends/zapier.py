from webhooks.backends.base import WebHookBase
from settings import ZAPIER_URL


class ZapierClient(WebHookBase):

    def get_url(self, event_name, **kwargs) -> str:
        return ZAPIER_URL

    def get_request_method(self, event_name, **kwargs) -> str:
        return 'post'

    def new_video(self, **kwargs):
        return self.payload
