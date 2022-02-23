#!/usr/bin/env python3
#
# Copyright 2021-2022 9th grade 5th class.
#
# Authors:
#     5jx2oh@gmail.com

import os
import psutil
import shutil

from PyQt5.QtWidgets import (QDialog, QApplication, QMenuBar,
                             QAction, QFileDialog, QMessageBox,
                             qApp)
from PyQt5.QtCore import QDate
from PyQt5 import uic


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


class FileAutoDelete(QDialog):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "resources/auto_file_delete.ui")
        uic.loadUi(ui_path, self)

        # self.setFixedSize(self.width(), self.height())

        drive = []
        # Save all of the user's drives in drive variable.
        for i in range(len(psutil.disk_partitions())):
            drive.append(str(psutil.disk_partitions()[i])[18:19])

        self.calendarWidget.activated.connect(self.showDate)

        self.path = None
        self.date = None

        self.exit_pushButton.clicked.connect(self.exit_click)

    def exit_click(self):
        self.close()

    def showDate(self, date):
        self.date = date.toString('yyMMdd')
        self.check_file_date(r'D:\JS06\image\vista')    # JS06Setting.get('image_save_path')

    def check_file_date(self, path: str):
        is_old = []

        for f in os.listdir(path):
            if int(f) <= int(self.date):
                is_old.append(int(f))

        if is_old:
            dlg = QMessageBox.question(self, 'Warning', f'Delete {is_old} folder?',
                                       QMessageBox.Yes | QMessageBox.No)
            if dlg == QMessageBox.Yes:
                print('DELETE!!')
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
            # shutil.rmtree(a)
            print(f'{a} delete complete.')

    def delete_oldest_files(self, path: str, minimum_storage_GB=100):
        """
        The main function of this Program
        Find oldest file and proceed with deletion

        :param path: Path to proceed with a auto-delete
        :param minimum_storage_GB: Minimum storage space desired by the user
        """
        is_old = {}

        if minimum_storage_GB >= byte_transform(self.free, 'GB'):

            for f in os.listdir(path):
                i = os.path.join(path, f)
                is_old[f'{i}'] = int(os.path.getctime(i))

            value = list(is_old.values())
            key = {v: k for k, v in is_old.items()}
            old_folder = key.get(min(value))
            print(old_folder)

            try:
                # shutil.rmtree(old_folder)
                self.progressBar.setValue(self.progressBar.value() + 1)
            except IndexError:
                pass

            self.progressBar.setValue(100)

        else:
            print('Already you have enough storage.')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FileAutoDelete()
    window.show()
    sys.exit(app.exec_())
