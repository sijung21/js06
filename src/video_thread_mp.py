#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os

import cv2
import time
import numpy as np
import pandas as pd

from model import JS06Settings
import target_info


def producer(q):

    cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')

    if cap.isOpened():
        while True:
            epoch = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            date = epoch[2:8]

            if epoch[-2:] == '00':
                try:
                    target_name, left_range, right_range, distance = target_info.get_target("PNM_9030V")
                    if len(left_range) < 4:
                        continue
                    else:
                        pass

                    image_save_path = JS06Settings.get('image_save_path')
                    os.makedirs(f'{image_save_path}/vista/{date}', exist_ok=True)
                    os.makedirs(f'{image_save_path}/resize/{date}', exist_ok=True)

                    ret, frame = cap.read()
                    if not ret:
                        cap.release()
                        cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
                        print('Found Error; Rebuilding stream')

                    if JS06Settings.get('image_size') == 0:     # Original size
                        cv2.imwrite(f'{image_save_path}/vista/{date}/{epoch}.png', frame)
                    elif JS06Settings.get('image_size') == 1:   # FHD size
                        frame = cv2.resize(frame, (1920, 840), interpolation=cv2.INTER_LINEAR)
                        cv2.imwrite(f'{image_save_path}/vista/{date}/{epoch}.png', frame)
                    frame = cv2.resize(frame, (315, 131), interpolation=cv2.INTER_NEAREST)  # Thumbnail size
                    cv2.imwrite(f'{image_save_path}/resize/{date}/{epoch}.jpg', cv2.resize(frame, (315, 131)))

                    visibility = target_info.minprint(epoch[:-2], left_range, right_range, distance, frame)
                    q.put(visibility)

                    time.sleep(1)
                    cap.release()
                    cap = cv2.VideoCapture("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")

                except:
                    print(traceback.format_exc())
                    cap.release()
                    cap = cv2.VideoCapture("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")

            cv2.destroyAllWindows()
    else:
        print('cap closed')
