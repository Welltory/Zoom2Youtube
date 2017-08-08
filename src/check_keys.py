import settings


def check_keys():
    success = True
    for key in ('GOOGLE_REFRESH_TOKEN', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET',
                'GOOGLE_CODE', 'ZOOM_KEY', 'ZOOM_SECRET', 'ZOOM_HOST_ID', 'ZOOM_EMAIL',
                'ZOOM_PASSWORD', 'VIDEO_DIR', 'SLACK_TOKEN', 'SLACK_CHANNEL'):
        value = getattr(settings, key)
        if not value:
            success = False
            print('{:<30} IS NOT FILLED.'.format(key))
        else:
            print('{:<30} OK.'.format(key))

    if success:
        print('Successfully.')


if __name__ == '__main__':
    check_keys()
