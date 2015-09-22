# -*- coding: utf-8 -*-

import cv2
import requests
import time
import threading

from lib.config import *
from lib.capture import *
from lib.gamestart import *
from lib.gameresult import *

config = Config()
cap = Capture.apply(config)

def capture():
    context = {}
    scenes = [GameStart(config), GameResult(config)]
    while cap.is_opened():
        ret, frame = cap.read()

        for scene in scenes:
            if scene.match(frame, context):
                while scene.wait():
                    ret, frame = cap.read()
                scene.execute(frame, context)
                print context
                break

def main():
    thread_capture = threading.Thread(target = capture)
    thread_capture.setDaemon(True)
    thread_capture.start()

    while cap.is_opened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('preview', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
