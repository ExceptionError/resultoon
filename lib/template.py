# -*- coding: utf-8 -*-

import cv2

RIGHTUP = cv2.imread('./templates/result_upright_binary.bmp', cv2.IMREAD_GRAYSCALE)

NUMBERS = []
for x in xrange(10):
    img = cv2.imread('./templates/numbers/binarized/' + str(x) + '.png', cv2.IMREAD_GRAYSCALE)
    ret, binary_img = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    NUMBERS.append(binary_img)

RULE_NAMES = ['none', 'nawabari', 'area', 'yagura', 'hoko']
RULES = [cv2.imread('./templates/rules/' + name + '.png', cv2.IMREAD_GRAYSCALE) for name in RULE_NAMES]
RULE_LABELS = ['', 'ナワバリバトル', 'ガチエリア', 'ガチヤグラ', 'ガチホコ']

STAGE_NAMES = ['none', 'dekaline', 'sionome', 'bbus', 'hakofugu', 'alowana', 'hokke',
                'mozuku', 'negitoro', 'tachiuo', 'mongara', 'hirame', 'masaba']
STAGES = [cv2.imread('./templates/stages/' + name + '.png', cv2.IMREAD_GRAYSCALE) for name in STAGE_NAMES]
STAGE_LABELS = ['', 'デカライン高架下', 'シオノメ油田', 'Bバスパーク', 'ハコフグ倉庫', 'アロワナモール', 'ホッケふ頭',
                'モズク農園', 'ネギトロ炭鉱', 'タチウオパーキング', 'モンガラキャンプ場', 'ヒラメが丘団地', 'マサバ海峡大橋']

def is_gachi(label):
    return label in ['ガチエリア', 'ガチヤグラ', 'ガチホコ']
