#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
import sys

import cv2
import time
import numpy as np
import pandas as pd

from model import JS06Settings
import target_info


def producer(q):
    front_cap_name = 'PNM_9030V'
    rear_cap_name = 'PNM_9022V'

    front_cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
    rear_cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp')

    # if front_cap.isOpened():
    if rear_cap.isOpened() and front_cap.isOpened():
        while True:
            epoch = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            date = epoch[2:8]

            if epoch[-2:] == '00':
                front_target_name, front_left_range, front_right_range, front_distance = \
                    target_info.get_target(front_cap_name)
                rear_target_name, rear_left_range, rear_right_range, rear_distance = \
                    target_info.get_target(rear_cap_name)

                # if len(front_left_range) < 4:
                if len(front_left_range) < 4 and len(rear_left_range) < 4:
                    continue
                else:
                    pass

                image_save_path = JS06Settings.get('image_save_path')
                os.makedirs(f'{image_save_path}/vista/{front_cap_name}/{date}', exist_ok=True)
                os.makedirs(f'{image_save_path}/vista/{rear_cap_name}/{date}', exist_ok=True)
                os.makedirs(f'{image_save_path}/resize/{front_cap_name}/{date}', exist_ok=True)
                os.makedirs(f'{image_save_path}/resize/{rear_cap_name}/{date}', exist_ok=True)

                front_ret, front_frame = front_cap.read()
                rear_ret, rear_frame = rear_cap.read()

                # if not front_ret:
                if not front_ret or not rear_ret:
                    front_cap.release()
                    rear_cap.release()
                    front_cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
                    rear_cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp')
                    print('Found Error; Rebuilding stream')

                visibility_front = target_info.minprint(epoch[:-2], front_left_range, front_right_range,
                                                        front_distance, front_frame, front_cap_name)
                visibility_rear = target_info.minprint(epoch[:-2], rear_left_range, rear_right_range,
                                                       rear_distance, rear_frame, front_cap_name)
                visibility_front = visibility_front
                # visibility_rear = visibility_rear

                q.put(visibility_front)

                # print('*****')
                # print(f'Front Visibility: {format(int(float(visibility_front) * 1000), ",")} m')
                # print(f'Rear Visibility: {format(int(float(visibility_rear) * 1000), ",")} m')

                if JS06Settings.get('image_size') == 0:  # Original size
                    cv2.imwrite(f'{image_save_path}/vista/{front_cap_name}/{date}/{epoch}.png', front_frame)
                    cv2.imwrite(f'{image_save_path}/vista/{rear_cap_name}/{date}/{epoch}.png', rear_frame)

                elif JS06Settings.get('image_size') == 1:  # FHD size
                    front_frame = cv2.resize(front_frame, (1920, 840), interpolation=cv2.INTER_LINEAR)
                    rear_frame = cv2.resize(rear_frame, (1920, 840), interpolation=cv2.INTER_LINEAR)

                    cv2.imwrite(
                        f'{image_save_path}/vista/{front_cap_name}/{date}/{epoch}_{front_cap_name}.png', front_frame)
                    cv2.imwrite(
                        f'{image_save_path}/vista/{rear_cap_name}/{date}/{epoch}_{rear_cap_name}.png', rear_frame)

                front_frame = cv2.resize(front_frame, (315, 131), interpolation=cv2.INTER_NEAREST)  # Thumbnail size
                rear_frame = cv2.resize(rear_frame, (315, 131), interpolation=cv2.INTER_LINEAR)
                cv2.imwrite(
                    f'{image_save_path}/resize/{front_cap_name}/{date}/{epoch}.jpg', front_frame)
                cv2.imwrite(
                    f'{image_save_path}/resize/{rear_cap_name}/{date}/{epoch}.jpg', rear_frame)

                time.sleep(1)
                front_cap.release()
                rear_cap.release()
                front_cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
                rear_cap = cv2.VideoCapture('rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp')

            cv2.destroyAllWindows()
    else:
        print('cap closed')
