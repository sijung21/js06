#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

from PySide6.QtCore import QThread, Signal


class Consumer(QThread):
    poped = Signal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            if not self.q.empty():
                data = self.q.get()
                self.poped.emit(data)

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True

    def stop(self):
        self.terminate()