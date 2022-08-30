#!/usr/bin/env python3
#
# Copyright 2021-2022 9th grade 5th class.
#
# Authors:
#     5jx2oh@gmail.com

import os
import psutil
import shutil

from PySide6.QtWidgets import (QDialog, QApplication, QMessageBox)

from model import JS08Settings
from resources.auto_file_delete import Ui_Form


def byte_transform(bytes, to, bsize=1024):
    """
    Unit conversion of byte received from shutil

    :return: Capacity of the selected unit (int)
    """
    unit = {'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4}
    r = float(bytes)
    for i in range(unit[to]):
        r = r / bsize
    return int(r)


class FileAutoDelete(QDialog, Ui_Form):

    def __init__(self):
        super().__init__()

        # ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        #                        "resources/auto_file_delete.ui")
        # uic.loadUi(ui_path, self)
        self.setupUi(self)

        # self.setFixedSize(self.width(), self.height())

        drive = []
        # Save all of the user's drives in drive variable.
        for i in range(len(psutil.disk_partitions())):
            drive.append(str(psutil.disk_partitions()[i])[18:19])

        self.calendarWidget.activated.connect(self.showDate)

        self.path = None
        self.date = None
        self.date_convert = None

        self.exit_pushButton.clicked.connect(self.exit_click)

    def exit_click(self):
        self.close()

    def showDate(self, date):
        self.date = date.toString('yyMMdd')
        self.date_convert = date.toString('yyyy/MM/dd')
        self.check_file_date(os.path.join(JS08Settings.get('image_save_path'), 'vista',
                                          JS08Settings.get('front_camera_name')))

    def check_file_date(self, path: str):
        is_old = []

        for f in os.listdir(path):
            if int(f) <= int(self.date):
                is_old.append(int(f))

        if is_old:
            dlg = QMessageBox.question(self, 'Warning', f'Delete folder before {self.date_convert} ?',
                                       QMessageBox.Yes | QMessageBox.No)
            if dlg == QMessageBox.Yes:
                self.delete_select_date(path, is_old)
        else:
            QMessageBox.information(self, 'Information', 'There is no data before the selected date.')

    def delete_select_date(self, path: str, folder: list):
        """
        Delete the list containing the folder name

        :param path: Path to proceed with a auto-delete
        :param folder: Data older than the date selected as the calendarWidget
        """

        for i in range(len(folder)):
            a = os.path.join(path, str(folder[i]))
            shutil.rmtree(a)
            print(f'{a} delete complete.')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FileAutoDelete()
    window.show()
    sys.exit(app.exec_())
