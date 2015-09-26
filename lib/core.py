# -*- coding: utf-8 -*-

import time
from config import *
from capture import *
from gamestart import *
from gameresult import *
from report import *
from tyoshi import *


class Core(object):
    config = Config()
    capture = Capture.apply(config)
    match_time = {}
    context = {}
    steps = [
        Tyoshi(config),
        GameStart(config),
        GameResult(config),
        Report(config)
    ]

    def __init__(self):
        pass

    def show(self, name):
        while self.capture.is_opened():
            ret, frame = self.capture.read()
            if not ret:
                break
            cv2.imshow(name, frame)
            if cv2.waitKey(1) == 27:
                break
        self.capture.release()
        cv2.destroyAllWindows()

    def execute(self):
        while self.capture.is_opened():
            ret, frame = self.capture.read()
            for step in self.steps:
                name = step.__class__.__name__
                if self._match(step, name, frame):
                    print "match: ", name
                    self.match_time[name] = time.time()
                    frame = self._wait(step, name, frame)
                    print "execute: ", name
                    step.execute(frame, self.context)
                    print self.context
                    break

    def _match(self, step, name, frame):
        if hasattr(step, 'interval_time') and name in self.match_time:
            interval_time = self.match_time[name] + step.interval_time
            if time.time() < interval_time:
                return False
        return step.match(frame, self.context)

    def _wait(self, step, name, frame):
        if hasattr(step, 'wait_time'):
            wait_time = self.match_time[name] + step.wait_time
            while time.time() < wait_time:
                ret, frame = self.capture.read()
        return frame
