# -*- coding: utf-8 -*-

import os

from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

BASE_DIR = dirname(dirname(os.path.abspath(__file__)))

GOOGLE_REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_CODE = os.environ.get('GOOGLE_CODE')


ZOOM_KEY = os.environ.get('ZOOM_KEY')
ZOOM_SECRET = os.environ.get('ZOOM_SECRET')
ZOOM_HOST_ID = os.environ.get('ZOOM_HOST_ID')
ZOOM_EMAIL = os.environ.get('ZOOM_EMAIL')
ZOOM_PASSWORD = os.environ.get('ZOOM_PASSWORD')


VIDEO_DIR = join(BASE_DIR, 'video')

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
SLACK_CHANNELS_UNIQUE_SETTINGS = {}  # Example: {'lesson_1': ['#main', '#lessons']}

ZAPIER_URL = os.environ.get('ZAPIER_URL')

DOWNLOADED_FILES = join(BASE_DIR, 'downloaded')
LOCK_FILE = join(BASE_DIR, 'lock')


WEBHOOK_BACKEND_PIPELINES = [
    'webhooks.backends.slack.SlackClient',
]

MIN_DURATION = os.environ.get('MIN_DURATION') or 10  # minute

try:
    from local_settings import *
except ImportError:
    pass
