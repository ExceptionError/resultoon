# -*- coding: utf-8 -*-

import ConfigParser

__ini = ConfigParser.SafeConfigParser()
__ini.read('config.ini')

DEBUG = __ini.getboolean('resultoon', 'debug')
CAPTURE_DEVICE = __ini.getboolean('resultoon', 'capture_device')
GOOGLE_APPS_SCRIPT_URL = __ini.get('resultoon', 'google_apps_script_url')

DEVICE_ID = int(__ini.get('device', 'device_id'))
DEVICE_WIDTH = int(__ini.get('device', 'width'))
DEVICE_HEIGHT = int(__ini.get('device', 'height'))

SCREEN_CROP_X = int(__ini.get('screen', 'crop_x'))
SCREEN_CROP_Y = int(__ini.get('screen', 'crop_y'))
SCREEN_CROP_W = int(__ini.get('screen', 'crop_w'))
SCREEN_CROP_H = int(__ini.get('screen', 'crop_h'))
SCREEN_WIDTH = int(__ini.get('screen', 'width'))
SCREEN_HEIGHT = int(__ini.get('screen', 'height'))

PREVIEW_DISPLAY = __ini.getboolean('preview', 'display')
