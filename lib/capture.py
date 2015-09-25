# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pyautogui


class Capture(object):

    def __init__(self):
        pass

    @staticmethod
    def apply(config):
        W, H = (1280, 720)
        if config.CAPTURE_DEVICE:
            return VideoCapture(config.DEVICE_ID, W, H)
        elif config.SCREEN_RECT_DISABLED:
            return ScreenCapture(None, W, H)
        else:
            return ScreenCapture(config.SCREEN_RECT, W, H)


class VideoCapture(Capture):

    def __init__(self, deviceId, width, height):
        super(VideoCapture, self).__init__()
        self.cap = cv2.VideoCapture(deviceId)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    def is_opened(self):
        return self.cap.isOpened()

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()


class ScreenCapture(Capture):

    def __init__(self, bbox, width, height):
        super(ScreenCapture, self).__init__()
        self.bbox = bbox
        self.width = width
        self.height = height
        self._is_opened = True

    def is_opened(self):
        return self._is_opened

    def read(self):
        img = pyautogui.screenshot()
        if self.bbox:
            img = img.crop(self.bbox)
        img = np.asarray(img)
        img = cv2.resize(img, (self.width, self.height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return (self._is_opened, img)

    def release(self):
        self._is_opened = False


class FileCapture(Capture):

    def __init__(self, file):
        super(FileCapture, self).__init__()
        self.img = cv2.imread(file)
        self._is_opened = True

    def is_opened(self):
        return self._is_opened

    def read(self):
        return (self._is_opened, self.img)

    def release(self):
        self._is_opened = False
