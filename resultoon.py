# -*- coding: utf-8 -*-

import cv2
import requests
import time
import threading

from lib import *

display_info = {}
cap = capture.create(config)


def send_to_google_spreadsheet(payload):
    if 'rule' in payload and template.is_gachi(payload['rule']):
        headers = {'content-type': 'application/json'}
        r = requests.post(config.GOOGLE_APPS_SCRIPT_URL, json=payload, headers=headers)
        print r.content
        print 'Reported'
    else:
        print 'Not GachiMatch'


def draw_info_on_display(frame):
    y = 1
    for item in display_info.items():
        cv2.putText(frame, item[0] + ': ' + str(item[1]), (10, y * 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2, cv2.CV_AA)
        y += 1
    return frame


def view():
    while cap.is_opened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = draw_info_on_display(frame)
        cv2.imshow('preview', frame)
        if cv2.waitKey(1) == 27:
            break


def capture():
    report = dict()
    while cap.is_opened():
        ret, frame = cap.read()
        if not ret:
            break
        display_info['fps'] = cap.fps

        if splatoon.is_opening(frame):
            """ルールとステージの取得"""
            time.sleep(6)
            ret, frame = cap.read()
            if not ret:
                break
            stage_and_rule = splatoon.recognize_stage_and_rule(frame)
            display_info['stage'] = template.STAGE_NAMES[stage_and_rule['stage']]
            display_info['rule'] = template.RULE_NAMES[stage_and_rule['rule']]
            print display_info
            report['stage'] = template.STAGE_LABELS[stage_and_rule['stage']]
            report['rule'] = template.RULE_LABELS[stage_and_rule['rule']]
            continue

        if splatoon.is_result(frame):
            """参加者の成績の取得"""
            time.sleep(1)
            ret, frame = cap.read()
            if not ret:
                break
            members = splatoon.recognize_result_summary(frame)
            print members
            report['members'] = members

            """自分のウデマエとポイントの差分の取得"""
            time.sleep(6)
            ret, frame = cap.read()
            if not ret:
                break
            udemae_point = splatoon.recognize_result_udemae_point(frame)
            print udemae_point
            report['udemae_point'] = udemae_point['udemae_point']
            report['udemae_diff'] = udemae_point['udemae_diff']

            send_to_google_spreadsheet(report)
            result = dict()
            time.sleep(10)
            continue


def start_view():
    thread_view = threading.Thread(target = view)
    thread_view.setDaemon(True)
    thread_view.start()


def main():
    if config.PREVIEW_DISPLAY:
        start_view()

    thread_capture = threading.Thread(target = capture)
    thread_capture.setDaemon(True)
    thread_capture.start()

    while(True):
        input = raw_input()
        if input == "p":
            start_view()
        elif input == "q" or input == "exit":
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
