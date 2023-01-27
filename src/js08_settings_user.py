#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

from PySide6.QtWidgets import QDialog, QFileDialog, QLineEdit, QMessageBox
from PySide6.QtGui import QIcon

from model import JS08Settings
from resources.user_menu import Ui_Dialog

import warnings

warnings.filterwarnings('ignore')


class JS08UserSettingWidget(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('JS08_Logo.ico'))

        self.data_csv_path_button.clicked.connect(self.data_csv_path)
        self.target_csv_path_button.clicked.connect(self.target_csv_path)
        self.image_save_path_button.clicked.connect(self.image_save_path)

        self.data_csv_path_textBrowser.setPlainText(JS08Settings.get('data_csv_path'))
        self.target_csv_path_textBrowser.setPlainText(JS08Settings.get('target_csv_path'))
        self.image_save_path_textBrowser.setPlainText(JS08Settings.get('image_save_path'))

        self.vis_limit_spinBox.setValue(JS08Settings.get('visibility_alert_limit'))
        self.id_lineEdit.setText(JS08Settings.get('current_id'))
        self.current_pw.setEchoMode(QLineEdit.Password)
        self.new_pw.setEchoMode(QLineEdit.Password)
        self.new_pw_check.setEchoMode(QLineEdit.Password)

        self.image_size_comboBox.setCurrentIndex(JS08Settings.get('image_size'))

        self.buttonBox.accepted.connect(self.accept_click)
        self.buttonBox.rejected.connect(self.reject_click)
        self.resize(417, 516)

    def data_csv_path(self):
        fName = QFileDialog.getExistingDirectory(
            self, 'Select path to save data csv file', JS08Settings.get('data_csv_path'))
        if fName:
            self.data_csv_path_textBrowser.setPlainText(fName)
        else:
            pass

    def target_csv_path(self):
        fName = QFileDialog.getExistingDirectory(
            self, 'Select path to save target csv file', JS08Settings.get('target_csv_path'))
        if fName:
            self.target_csv_path_textBrowser.setPlainText(fName)
        else:
            pass

    def image_save_path(self):
        fName = QFileDialog.getExistingDirectory(
            self, 'Select path to save image file', JS08Settings.get('image_save_path'))
        if fName:
            self.image_save_path_textBrowser.setPlainText(fName)
        else:
            pass

    def accept_click(self):
        # print(f'user pw: {JS08Settings.get_user("user_pw")}')
        current_id = JS08Settings.get('current_id')

        user_id = list(JS08Settings.get_user('user').keys())
        user_pw = list(JS08Settings.get_user('user').values())
        user_index = user_id.index(current_id)

        input_current_pw = self.current_pw.text()
        input_new_pw = self.new_pw.text()
        input_new_pw_check = self.new_pw_check.text()

        if input_current_pw == JS08Settings.get('current_pw') and \
                input_new_pw == input_new_pw_check:
            user_pw[user_index] = input_new_pw

            JS08Settings.set('data_csv_path', self.data_csv_path_textBrowser.toPlainText())
            JS08Settings.set('target_csv_path', self.target_csv_path_textBrowser.toPlainText())
            JS08Settings.set('image_save_path', self.image_save_path_textBrowser.toPlainText())
            JS08Settings.set('image_size', self.image_size_comboBox.currentIndex())
            JS08Settings.set('visibility_alert_limit', self.vis_limit_spinBox.value())
            JS08Settings.set('user_pw', user_pw)
            JS08Settings.set('current_pw', input_new_pw)
            # print(f'user pw: {JS08Settings.get_user("user_pw")}')
            # print(f'current user pw: {JS08Settings.get("current_user_pw")}')

            self.close()

        else:
            QMessageBox.warning(self, 'Warning', 'Password Error')

    def reject_click(self):
        self.close()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = JS08UserSettingWidget()
    ui.show()
    sys.exit(app.exec())
