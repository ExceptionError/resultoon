# -*- coding: utf-8 -*-

import cv2
import time

class GameStart(object):
    GACHI_LABELS = ['ガチエリア', 'ガチヤグラ', 'ガチホコ']
    RULE_NAMES = ['nawabari', 'area', 'yagura', 'hoko']
    RULE_LABELS = ['ナワバリバトル', 'ガチエリア', 'ガチヤグラ', 'ガチホコ']
    STAGE_NAMES = ['dekaline', 'sionome', 'bbus', 'hakofugu', 'alowana', 'hokke', 'mozuku', 'negitoro', 'tachiuo', 'mongara', 'hirame', 'masaba']
    STAGE_LABELS = ['デカライン高架下', 'シオノメ油田', 'Bバスパーク', 'ハコフグ倉庫', 'アロワナモール', 'ホッケふ頭', 'モズク農園', 'ネギトロ炭鉱', 'タチウオパーキング', 'モンガラキャンプ場', 'ヒラメが丘団地', 'マサバ海峡大橋']

    def __init__(self, config):
        self.DEBUG = config.DEBUG
        self.RULES = self._load('./templates/rules/', self.RULE_NAMES, '.png')
        self.STAGES = self._load('./templates/stages/', self.STAGE_NAMES, '.png')

    def match(self, img, context):
        rule = self.rule(img)
        if rule is not None:
            context['rule'] = self.RULE_LABELS[rule]
            context['gachi'] = self.is_gachi(context)

        stage = self.stage(img)
        if stage is not None:
            context['stage'] = self.STAGE_LABELS[stage]
        return rule and stage

    def wait(self):
        return False

    def execute(self, img, context):
        time.sleep(4)

    def rule(self, img):
        return self._match(img, (489, 250, 300, 60), self.RULES)

    def stage(self, img):
        return self._match(img, (811, 582, 420, 60), self.STAGES)

    def is_gachi(self, context):
        return context.get('rule') in self.GACHI_LABELS

    def _load(self, prefix, names, postfix):
        return [cv2.imread(prefix + name + postfix, cv2.IMREAD_GRAYSCALE) for name in names]

    def _match(self, img, rect, templates):
        X, Y, W, H = rect
        D = 255 * W * H
        gray = cv2.cvtColor(img[Y:Y + H, X:X + W], cv2.COLOR_BGR2GRAY)
        ret, bin = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        norm = [cv2.norm(bin, tpl, cv2.NORM_L1) / D for tpl in templates]
        score = min(norm)
        if score > 0.05:
            return None
        else:
            return norm.index(score)
