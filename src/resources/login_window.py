# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(290, 300)
        Dialog.setStyleSheet(u"background-color:rgb(22,32,42);")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridWidget = QWidget(Dialog)
        self.gridWidget.setObjectName(u"gridWidget")
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        self.gridWidget.setFont(font)
        self.gridWidget.setStyleSheet(u"background-color:rgb(27,49,70);")
        self.gridLayout_2 = QGridLayout(self.gridWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.id_lineEdit = QLineEdit(self.gridWidget)
        self.id_lineEdit.setObjectName(u"id_lineEdit")
        self.id_lineEdit.setFont(font)
        self.id_lineEdit.setStyleSheet(u"background-color: #ffffff;")

        self.gridLayout_2.addWidget(self.id_lineEdit, 2, 0, 1, 1)

        self.alert_label = QLabel(self.gridWidget)
        self.alert_label.setObjectName(u"alert_label")
        self.alert_label.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alert_label.sizePolicy().hasHeightForWidth())
        self.alert_label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR Medium"])
        font1.setPointSize(10)
        self.alert_label.setFont(font1)
        self.alert_label.setStyleSheet(u"color:#ff0000;")
        self.alert_label.setFrameShadow(QFrame.Plain)
        self.alert_label.setTextFormat(Qt.AutoText)
        self.alert_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.alert_label, 5, 0, 1, 1)

        self.pw_lineEdit = QLineEdit(self.gridWidget)
        self.pw_lineEdit.setObjectName(u"pw_lineEdit")
        self.pw_lineEdit.setFont(font)
        self.pw_lineEdit.setStyleSheet(u"background-color: #ffffff;")
        self.pw_lineEdit.setEchoMode(QLineEdit.Password)

        self.gridLayout_2.addWidget(self.pw_lineEdit, 3, 0, 1, 1)

        self.sijunglogo = QPushButton(self.gridWidget)
        self.sijunglogo.setObjectName(u"sijunglogo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sijunglogo.sizePolicy().hasHeightForWidth())
        self.sijunglogo.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u"asset/f_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.sijunglogo.setIcon(icon)
        self.sijunglogo.setIconSize(QSize(170, 90))
        self.sijunglogo.setCheckable(False)
        self.sijunglogo.setAutoDefault(False)
        self.sijunglogo.setFlat(True)

        self.gridLayout_2.addWidget(self.sijunglogo, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.gridWidget, 0, 0, 1, 1)

        self.login_button = QPushButton(Dialog)
        self.login_button.setObjectName(u"login_button")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setBold(True)
        self.login_button.setFont(font2)
        self.login_button.setStyleSheet(u"background-color:rgb(27,49,70);color:#ffffff;")

        self.gridLayout.addWidget(self.login_button, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.sijunglogo.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Login", None))
        self.id_lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"ID", None))
        self.alert_label.setText("")
        self.pw_lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Password", None))
        self.sijunglogo.setText("")
        self.login_button.setText(QCoreApplication.translate("Dialog", u"Login", None))
    # retranslateUi

