# -*- coding: utf-8 -*-

import cv2
import tesseract


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


def ipl_image(img):
    ipl = cv2.cv.CreateImageHeader(
        (img.shape[1], img.shape[0]),
        cv2.cv.IPL_DEPTH_8U,
        1
    )
    cv2.cv.SetData(ipl, img.tostring())
    return ipl


def tesseract_text(ipl_img, chars):
    path = "C:\Program Files (x86)\Tesseract-OCR"
    api = tesseract.TessBaseAPI()
    api.Init(path, "eng", tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist", chars)
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)
    tesseract.SetCvImage(ipl_img, api)
    return api.GetUTF8Text().split("\n")[0]


def text(img, chars):
    ipl_img = ipl_image(img)
    text = tesseract_text(ipl_img, chars)
    return text
