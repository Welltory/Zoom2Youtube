# -*- coding: utf-8 -*-

import requests

from settings import GOOGLE_CODE, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
GRANT_TYPE = 'authorization_code'


def get_token(url, code, client_id, client_secret, redirect_uri, grant_type):
    assert code, "Not found GOOGLE_CODE"
    assert client_id, "Not found GOOGLE_CLIENT_ID"
    assert client_secret, "Not found GOOGLE_CLIENT_SECRET"

    payload = dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type
    )
    response = requests.post(url, data=payload)
    return response.status_code, response.json()


if __name__ == '__main__':
    status, data = get_token(
        TOKEN_URL,
        GOOGLE_CODE,
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        REDIRECT_URI,
        GRANT_TYPE
    )
    if status == 200:
        print('Your token:\n{}\n'.format(data.get('refresh_token')))
    else:
        print('Error: {}\nDescription: {}'.format(
            data.get('error'), data.get('error_description'))
        )
