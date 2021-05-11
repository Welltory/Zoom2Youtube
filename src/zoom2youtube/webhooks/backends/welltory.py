from webhooks.backends.zapier import ZapierClient


class WelltoryTeam(ZapierClient):

    def get_data_for_event(self, event_name, **kwargs):
        data = super().get_data_for_event(event_name, **kwargs)
        title = data['result']['name'].split(' ')[0]
        data['result']['title'] = title
        return data

