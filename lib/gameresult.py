# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import tesseract
import utils


class GameResult(object):
    WIN_RECT = (656, 42, 116, 38)
    WIN = cv2.imread('./templates/results/win.png', cv2.IMREAD_GRAYSCALE)
    LOSE_RECT = (656, 374, 116, 38)
    LOSE = cv2.imread('./templates/results/lose.png', cv2.IMREAD_GRAYSCALE)
    NUMBERS = [cv2.imread(
        './templates/numbers/binarized/' + str(x) + '.png',
        cv2.IMREAD_GRAYSCALE
    ) for x in xrange(10)]

    def __init__(self, config):
        self.DEBUG = config.DEBUG
        self.first_match = 0

    def match(self, img, context):
        win = utils.match_binary(img, self.WIN_RECT, 250, 255, self.WIN)
        lose = utils.match_binary(img, self.LOSE_RECT, 250, 255, self.LOSE)
        if win and lose and self.first_match == 0:
            self.first_match = time.time()
            return True

    def wait(self):
        return time.time() - self.first_match < 1

    def execute(self, img, context):
        self.first_match = 0
        summary = self.summary(img, context.get('gachi', False))
        context['members'] = summary
        time.sleep(5)

    def summary(self, img, is_gachi):
        kills = self.kills(img)
        deaths = self.deaths(img)
        udemaes = self.udemaes(img, is_gachi)
        players = self.players(img)
        members = []
        zipped = zip(xrange(8), udemaes, kills, deaths, players)
        for i, udemae, kill, death, player in zipped:
            team = 'win' if i < 4 else 'lose'
            member = {'udemae': udemae, 'kill': kill,
                      'death': death, 'isPlayer': player, 'team': team}
            members.append(member)
        return members

    def kills(self, img):
        return self._kds(img, [102, 167, 232, 297, 432, 497, 562, 627])

    def deaths(self, img):
        return self._kds(img, [123, 188, 253, 318, 453, 518, 583, 648])

    def players(self, img):
        X, Y, W, H = (616, [102, 167, 232, 297, 432, 497, 562, 627], 36, 36)
        imgs = [img[y:y + H, X:X + W] for y in Y]
        white_areas = [self._white_area(img) for img in imgs]
        return [bool(area == max(white_areas)) for area in white_areas]

    def udemaes(self, img, is_gachi):
        if is_gachi:
            X, Y, W, H = (
                1027, [102, 167, 232, 297, 432, 497, 562, 627], 53, 36)
            imgs = [img[y:y + H, X:X + W] for y in Y]
            return [self._udemae(img) for img in imgs]
        else:
            return ['' for x in xrange(8)]

    def _kds(self, img, Y):
        X0, X1, W, H, = (1187, 1202, 12, 18)
        return [
            10 * self._digit(img[y:y + H, X0:X0 + W]) +
            1 * self._digit(img[y:y + H, X1:X1 + W])
            for y in Y
        ]

    def _digit(self, img):
        bin = utils.binary(img, None, 240, 255)
        if bin.sum() < 10:
            return 0
        dist = [(bin - number).sum() for number in self.NUMBERS]
        return dist.index(min(dist))

    def _white_area(self, img):
        bin = utils.binary(img, None, 240, 255)
        return bin.sum()

    def _udemae(self, img):
        img = self._erode(utils.binary(img, None, 240, 255))

        api = tesseract.TessBaseAPI()
        api.Init("C:\Program Files (x86)\Tesseract-OCR",
                 "eng", tesseract.OEM_DEFAULT)
        api.SetVariable("tessedit_char_whitelist", "SABC+-")
        api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)

        ipl_img = self._ipl_image(img)
        tesseract.SetCvImage(ipl_img, api)
        udemae = api.GetUTF8Text().split("\n")[0]
        return udemae

    def _erode(self, img):
        kernel = np.ones((4, 4), np.uint8)
        return cv2.erode(img, kernel, iterations=1)

    def _ipl_image(self, img):
        ipl_img = cv2.cv.CreateImageHeader(
            (img.shape[1], img.shape[0]), cv2.cv.IPL_DEPTH_8U, 1)
        cv2.cv.SetData(ipl_img, img.tostring())
        return ipl_img
