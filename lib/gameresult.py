# -*- coding: utf-8 -*-

import cv2
import numpy as np
import utils


class GameResult(object):
    wait_time = 1
    interval_time = 5

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

    def match(self, img, context):
        win = utils.match_binary(img, self.WIN_RECT, 250, 255, self.WIN)
        lose = utils.match_binary(img, self.LOSE_RECT, 250, 255, self.LOSE)
        return win and lose

    def execute(self, img, context):
        self.first_match = 0
        context['members'] = self._members(img, context.get('gachi', False))

    def _members(self, img, is_gachi):
        kills = self._kills(img)
        deaths = self._deaths(img)
        udemaes = self._udemaes(img, is_gachi)
        players = self._players(img)
        members = []
        zipped = zip(xrange(8), udemaes, kills, deaths, players)
        for i, udemae, kill, death, player in zipped:
            team = 'win' if i < 4 else 'lose'
            member = {'udemae': udemae, 'kill': kill,
                      'death': death, 'isPlayer': player, 'team': team}
            members.append(member)
        return members

    def _kills(self, img):
        return self._kds(img, [102, 167, 232, 297, 432, 497, 562, 627])

    def _deaths(self, img):
        return self._kds(img, [123, 188, 253, 318, 453, 518, 583, 648])

    def _players(self, img):
        X, W, H = (616, 36, 36)
        Y = [102, 167, 232, 297, 432, 497, 562, 627]
        imgs = [img[y:y + H, X:X + W] for y in Y]
        white_areas = [self._white_area(img) for img in imgs]
        return [bool(area == max(white_areas)) for area in white_areas]

    def _udemaes(self, img, is_gachi):
        if is_gachi:
            X, W, H = (1027, 53, 36)
            Y = [102, 167, 232, 297, 432, 497, 562, 627]
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
        type = cv2.THRESH_BINARY | cv2.THRESH_OTSU
        ret, bin = cv2.threshold(utils.gray(img), 240, 255, type)
        img = self._erode(bin)
        return utils.text(img, "SABC+-")

    def _erode(self, img):
        kernel = np.ones((4, 4), np.uint8)
        return cv2.erode(img, kernel, iterations=1)
