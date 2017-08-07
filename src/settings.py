import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)


YOUTUBE_REFRESH_TOKEN = os.environ.get('YOUTUBE_REFRESH_TOKEN')
YOUTUBE_CLIENT_ID = os.environ.get('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.environ.get('YOUTUBE_CLIENT_SECRET')


ZOOM_KEY = os.environ.get('ZOOM_KEY')
ZOOM_SECRET = os.environ.get('ZOOM_SECRET')
ZOOM_HOST_ID = os.environ.get('ZOOM_HOST_ID')
ZOOM_EMAIL = os.environ.get('ZOOM_EMAIL')
ZOOM_PASSWORD = os.environ.get('ZOOM_PASSWORD')


VIDEO_DIR = 'video'

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
