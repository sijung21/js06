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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5 import uic

from model import JS06Settings


class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'resources/login_window.ui')
        uic.loadUi(ui_path, self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.show()

        self.login_button.clicked.connect(self.login_click)
        self.login_button.setShortcut('Return')

        self.id = JS06Settings.get('login_id')
        self.pw = JS06Settings.get('login_pw')

        self.flag = 0

    def login_click(self):
        if self.id_lineEdit.text() == self.id and self.pw_lineEdit.text() == self.pw:
            self.close()
        else:
            self.alert_label.setText('ID or P/W is not correct')
            self.flag = self.flag + 1
            if self.flag >= 5:
                self.alert_label.setText('P/W = 1 + 2 + 3 + 4')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
