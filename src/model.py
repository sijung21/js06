#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
from PyQt5.QtCore import (QSettings, QRect)
from PyQt5.QtGui import (QImage)


class JS06Settings:
    settings = QSettings('sijung', 'js06')

    defaults = {
        'data_csv_path': os.path.join('D:\\JS06', 'data'),
        'target_csv_path': os.path.join('D:\\JS06', 'target'),
        'image_save_path': os.path.join('D:\\JS06', 'image'),
        'image_size': 0,
        'visibility_alert_limit': 1000,
        'login_id': 'admin',
        'login_pw': '1234'
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
    def restore_defaults(cls):
        for key, value in cls.defaults.items():
            cls.set(key, value)


class JS06SimpleTarget:

    def __init__(self,
                 label: str, wedge: str, azimuth: float,
                 distance: float, roi: QRect, mask: QImage,
                 input_width: int, input_height: int):
        super().__init__()
        self.label = label
        self.wedge = wedge
        self.azimuth = azimuth
        self.distance = distance
        self.roi = roi

