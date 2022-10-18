#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from resources.thumbnail_view import Ui_MainWindow
from model import JS08Settings


class ThumbnailView(QMainWindow, Ui_MainWindow):

    def __init__(self, image_file_name: str, date: int):
        super().__init__()

        self.setupUi(self)
        front_image = f'{JS08Settings.get("image_save_path")}/vista/{JS08Settings.get("front_camera_name")}/' \
                      f'{date}/{image_file_name}.png'
        rear_image = f'{JS08Settings.get("image_save_path")}/vista/{JS08Settings.get("rear_camera_name")}/' \
                     f'{date}/{image_file_name}.png'

        print(front_image)
        print(rear_image)

        if os.path.isfile(front_image) and os.path.isfile(rear_image):
            self.front_image.setPixmap(
                QPixmap(front_image).scaled(self.width(), self.height(), Qt.KeepAspectRatio))
            self.rear_image.setPixmap(
                QPixmap(rear_image).scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        else:
            print('no file')
