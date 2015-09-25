# -*- coding: utf-8 -*-

import cv2


def binary(img, rect, thresh, maxval):
    if rect is not None:
        X, Y, W, H = rect
        crop = img[Y:Y + H, X:X + W]
    else:
        crop = img

    if crop.shape[2] != 1:
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    else:
        gray = crop

    ret, bin = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY)
    return bin


def match(img, tpl):
    coef = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
    return coef[0] > 0.95


def match_binary(img, rect, thresh, maxval, tpl):
    return match(binary(img, rect, thresh, maxval), tpl)
