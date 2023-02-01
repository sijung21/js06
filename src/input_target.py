#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import sys

from PySide6.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QApplication
from PySide6.QtGui import QIcon


class InputTarget(QDialog):
    def __init__(self, azimuth=''):
        super().__init__()
        self.setWindowTitle('거리 입력')
        self.setWindowIcon(QIcon('resources/asset/logo.png'))

        self.distance = QLineEdit(self)
        self.azimuth = QLineEdit(self)
        self.azimuth.setText(azimuth)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("거리(km)", self.distance)
        layout.addRow("방위", self.azimuth)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return self.distance.text(), self.azimuth.text()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    dialog = InputTarget()
    dialog.show()
    sys.exit(app.exec())
