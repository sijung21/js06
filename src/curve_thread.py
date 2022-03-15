#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

from multiprocessing import Queue

from PyQt5.QtCore import QThread, pyqtSignal


class CurveThread(QThread):
    poped = pyqtSignal(str)

    def __init__(self, _q: Queue = None):
        super().__init__()
        self._run_flag = False
        self.q = _q

    def run(self):

        self._run_flag = True
        while self._run_flag:
            if not self.q.empty():
                visibility = self.q.get()
                self.poped.emit(visibility)
            # shut down capture system

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.quit()
        self.wait()
