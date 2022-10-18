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
from resources.login_window import Ui_Dialog


class LoginWindow(QDialog, Ui_Dialog):

    def __init__(self):
        super(LoginWindow, self).__init__()

        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.show()

        self.login_button.clicked.connect(self.login_click)
        self.login_button.setShortcut('Return')

        self.id = JS08Settings.get('login_id')
        self.pw = JS08Settings.get('login_pw')

        self.flag = 0

    def login_click(self):
        if self.id_lineEdit.text() == self.id and self.pw_lineEdit.text() == self.pw:
            self.close()
        else:
            self.alert_label.setText('ID or P/W is not correct')
            self.flag = self.flag + 1

            if self.flag >= 5:
                self.alert_label.setText('P/W = 1 + 2 + 3 + 4')

                if self.flag > 10:
                    self.close()
                    sys.exit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
