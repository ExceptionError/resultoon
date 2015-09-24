# -*- coding: utf-8 -*-

import cv2
import datetime
import numpy as np
import requests
import time
import tesseract

class GameResult(object):
    def __init__(self, config):
        self.DEBUG = config.DEBUG
        self.GOOGLE_APPS_SCRIPT_URL = config.GOOGLE_APPS_SCRIPT_URL

        self.WIN_RECT = (656, 42, 116, 38)
        self.WIN = cv2.imread('./templates/results/win.png', cv2.IMREAD_GRAYSCALE)
        self.LOSE_RECT = (656, 374, 116, 38)
        self.LOSE = cv2.imread('./templates/results/lose.png', cv2.IMREAD_GRAYSCALE)
        self.NUMBERS = [cv2.imread('./templates/numbers/binarized/' + str(x) + '.png', cv2.IMREAD_GRAYSCALE) for x in xrange(10)]

        self.first_match = 0

    def match(self, img, context):
        win = self._match(img, self.WIN_RECT, self.WIN)
        lose = self._match(img, self.LOSE_RECT, self.LOSE)
        if win and lose and self.first_match == 0:
            self.first_match = time.time()
            return True

    def wait(self):
        return time.time() - self.first_match < 1

    def execute(self, img, context):
        self.first_match = 0
        summary = self.summary(img, context.get('gachi', False))
        context['members'] = summary
        self.send_to_google_spreadsheet(context)
        time.sleep(5)
        context.clear()

    def summary(self, img, is_gachi):
        kills = self.kills(img)
        deaths = self.deaths(img)
        udemaes = self.udemaes(img, is_gachi)
        players = self.players(img)
        members = []
        for i, udemae, kill, death, player in zip(xrange(8), udemaes, kills, deaths, players):
            team = 'win' if i < 4 else 'lose'
            member = {'udemae': udemae, 'kill': kill, 'death': death, 'isPlayer': player, 'team': team}
            members.append(member)
        return members

    def kills(self, img):
        return self._kds(img, [102, 167, 232, 297, 432, 497, 562, 627])

    def deaths(self, img):
        return self._kds(img, [123, 188, 253, 318, 453, 518, 583, 648])

    def players(self, img):
        X, Y, W, H = (616, [102, 167, 232, 297, 432, 497, 562, 627], 36, 36)
        imgs = [img[y:y+H, X:X+W] for y in Y]
        white_areas = [self._white_area(img) for img in imgs]
        return [bool(area == max(white_areas)) for area in white_areas]

    def udemaes(self, img, is_gachi):
        if is_gachi:
            X, Y, W, H = (1027, [102, 167, 232, 297, 432, 497, 562, 627], 53, 36)
            imgs = [img[y:y+H, X:X+W] for y in Y]
            return [self._udemae(img) for img in imgs]
        else:
            return ['' for x in xrange(8)]

    def _match(self, img, rect, base):
        X, Y, W, H = rect
        gray = cv2.cvtColor(img[Y:Y + H, X:X + W], cv2.COLOR_BGR2GRAY)
        ret, bin = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
        coef = cv2.matchTemplate(bin, base, cv2.TM_CCOEFF_NORMED)
        return coef[0] > 0.95

    def _kds(self, img, Y):
        X0, X1, W, H, = (1187, 1202, 12, 18)
        return [10 * self._digit(img[y:y+H, X0:X0+W]) + self._digit(img[y:y+H, X1:X1+W]) for y in Y]

    def _digit(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, bin = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        if bin.sum() < 10:
            return 0
        dist = [(bin - number).sum() for number in self.NUMBERS]
        return dist.index(min(dist))

    def _white_area(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        return binary_img.sum()

    def _udemae(self, img):
        img = self._erode(self._binarize(img))

        api = tesseract.TessBaseAPI()
        api.Init("C:\Program Files (x86)\Tesseract-OCR", "eng", tesseract.OEM_DEFAULT)
        api.SetVariable("tessedit_char_whitelist", "SABC+-")
        api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)

        ipl_img = self._ipl_image(img)
        tesseract.SetCvImage(ipl_img, api)
        udemae = api.GetUTF8Text().split("\n")[0]
        return udemae

    def _binarize(self, img):
        if img.shape[2] != 1:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, bin = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return bin

    def _erode(self, img):
        kernel = np.ones((4, 4), np.uint8)
        return cv2.erode(img, kernel, iterations=1)

    def _ipl_image(self, img):
        ipl_img = cv2.cv.CreateImageHeader((img.shape[1], img.shape[0]), cv2.cv.IPL_DEPTH_8U, 1)
        cv2.cv.SetData(ipl_img, img.tostring())
        return ipl_img

    def send_to_google_spreadsheet(self, payload):
        headers = {'content-type': 'application/json'}
        requests.post(self.GOOGLE_APPS_SCRIPT_URL, json=payload, headers=headers)
        print 'Reported'
