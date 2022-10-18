# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'thumbnail_view.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1035, 816)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(400, 300))
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        MainWindow.setStyleSheet(u"background-color:rgb(22,32,42);\n"
"border-color: rgb(255, 255, 255);")
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionsd = QAction(MainWindow)
        self.actionsd.setObjectName(u"actionsd")
        self.actionkm = QAction(MainWindow)
        self.actionkm.setObjectName(u"actionkm")
        self.actionkm.setCheckable(True)
        self.actionkm.setEnabled(True)
        self.actionmi = QAction(MainWindow)
        self.actionmi.setObjectName(u"actionmi")
        self.actionmi.setCheckable(True)
        self.actionmi.setEnabled(True)
        self.actionInference = QAction(MainWindow)
        self.actionInference.setObjectName(u"actionInference")
        self.actionInference.setCheckable(True)
        self.actionInference.setChecked(False)
        self.actionEdit_Target = QAction(MainWindow)
        self.actionEdit_Target.setObjectName(u"actionEdit_Target")
        self.actionEdit_Target.setCheckable(False)
        self.actionEdit_Camera = QAction(MainWindow)
        self.actionEdit_Camera.setObjectName(u"actionEdit_Camera")
        self.actionEdit_Camera.setEnabled(True)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionConfiguration = QAction(MainWindow)
        self.actionConfiguration.setObjectName(u"actionConfiguration")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 2, 0, 0)
        self.label_horizontalLayout = QHBoxLayout()
        self.label_horizontalLayout.setSpacing(2)
        self.label_horizontalLayout.setObjectName(u"label_horizontalLayout")
        self.label_horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.front_label = QLabel(self.centralwidget)
        self.front_label.setObjectName(u"front_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.front_label.sizePolicy().hasHeightForWidth())
        self.front_label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        font1.setPointSize(17)
        font1.setBold(False)
        self.front_label.setFont(font1)
        self.front_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: rgb(255, 255, 255);")
        self.front_label.setAlignment(Qt.AlignCenter)

        self.label_horizontalLayout.addWidget(self.front_label)

        self.rear_label = QLabel(self.centralwidget)
        self.rear_label.setObjectName(u"rear_label")
        sizePolicy1.setHeightForWidth(self.rear_label.sizePolicy().hasHeightForWidth())
        self.rear_label.setSizePolicy(sizePolicy1)
        self.rear_label.setFont(font1)
        self.rear_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: rgb(255, 255, 255);")
        self.rear_label.setAlignment(Qt.AlignCenter)

        self.label_horizontalLayout.addWidget(self.rear_label)


        self.verticalLayout.addLayout(self.label_horizontalLayout)

        self.image_horizontalLayout = QHBoxLayout()
        self.image_horizontalLayout.setSpacing(2)
        self.image_horizontalLayout.setObjectName(u"image_horizontalLayout")
        self.front_image = QLabel(self.centralwidget)
        self.front_image.setObjectName(u"front_image")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.front_image.sizePolicy().hasHeightForWidth())
        self.front_image.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setPointSize(20)
        self.front_image.setFont(font2)
        self.front_image.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.front_image.setAlignment(Qt.AlignCenter)

        self.image_horizontalLayout.addWidget(self.front_image)

        self.rear_image = QLabel(self.centralwidget)
        self.rear_image.setObjectName(u"rear_image")
        sizePolicy2.setHeightForWidth(self.rear_image.sizePolicy().hasHeightForWidth())
        self.rear_image.setSizePolicy(sizePolicy2)
        self.rear_image.setFont(font2)
        self.rear_image.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.rear_image.setAlignment(Qt.AlignCenter)

        self.image_horizontalLayout.addWidget(self.rear_image)


        self.verticalLayout.addLayout(self.image_horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"JS-08", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(tooltip)
        self.actionExit.setToolTip(QCoreApplication.translate("MainWindow", u"Exit", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionExit.setStatusTip(QCoreApplication.translate("MainWindow", u"Exit JS-06", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.actionsd.setText(QCoreApplication.translate("MainWindow", u"sd", None))
        self.actionkm.setText(QCoreApplication.translate("MainWindow", u"km", None))
        self.actionmi.setText(QCoreApplication.translate("MainWindow", u"mi", None))
        self.actionInference.setText(QCoreApplication.translate("MainWindow", u"Inference", None))
#if QT_CONFIG(shortcut)
        self.actionInference.setShortcut(QCoreApplication.translate("MainWindow", u"I", None))
#endif // QT_CONFIG(shortcut)
        self.actionEdit_Target.setText(QCoreApplication.translate("MainWindow", u"Edit &Target", None))
        self.actionEdit_Camera.setText(QCoreApplication.translate("MainWindow", u"Edit &Camera Info", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionConfiguration.setText(QCoreApplication.translate("MainWindow", u"Con&figuration", None))
        self.front_label.setText(QCoreApplication.translate("MainWindow", u"Front", None))
        self.rear_label.setText(QCoreApplication.translate("MainWindow", u"Rear", None))
        self.front_image.setText(QCoreApplication.translate("MainWindow", u"No file", None))
        self.rear_image.setText(QCoreApplication.translate("MainWindow", u"No file", None))
    # retranslateUi

