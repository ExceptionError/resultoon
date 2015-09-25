# -*- coding: utf-8 -*-

import ConfigParser


class Config(object):

    def __init__(self):
        _ini = ConfigParser.SafeConfigParser()
        _ini.read('config.ini')

        self.DEBUG = _ini.getboolean('resultoon', 'debug')
        self.CAPTURE_DEVICE = _ini.getboolean('resultoon', 'capture_device')
        self.GOOGLE_APPS_SCRIPT_URL = _ini.get(
            'resultoon', 'google_apps_script_url')
        self.DEVICE_ID = int(_ini.get('device', 'device_id'))

        self.SCREEN_X = x = int(_ini.get('screen', 'crop_x'))
        self.SCREEN_Y = y = int(_ini.get('screen', 'crop_y'))
        self.SCREEN_W = w = int(_ini.get('screen', 'crop_w'))
        self.SCREEN_H = h = int(_ini.get('screen', 'crop_h'))

        self.SCREEN_RECT_DISABLED = (w == 0 or ch == 0)
        self.SCREEN_RECT = (x, y, w, h)
