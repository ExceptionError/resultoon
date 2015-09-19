# -*- coding: utf-8 -*-

import cv2
import datetime
import numpy as np
import tesseract

import config
import template

def get_all_kd(img):
    W = 12
    H = 18
    X = (1187, 1202)
    Y = [102, 167, 232, 297, 432, 497, 562, 627]
    kds = []
    for y in Y:
        kill = dict()
        death = dict()
        kill['10'] = get_digit(img[y:y+H, X[0]:X[0]+W])
        kill['1'] = get_digit(img[y:y+H, X[1]:X[1]+W])
        y2 = y + 21
        death['10'] = get_digit(img[y2:y2+H, X[0]:X[0]+W])
        death['1'] = get_digit(img[y2:y2+H, X[1]:X[1]+W])
        kds.append({'kill': kill['10']*10 + kill['1'], 'death': death['10']*10 + death['1']})
    return kds


def get_digit(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # 画面全体の輝度値合計がほとんど0なら数字なしとみなし、0を返す
    if binary_img.sum() < 10:
        return 0
    dist = [(binary_img - number).sum() for number in template.NUMBERS]
    return dist.index(min(dist))


def get_coef_of_rightup_rect(img):
    cropped_gray_img = cv2.cvtColor(img[0:0+64, 1188:1188+64], cv2.COLOR_BGR2GRAY)
    ret, temp = cv2.threshold(cropped_gray_img, 250, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    coef = cv2.matchTemplate(temp, template.RIGHTUP, cv2.TM_CCOEFF_NORMED)
    return coef[0]


def is_result(img):
    return get_coef_of_rightup_rect(img) > 0.95


def recognize_result_summary(img):
    W = 53
    H = 36
    X = 1027
    Y = [102, 167, 232, 297, 432, 497, 562, 627]
    imgs = [img[y:y+H, X:X+W] for y in Y]
    udemaes = [ocr_udemae(i) for i in imgs]
    kds = get_all_kd(img)
    player_index = identify_player(img)
    members = [{'udemae': udemae, 'kill': kd['kill'], 'death': kd['death']} for udemae, kd in zip(udemaes, kds)]
    members[player_index]['isPlayer'] = True
    for i, m in enumerate(members):
        team = 'win' if i < 4 else 'lose'
        m.update({'team': team})
    return members


def identify_player(img):
    """リザルト画面のメンバーを上から順に0-7番として、プレイヤーに該当する番号を返す"""
    W = 36
    H = 36
    X = 616
    Y = [102, 167, 232, 297, 432, 497, 562, 627]
    imgs = [img[y:y+H, X:X+W] for y in Y]
    white_areas = [calc_white_area(img) for img in imgs]
    return white_areas.index(max(white_areas))


def calc_white_area(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    return binary_img.sum()


def is_opening(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if gray.sum() < 1000000:
        right_down_violet = img[590:690, 1140:1240]
        return right_down_violet.sum() > 100000


def recognize_stage_and_rule(img):
    # rule
    W = 300
    H = 60
    X = 489
    Y = 250
    gray = cv2.cvtColor(img[Y:Y+H, X:X+W], cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    dist = [(binary_img - tpl).sum() for tpl in template.RULES]
    rule = dist.index(min(dist))
    if config.DEBUG:
        save_image(binary_img, './debug/rule_' + template.RULE_NAMES[rule] + '_')

    # stage
    W = 420
    H = 60
    X = 811
    Y = 582
    gray = cv2.cvtColor(img[Y:Y+H, X:X+W], cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    dist = [(binary_img - tpl).sum() for tpl in template.STAGES]
    stage = dist.index(min(dist))
    if config.DEBUG:
        save_image(binary_img, './debug/stage_' + template.STAGE_NAMES[stage] + '_')

    return {'stage': stage, 'rule': rule}


def ocr_udemae(img):
    img = binarize(img)
    img = erode(img)

    api = tesseract.TessBaseAPI()
    api.Init("C:\Program Files (x86)\Tesseract-OCR", "eng", tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist", "SABC+-")
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)

    cv_im = convert_to_IplImage(img)
    tesseract.SetCvImage(cv_im, api)
    udemae = api.GetUTF8Text().split("\n")[0]
    if config.DEBUG:
        save_image(img, './debug/udemae_[' + udemae + ']_')

    return udemae


def ocr_number(img):
    api = tesseract.TessBaseAPI()
    api.Init("C:\Program Files (x86)\Tesseract-OCR", "eng", tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist", "0123456789+-")
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)

    cv_im = convert_to_IplImage(img)
    tesseract.SetCvImage(cv_im, api)
    number = api.GetUTF8Text().split("\n")[0]
    return number


def save_image(img, prefix):
    d = datetime.datetime.today()
    filename = prefix + d.strftime("%Y%m%d_%H%M%S") + ".png"
    cv2.imwrite(filename, img)


def recognize_result_udemae_point(img):
    cropped_img = img[206:206+64, 842:842+96]
    temp = binarize(cropped_img)
    temp = rotate_10_degree(temp)
    temp = erode(temp)
    udemae_diff = ocr_number(temp)
    if config.DEBUG:
        save_image(temp, './debug/diff_[' + udemae_diff + ']_')

    cropped_img = img[382:382+64, 774:774+92]
    temp = binarize(cropped_img)
    temp = erode(temp)
    udemae_point = ocr_number(temp)
    if config.DEBUG:
        save_image(temp, './debug/udemae_[' + udemae_diff + ']_')

    return {"udemae_diff": udemae_diff, "udemae_point": udemae_point}


def convert_to_IplImage(img):
    ipl_img = cv2.cv.CreateImageHeader((img.shape[1], img.shape[0]), cv2.cv.IPL_DEPTH_8U, 1)
    cv2.cv.SetData(ipl_img, img.tostring())
    return ipl_img


def binarize(img):
    if img.shape[2] != 1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_image = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image


def erode(img):
    kernel = np.ones((4, 4), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    return erosion


def rotate_10_degree(img):
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 10, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    return dst
