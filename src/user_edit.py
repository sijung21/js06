#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QMessageBox

from model import JS08Settings
from resources.user_list import Ui_Dialog


class UserEdit(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('JS08_Logo.ico'))
        self.info.clear()

        self.user_dict = {}

        self.user_id_list = list(JS08Settings.get_user('user').keys())
        self.user_pw_list = list(JS08Settings.get_user('user').values())

        self.listWidget.addItems(self.user_id_list)
        self.listWidget.itemClicked.connect(self.itemClicked)
        self.listWidget.clearSelection()

        self.user_id.setReadOnly(True)
        self.user_pw.setReadOnly(True)
        self.user_id.textChanged.connect(self.change_id)
        self.user_pw.textChanged.connect(self.change_pw)

        self.current_user = ['', '']

        self.add_button.clicked.connect(self.add)
        self.delete_button.clicked.connect(self.delete)
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setShortcut('Esc')

        for ide, pw in zip(self.user_id_list, self.user_pw_list):
            self.user_dict[ide] = pw

    def add(self):
        # print(self.user_dict)
        # count = self.listWidget.count() + 1
        for ide, pw in zip(list(self.user_dict.keys()), list(self.user_dict.values())):
            self.user_dict[ide] = pw

        if not 'Add_user' in self.user_dict.keys():
            self.listWidget.addItem('Add_user')
            # self.user_dict[f'user{count}'] = ''
            self.user_dict['Add_user'] = ''
            # print(self.user_dict)
        else:
            pass
        self.listWidget.clearSelection()
        self.info.setText('사용자 추가')

    def delete(self):
        try:
            del self.user_dict[f'{self.listWidget.currentItem().text()}']
            delete = self.listWidget.currentItem().text()
        except AttributeError:
            QMessageBox.information(None, 'Info', '삭제할 유저를 선택하세요.')

        # print('delete:', self.user_dict)
        self.listWidget.takeItem(self.listWidget.currentRow())
        self.listWidget.clearSelection()
        self.user_id.clear()
        self.user_pw.clear()
        self.info.setText(f'{delete} 제거')

    def save(self):
        # print('save:', self.user_dict)
        if not self.listWidget.count() == 0:
            item = self.listWidget.currentItem().text()

            if not self.current_user[0] == '':
                # print(item, self.current_user)
                self.user_dict.__delitem__(item)
                self.user_dict[self.current_user[0]] = self.current_user[1]
                d1 = sorted(self.user_dict.items())
                self.user_dict = dict(d1)

        JS08Settings.set('user', self.user_dict)
        # print(self.user_dict)

        self.listWidget.clearSelection()
        self.listWidget.clear()
        self.listWidget.addItems(self.user_dict.keys())
        self.info.setText('사용자 저장')

    def change_id(self):
        self.current_user[0] = self.user_id.text()
        self.current_user[1] = self.user_pw.text()

    def change_pw(self):
        self.current_user[0] = self.user_id.text()
        self.current_user[1] = self.user_pw.text()

    def itemClicked(self):
        self.user_id.setReadOnly(False)
        self.user_pw.setReadOnly(False)

        item = self.listWidget.currentItem().text()

        if item in list(self.user_dict.keys()):
            self.user_id.setText(list(self.user_dict.keys())[self.listWidget.currentRow()])
            self.user_pw.setText(list(self.user_dict.values())[self.listWidget.currentRow()])
        else:
            self.user_id.setText(item)
            self.user_pw.setText('')

    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            if e.key() == Qt.Key_T:
                self.add()
            if e.key() == Qt.Key_S:
                self.save()
            if e.key() == Qt.Key_W:
                self.close()
            if e.key() == Qt.Key_P:
                print(f'USER DICT: {self.user_dict}')

        if e.modifiers() & Qt.Key_Escape:
            self.close()

    def closeEvent(self, e):
        pass


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = UserEdit()
    ui.show()
    sys.exit(app.exec())
