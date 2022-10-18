# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auto_file_delete.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModal)
        Form.resize(298, 282)
        font = QFont()
        font.setFamilies([u"KoPubWorld\ub3cb\uc6c0\uccb4 Medium"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        Form.setFont(font)
        Form.setCursor(QCursor(Qt.ArrowCursor))
        Form.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.calendarWidget = QCalendarWidget(Form)
        self.calendarWidget.setObjectName(u"calendarWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        self.calendarWidget.setFont(font1)
        self.calendarWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.calendarWidget.setLocale(QLocale(QLocale.Korean, QLocale.SouthKorea))
        self.calendarWidget.setFirstDayOfWeek(Qt.Sunday)
        self.calendarWidget.setGridVisible(True)

        self.verticalLayout_2.addWidget(self.calendarWidget)

        self.exit_pushButton = QPushButton(Form)
        self.exit_pushButton.setObjectName(u"exit_pushButton")
        sizePolicy.setHeightForWidth(self.exit_pushButton.sizePolicy().hasHeightForWidth())
        self.exit_pushButton.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.exit_pushButton.setFont(font2)
        self.exit_pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_pushButton.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.exit_pushButton)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"File delete", None))
#if QT_CONFIG(whatsthis)
        Form.setWhatsThis(QCoreApplication.translate("Form", u"This is this.", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.calendarWidget.setWhatsThis(QCoreApplication.translate("Form", u"Select a date and erase the data before that date", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.exit_pushButton.setWhatsThis(QCoreApplication.translate("Form", u"Exit this window", None))
#endif // QT_CONFIG(whatsthis)
        self.exit_pushButton.setText(QCoreApplication.translate("Form", u"Close", None))
#if QT_CONFIG(shortcut)
        self.exit_pushButton.setShortcut(QCoreApplication.translate("Form", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

