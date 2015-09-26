# -*- coding: utf-8 -*-

import cv2


def crop(img, rect):
    if rect is not None:
        X, Y, W, H = rect
        return img[Y:Y + H, X:X + W]
    else:
        return img


def gray(img):
    if img.shape[2] != 1:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        return img


def binary(img, rect, thresh, maxval):
    c = crop(img, rect)
    g = gray(c)
    ret, bin = cv2.threshold(g, thresh, maxval, cv2.THRESH_BINARY)
    return bin


def match(img, tpl):
    coef = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
    return coef[0] > 0.95


def match_binary(img, rect, thresh, maxval, tpl):
    return match(binary(img, rect, thresh, maxval), tpl)
