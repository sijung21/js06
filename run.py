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
import multiprocessing as mp
from multiprocessing import Queue, Process

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QGuiApplication

from src.video_thread_mp import producer
from src.clock import clockclock
from src.js08 import JS08MainWindow
from src.model import JS08Settings


if __name__ == '__main__':
    print(f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    mp.freeze_support()
    q = Queue()
    _q = Queue()

    _producer = producer

    p = Process(name='clock', target=clockclock, args=(q,), daemon=True)
    _p = Process(name='producer', target=_producer, args=(_q,), daemon=True)

    p.start()
    _p.start()

    os.makedirs(f'{JS08Settings.get("data_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS08Settings.get("target_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS08Settings.get("image_save_path")}', exist_ok=True)

    app = QApplication(sys.argv)
    screen_size = QGuiApplication.screens()[0].geometry()
    width, height = screen_size.width(), screen_size.height()
    if width > 1920 or height > 1080:
        QMessageBox.warning(None, 'Warning', 'JS08 is based on FHD screen.')
    window = JS08MainWindow(q, _q)
    sys.exit(app.exec())
