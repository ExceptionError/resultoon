# -*- coding: utf-8 -*-

import cv2
import utils


class Tyoshi(object):
    interval_time = 5

    FRAME = cv2.imread('./templates/tyoshi/frame.png', cv2.IMREAD_GRAYSCALE)
    FRAME_RECT = (314, 184, 68, 40)
    NUM_RECT = (464, 200, 60, 16)

    def __init__(self, config):
        self.DEBUG = config.DEBUG

    def match(self, img, context):
        return utils.match_binary(img, self.FRAME_RECT, 90, 255, self.FRAME)

    def execute(self, img, context):
        gray = utils.gray(utils.crop(img, self.NUM_RECT))
        type = cv2.THRESH_BINARY | cv2.THRESH_OTSU
        ret, bin = cv2.threshold(gray, 60, 255, type)
        #cv2.imshow('tyoshi', bin)
        #cv2.waitKey(1)

        context.clear()
        context['tyoshi'] = utils.text(bin, "+0123456789")
