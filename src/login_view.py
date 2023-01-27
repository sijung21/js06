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

from PySide6.QtWidgets import QDialog, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from model import JS08Settings
from resources.login_window import Ui_Dialog


class LoginWindow(QDialog, Ui_Dialog):

    def __init__(self):
        super(LoginWindow, self).__init__()

        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()

        self.sijunglogo.setIcon(QIcon('resources/asset/f_logo.png'))
        self.login_button.clicked.connect(self.login_click)
        self.login_button.setShortcut('Return')

        self.admin_id = JS08Settings.get('admin_id')
        self.admin_pw = JS08Settings.get('admin_pw')
        self.user_id = list(JS08Settings.get_user('user').keys())
        self.user_pw = list(JS08Settings.get_user('user').values())
        self.id = [self.admin_id]
        self.id.extend(self.user_id)
        self.pw = [self.admin_pw]
        self.pw.extend(self.user_pw)
        self.account = {}
        for i in range(len(self.id)):
            self.account[self.id[i]] = self.pw[i]
        self.id = list(self.account.keys())
        self.pw = list(self.account.values())

        self.pw_lineEdit.setEchoMode(QLineEdit.Password)

        self.flag = 0

    def login_click(self):
        input_id = self.id_lineEdit.text()
        input_pw = self.pw_lineEdit.text()
        if input_id in self.account.keys() and input_pw == self.account[f'{input_id}']:
            if self.id_lineEdit.text() == 'admin':
                JS08Settings.set('right', 'administrator')
            else:
                JS08Settings.set('right', 'user')
            JS08Settings.set('current_id', self.id_lineEdit.text())
            JS08Settings.set('current_pw', self.pw_lineEdit.text())
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
            sys.exit()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())
