import time

from datetime import datetime
from datetime import timedelta

import jwt


def make_http_headers(access_token: str) -> dict:
    return {
        "authorization": "Bearer {}".format(access_token),
        "content-type": "application/json"
    }


def generate_access_token(
        api_key: str,
        api_secret: str,
        token_exp_delta: int
) -> str:
    jwt_payload = make_jwt_payload(api_key, token_exp_delta)
    return generate_jwt_token(jwt_payload, api_secret)


def make_jwt_payload(api_key: str, token_exp_delta: int) -> dict:
    dt = datetime.utcnow() + timedelta(seconds=token_exp_delta)
    exp = int(time.mktime(dt.timetuple()))

    return {
        "iss": api_key,
        "exp": exp
    }


def generate_jwt_token(payload: dict, api_secret: str) -> str:
    encoded = jwt.encode(payload, api_secret, algorithm='HS256')
    if isinstance(encoded, bytes):
        # For PyJWT <= 1.7.1
        return encoded.decode()
    # For PyJWT >= 2.0.0a1
    return encoded
