# -*- coding: utf-8 -*-

import requests

class Report(object):
    keys = ['rule', 'stage', 'members']

    def __init__(self, config):
        self.DEBUG = config.DEBUG
        self.GOOGLE_APPS_SCRIPT_URL = config.GOOGLE_APPS_SCRIPT_URL

    def match(self, img, context):
        return all([key in context for key in self.keys])

    def wait(self):
        return False

    def execute(self, img, context):
        self.send_to_google_spreadsheet(context)
        map(context.pop, self.keys)

    def send_to_google_spreadsheet(self, payload):
        headers = {'content-type': 'application/json'}
        requests.post(self.GOOGLE_APPS_SCRIPT_URL, json=payload, headers=headers)
