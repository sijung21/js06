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


def delete_select_date(path: str, folder: list):
    """
    Delete the list containing the folder name

    :param path: Path to proceed with a auto-delete
    :param folder: Data older than the date selected as the calendarWidget
    """

    # for i in range(len(folder)):
    #     a = os.path.join(path, str(folder[i]))
    #     shutil.rmtree(a)
    #     print(f'{a} delete complete.')
    a = os.path.join(path, str(folder[0]))
    print(f'{a} delete complete.')


def check_file_date(path: str):
    is_old = []

    for f in os.listdir(path):
        is_old.append(int(f))
    delete_select_date(path, is_old)


def FileAutoDelete():
    save_disk = JS08Settings.get('image_save_path')[:2]

    total, used, free = shutil.disk_usage(save_disk)
    if JS08Settings.get('afd'):
        if byte_transform(free, 'GB') <= 20:
            check_disk()


def check_disk():
    check_file_date(os.path.join(JS08Settings.get('image_save_path'), 'vista',
                                 JS08Settings.get('front_camera_name')))
    print('-' * 10)
    check_file_date(os.path.join(JS08Settings.get('image_save_path'), 'vista',
                                 JS08Settings.get('rear_camera_name')))


if __name__ == "__main__":
    import sys

    FileAutoDelete()
    # sys.exit(app.exec())
