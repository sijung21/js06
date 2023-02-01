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
        self.front_image_path = f'{JS08Settings.get("image_save_path")}/vista/{JS08Settings.get("front_camera_name")}/' \
                                f'{date}/{image_file_name}.png'
        self.rear_image_path = f'{JS08Settings.get("image_save_path")}/vista/{JS08Settings.get("rear_camera_name")}/' \
                               f'{date}/{image_file_name}.png'

        if os.path.isfile(self.front_image_path) and os.path.isfile(self.rear_image_path):
            print(self.size())
            print(self.front_image.size())
            self.front_image.setPixmap(
                # QPixmap(self.front_image_path).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
                QPixmap(self.front_image_path).scaled(1035, 816, Qt.IgnoreAspectRatio))
            self.rear_image.setPixmap(
                QPixmap(self.rear_image_path).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        else:
            print('no file')


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = ThumbnailView('20230130083300', 230130)
    ui.show()
    sys.exit(app.exec())
