from zoom import ZoomRecording
from youtube import YoutubeRecording
from settings import (
    ZOOM_KEY, ZOOM_SECRET, ZOOM_HOST_ID, ZOOM_EMAIL, ZOOM_PASSWORD, VIDEO_DIR,
    YOUTUBE_REFRESH_TOKEN, YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET
)


if __name__ == '__main__':
    zoom = ZoomRecording(ZOOM_KEY, ZOOM_SECRET, ZOOM_HOST_ID)
    zoom.download_meetings(ZOOM_EMAIL, ZOOM_PASSWORD, VIDEO_DIR)

    youtube = YoutubeRecording(
        YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN
    )
    youtube.uploads_videos()
