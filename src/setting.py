#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
import sys
import time

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

from model import JS08Settings
from resources.rtsp_setting import Ui_Dialog


class Setting(QDialog, Ui_Dialog):

    def __init__(self):
        super(Setting, self).__init__()

        self.setupUi(self)

        self.front_model_lineEdit.setText(JS08Settings.get('front_camera_name'))
        self.front_rtsp_lineEdit.setText(JS08Settings.get('front_camera_rtsp'))
        self.front_resize_rtsp_lineEdit.setText(JS08Settings.get('front_main'))

        self.rear_model_lineEdit.setText(JS08Settings.get('rear_camera_name'))
        self.rear_rtsp_lineEdit.setText(JS08Settings.get('rear_camera_rtsp'))
        self.rear_resize_rtsp_lineEdit.setText(JS08Settings.get('rear_main'))

        self.data_path_lineEdit.setText(JS08Settings.get('data_csv_path'))
        self.target_path_lineEdit.setText(JS08Settings.get('target_csv_path'))
        self.rgb_path_lineEdit.setText(JS08Settings.get('rgb_csv_path'))
        self.image_path_lineEdit.setText(JS08Settings.get('image_save_path'))

        self.buttonBox.accepted.connect(self.accept_click)

    def accept_click(self):
        JS08Settings.set('front_camera_name', self.front_model_lineEdit.text())
        JS08Settings.set('front_camera_rtsp', self.front_rtsp_lineEdit.text())
        JS08Settings.set('front_main', self.front_resize_rtsp_lineEdit.text())

        JS08Settings.set('rear_camera_name', self.rear_model_lineEdit.text())
        JS08Settings.set('rear_camera_rtsp', self.rear_rtsp_lineEdit.text())
        JS08Settings.set('rear_main', self.rear_resize_rtsp_lineEdit.text())

        JS08Settings.set('data_csv_path', self.data_path_lineEdit.text())
        JS08Settings.set('target_csv_path', self.target_path_lineEdit.text())
        JS08Settings.set('rgb_csv_path', self.rgb_path_lineEdit.text())
        JS08Settings.set('image_save_path', self.image_path_lineEdit.text())

        self.close()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = Setting()
    window.show()
    sys.exit(app.exec())
