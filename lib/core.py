# -*- coding: utf-8 -*-

from config import *
from capture import *
from gamestart import *
from gameresult import *
from report import *


class Core(object):
    config = Config()
    capture = Capture.apply(config)
    steps = [GameStart(config), GameResult(config), Report(config)]
    context = {}

    def __init__(self):
        pass

    def execute(self):
        while self.capture.is_opened():
            ret, frame = self.capture.read()
            for step in self.steps:
                name = step.__class__.__name__
                if step.match(frame, self.context):
                    print "match: ", name
                    while step.wait():
                        ret, frame = self.capture.read()
                        print "wait: ", name
                    print "execute: ", name
                    step.execute(frame, self.context)
                    print "context: ", self.context
                    break

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
