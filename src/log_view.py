#!/usr/bin/env python3
#
# Copyright 2021-2023 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QFileDialog

from model import JS08Settings
from resources.log_decrypt import Ui_Dialog
from save_log import decrypt_log


class LogView(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('JS08_Logo.ico'))

        self.pushButton.clicked.connect(self.open_file)

    def open_file(self):
        self.textBrowser.clear()
        fname = QFileDialog.getOpenFileName(self, 'Open file', JS08Settings.get('log_path'))
        if fname[0]:
            for v in decrypt_log(fname[0]):
                self.textBrowser.append(v)

    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            if e.key() == Qt.Key_W:
                self.close()

        if e.key() & Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = LogView()
    ui.show()
    sys.exit(app.exec())
