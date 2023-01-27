# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_list.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(417, 310)
        Dialog.setStyleSheet(u"background-color:rgb(22,32,42);")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        font = QFont()
        font.setFamilies([u"Noto Sans KR Medium"])
        font.setPointSize(14)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.verticalLayout_3.addWidget(self.listWidget)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.user_id = QLineEdit(Dialog)
        self.user_id.setObjectName(u"user_id")
        self.user_id.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.gridLayout_2.addWidget(self.user_id, 0, 0, 1, 1)

        self.user_pw = QLineEdit(Dialog)
        self.user_pw.setObjectName(u"user_pw")
        self.user_pw.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.gridLayout_2.addWidget(self.user_pw, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.add_button = QPushButton(Dialog)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.add_button)

        self.delete_button = QPushButton(Dialog)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.delete_button)

        self.save_button = QPushButton(Dialog)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.save_button)

        self.cancel_button = QPushButton(Dialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.cancel_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.info = QLabel(Dialog)
        self.info.setObjectName(u"info")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR Medium"])
        font1.setPointSize(10)
        self.info.setFont(font1)
        self.info.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.info.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.info)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"User List", None))
        self.user_id.setPlaceholderText(QCoreApplication.translate("Dialog", u"User ID", None))
        self.user_pw.setPlaceholderText(QCoreApplication.translate("Dialog", u"User Password", None))
        self.add_button.setText(QCoreApplication.translate("Dialog", u"\ucd94\uac00", None))
        self.delete_button.setText(QCoreApplication.translate("Dialog", u"\uc0ad\uc81c", None))
        self.save_button.setText(QCoreApplication.translate("Dialog", u"\uc800\uc7a5", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"\ucde8\uc18c", None))
        self.info.setText(QCoreApplication.translate("Dialog", u"\uc0ac\uc6a9\uc790 \ucd94\uac00", None))
    # retranslateUi

