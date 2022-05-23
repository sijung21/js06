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

from model import JS08Settings
import target_info


def producer(q):
    front_cap_name = 'PNM_9031RV_front'
    rear_cap_name = 'PNM_9031RV_rear'

    front_cap = cv2.VideoCapture(JS08Settings.get('front_camera_rtsp'))
    rear_cap = cv2.VideoCapture(JS08Settings.get('rear_camera_rtsp'))

    if rear_cap.isOpened() and front_cap.isOpened():
        while True:
            epoch = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            date = epoch[2:8]

            if epoch[-2:] == '00':
                front_target_name, front_left_range, front_right_range, front_distance, front_azimuth = \
                    target_info.get_target(front_cap_name)

                rear_target_name, rear_left_range, rear_right_range, rear_distance, rear_azimuth = \
                    target_info.get_target(rear_cap_name)

                front_target_name_W, front_left_range_W, front_right_range_W, front_distance_W, front_azimuth_W = \
                    target_info.get_target_from_azimuth(front_cap_name, 'W')

                front_target_name_NW, front_left_range_NW, front_right_range_NW, front_distance_NW, front_azimuth_NW = \
                    target_info.get_target_from_azimuth(front_cap_name, 'NW')

                front_target_name_N, front_left_range_N, front_right_range_N, front_distance_N, front_azimuth_N = \
                    target_info.get_target_from_azimuth(front_cap_name, 'N')

                front_target_name_NE, front_left_range_NE, front_right_range_NE, front_distance_NE, front_azimuth_NE = \
                    target_info.get_target_from_azimuth(front_cap_name, 'NE')

                front_target_name_E, front_left_range_E, front_right_range_E, front_distance_E, front_azimuth_E = \
                    target_info.get_target_from_azimuth(front_cap_name, 'E')

                rear_target_name_E, rear_left_range_E, rear_right_range_E, rear_distance_E, rear_azimuth_E = \
                    target_info.get_target_from_azimuth(rear_cap_name, 'E')

                rear_target_name_SE, rear_left_range_SE, rear_right_range_SE, rear_distance_SE, rear_azimuth_SE = \
                    target_info.get_target_from_azimuth(rear_cap_name, 'SE')

                rear_target_name_S, rear_left_range_S, rear_right_range_S, rear_distance_S, rear_azimuth_S = \
                    target_info.get_target_from_azimuth(rear_cap_name, 'S')

                rear_target_name_SW, rear_left_range_SW, rear_right_range_SW, rear_distance_SW, rear_azimuth_SW = \
                    target_info.get_target_from_azimuth(rear_cap_name, 'SW')

                rear_target_name_W, rear_left_range_W, rear_right_range_W, rear_distance_W, rear_azimuth_W = \
                    target_info.get_target_from_azimuth(rear_cap_name, 'W')

                if len(front_left_range_W) < 4 and len(rear_left_range_W) < 4:
                    continue
                else:
                    pass

                image_save_path = JS08Settings.get('image_save_path')
                os.makedirs(f'{image_save_path}/vista/{front_cap_name}/{date}', exist_ok=True)
                os.makedirs(f'{image_save_path}/vista/{rear_cap_name}/{date}', exist_ok=True)
                os.makedirs(f'{image_save_path}/resize/{front_cap_name}/{date}', exist_ok=True)
                os.makedirs(f'{image_save_path}/resize/{rear_cap_name}/{date}', exist_ok=True)

                front_ret, front_frame = front_cap.read()
                rear_ret, rear_frame = rear_cap.read()

                if not front_ret or not rear_ret:
                    print('Found Error; Rebuilding stream')

                    front_cap.release()
                    rear_cap.release()
                    front_cap = cv2.VideoCapture(JS08Settings.get('front_camera_rtsp'))
                    rear_cap = cv2.VideoCapture(JS08Settings.get('rear_camera_rtsp'))
                    front_ret, front_frame = front_cap.read()
                    rear_ret, rear_frame = rear_cap.read()

                visibility_front = target_info.minprint(epoch[:-2], front_left_range, front_right_range,
                                                        front_distance, front_frame, front_cap_name)
                visibility_rear = target_info.minprint(epoch[:-2], rear_left_range, rear_right_range,
                                                       rear_distance, rear_frame, rear_cap_name)

                visibility_front_W = target_info.minprint(epoch[:-2], front_left_range_W, front_right_range_W,
                                                          front_distance_W, front_frame, front_cap_name)
                visibility_front_NW = target_info.minprint(epoch[:-2], front_left_range_NW, front_right_range_NW,
                                                           front_distance_NW, front_frame, front_cap_name)
                visibility_front_N = target_info.minprint(epoch[:-2], front_left_range_N, front_right_range_N,
                                                          front_distance_N, front_frame, front_cap_name)
                visibility_front_NE = target_info.minprint(epoch[:-2], front_left_range_NE, front_right_range_NE,
                                                           front_distance_NE, front_frame, front_cap_name)
                visibility_front_E = target_info.minprint(epoch[:-2], front_left_range_E, front_right_range_E,
                                                          front_distance_E, front_frame, front_cap_name)

                visibility_rear_E = target_info.minprint(epoch[:-2], rear_left_range_E, rear_right_range_E,
                                                         rear_distance_E, rear_frame, rear_cap_name)
                visibility_rear_SE = target_info.minprint(epoch[:-2], rear_left_range_SE, rear_right_range_SE,
                                                          rear_distance_SE, rear_frame, rear_cap_name)
                visibility_rear_S = target_info.minprint(epoch[:-2], rear_left_range_S, rear_right_range_S,
                                                         rear_distance_S, rear_frame, rear_cap_name)
                visibility_rear_SW = target_info.minprint(epoch[:-2], rear_left_range_SW, rear_right_range_SW,
                                                          rear_distance_SW, rear_frame, rear_cap_name)
                visibility_rear_W = target_info.minprint(epoch[:-2], rear_left_range_W, rear_right_range_W,
                                                         rear_distance_W, rear_frame, rear_cap_name)

                # print(f'visibility W, NW, N, NE, E - {visibility_front_W, visibility_front_NW, visibility_front_N, visibility_front_NE, visibility_front_E}')
                # print(f'visibility E, SE, S, SW, W - {visibility_rear_E, visibility_rear_SE, visibility_rear_S, visibility_rear_SW, visibility_rear_W}')

                visibility = {'visibility_front': visibility_front, 'visibility_rear': visibility_rear,
                              'front_W': visibility_front_W, 'front_NW': visibility_front_NW,
                              'front_N': visibility_front_N, 'front_NE': visibility_front_NE,
                              'front_E': visibility_front_E, 'rear_E': visibility_rear_E,
                              'rear_SE': visibility_rear_SE, 'rear_S': visibility_rear_S,
                              'rear_SW': visibility_rear_SW, 'rear_W': visibility_rear_W}
                q.put(visibility)

                if JS08Settings.get('image_size') == 0:  # Original size
                    cv2.imwrite(f'{image_save_path}/vista/{front_cap_name}/{date}/{epoch}.png', front_frame)
                    cv2.imwrite(f'{image_save_path}/vista/{rear_cap_name}/{date}/{epoch}.png', rear_frame)

                elif JS08Settings.get('image_size') == 1:  # FHD size
                    front_frame = cv2.resize(front_frame, (1920, 640), interpolation=cv2.INTER_LINEAR)
                    rear_frame = cv2.resize(rear_frame, (1920, 640), interpolation=cv2.INTER_LINEAR)

                    cv2.imwrite(
                        f'{image_save_path}/vista/{front_cap_name}/{date}/{epoch}_{front_cap_name}.png', front_frame)
                    cv2.imwrite(
                        f'{image_save_path}/vista/{rear_cap_name}/{date}/{epoch}_{rear_cap_name}.png', rear_frame)

                front_frame = cv2.resize(front_frame, (393, 105), interpolation=cv2.INTER_NEAREST)  # Thumbnail size
                rear_frame = cv2.resize(rear_frame, (393, 105), interpolation=cv2.INTER_LINEAR)
                cv2.imwrite(
                    f'{image_save_path}/resize/{front_cap_name}/{date}/{epoch}.jpg', front_frame)
                cv2.imwrite(
                    f'{image_save_path}/resize/{rear_cap_name}/{date}/{epoch}.jpg', rear_frame)

                time.sleep(1)
                front_cap.release()
                rear_cap.release()
                front_cap = cv2.VideoCapture(JS08Settings.get('front_camera_rtsp'))
                rear_cap = cv2.VideoCapture(JS08Settings.get('rear_camera_rtsp'))

            cv2.destroyAllWindows()
    else:
        print('cap closed')
