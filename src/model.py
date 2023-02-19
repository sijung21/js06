#!/usr/bin/env python3
#
# Copyright 2021-2023 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import os
from PySide6.QtCore import QSettings


class JS08Settings:
    settings = QSettings('sijung', 'js08')

    defaults = {
        'front_camera_name': 'XNP-9300RW_front',
        'front_camera_rtsp': 'rtsp://admin:sijung5520@121.153.143.180/profile2/media.smp',
        'front_main': 'rtsp://admin:sijung5520@121.153.143.180/profile4/media.smp',
        'rear_camera_name': 'XNP-9300RW_rear',
        'rear_camera_rtsp': 'rtsp://admin:sijung5520@121.153.143.180/profile2/media.smp',
        'rear_main': 'rtsp://admin:sijung5520@121.153.143.180/profile4/media.smp',

        'data_csv_path': os.path.join('C:\\JS08', 'data'),
        'target_csv_path': os.path.join('C:\\JS08', 'target'),
        'rgb_csv_path': os.path.join('C:\\JS08', 'rgb'),
        'image_save_path': os.path.join('C:\\JS08', 'image'),
        'log_path': os.path.join('C:\\JS08', 'log'),
        'image_size': 0,
        'visibility_alert_limit': 1000,
        'right': 'administrator',
        'admin_id': 'admin',
        'admin_pw': 'admin',
        'user': {},
        'current_id': '',
        'current_pw': '',
        'login_time': '',
        'login_flag': 0,
        'first_step': True,
        'maxfev_flag': False,
        'maxfev_count': 0,
        'afd': False,
        'log_key': b'',
    }

    @classmethod
    def set(cls, key, value):
        cls.settings.setValue(key, value)

    @classmethod
    def get(cls, key):
        return cls.settings.value(
            key,
            cls.defaults[key],
            type(cls.defaults[key])
        )

    @classmethod
    def get_user(cls, key):
        return cls.settings.value(
            key, cls.defaults[key]
        )

    @classmethod
    def restore_defaults(cls):
        for key, value in cls.defaults.items():
            cls.set(key, value)

    @classmethod
    def restore_value(cls, key):
        if key in cls.defaults.keys():
            cls.set(key, cls.defaults[key])

    @classmethod
    def add_maxfev_time(cls, data: list):
        for i in data:
            cls.settings.setValue('maxfev_time', i)


if __name__ == '__main__':

    JS08Settings.restore_defaults()
    user = JS08Settings.get_user('user')
    # time_ = JS08Settings.get('login_time')
    # print(time_)
    # print(time_[-4])
    # print(type(time_))
    # print(user)
    # user['user1'] = '1111'
    # print(user)
