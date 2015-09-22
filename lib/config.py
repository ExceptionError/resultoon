# -*- coding: utf-8 -*-

import ConfigParser

class Config(object):
    def __init__(self):
        _ini = ConfigParser.SafeConfigParser()
        _ini.read('config.ini')
        self.DEBUG = _ini.getboolean('resultoon', 'debug')
        self.CAPTURE_DEVICE = _ini.getboolean('resultoon', 'capture_device')
        self.GOOGLE_APPS_SCRIPT_URL = _ini.get('resultoon', 'google_apps_script_url')
        self.DEVICE_ID = int(_ini.get('device', 'device_id'))
        self.SCREEN_X = int(_ini.get('screen', 'crop_x'))
        self.SCREEN_Y = int(_ini.get('screen', 'crop_y'))
        self.SCREEN_W = int(_ini.get('screen', 'crop_w'))
        self.SCREEN_H = int(_ini.get('screen', 'crop_h'))
