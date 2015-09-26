# -*- coding: utf-8 -*-

import cv2
import utils


class GameStart(object):
    interval_time = 4

    GACHI_LABELS = ['ガチエリア', 'ガチヤグラ', 'ガチホコ']
    RULE_NAMES = ['nawabari', 'area', 'yagura', 'hoko']
    RULE_LABELS = ['ナワバリバトル', 'ガチエリア', 'ガチヤグラ', 'ガチホコ']
    STAGE_NAMES = [
        'dekaline', 'sionome', 'bbus', 'hakofugu', 'alowana',
        'hokke', 'mozuku', 'negitoro', 'tachiuo', 'mongara',
        'hirame', 'masaba'
    ]
    STAGE_LABELS = [
        'デカライン高架下', 'シオノメ油田', 'Bバスパーク', 'ハコフグ倉庫', 'アロワナモール',
        'ホッケふ頭', 'モズク農園', 'ネギトロ炭鉱', 'タチウオパーキング', 'モンガラキャンプ場',
        'ヒラメが丘団地', 'マサバ海峡大橋'
    ]

    def __init__(self, config):
        self.DEBUG = config.DEBUG
        self.RULES = self._load('rules/', self.RULE_NAMES, '.png')
        self.STAGES = self._load('stages/', self.STAGE_NAMES, '.png')

    def match(self, img, context):
        return self._rule(img) and self._stage(img)

    def execute(self, img, context):
        rule = self._rule(img)
        if rule is not None:
            context['rule'] = self.RULE_LABELS[rule]
            context['gachi'] = self._is_gachi(context)

        stage = self._stage(img)
        if stage is not None:
            context['stage'] = self.STAGE_LABELS[stage]

    def _rule(self, img):
        return self._match(img, (489, 250, 300, 60), self.RULES)

    def _stage(self, img):
        return self._match(img, (811, 582, 420, 60), self.STAGES)

    def _is_gachi(self, context):
        return context.get('rule') in self.GACHI_LABELS

    def _load(self, prefix, names, postfix):
        return [cv2.imread(
            './templates/' + prefix + name + postfix,
            cv2.IMREAD_GRAYSCALE
        ) for name in names]

    def _match(self, img, rect, templates):
        D = 255 * rect[2] * rect[3]
        bin = utils.binary(img, rect, 240, 255)
        norm = [cv2.norm(bin, tpl, cv2.NORM_L1) / D for tpl in templates]
        score = min(norm)
        if score > 0.05:
            return None
        else:
            return norm.index(score)
