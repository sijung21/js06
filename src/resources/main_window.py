# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1087, 816)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(400, 300))
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        icon = QIcon()
        icon.addFile(u"logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color:rgb(22,32,42);\n"
"color: rgb(255, 255, 255);")
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
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.monitoring_horizontalLayout = QHBoxLayout()
        self.monitoring_horizontalLayout.setSpacing(0)
        self.monitoring_horizontalLayout.setObjectName(u"monitoring_horizontalLayout")
        self.thumbnail_info_label_2 = QLabel(self.centralwidget)
        self.thumbnail_info_label_2.setObjectName(u"thumbnail_info_label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.thumbnail_info_label_2.sizePolicy().hasHeightForWidth())
        self.thumbnail_info_label_2.setSizePolicy(sizePolicy1)
        self.thumbnail_info_label_2.setMinimumSize(QSize(0, 50))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        font1.setPointSize(30)
        self.thumbnail_info_label_2.setFont(font1)
        self.thumbnail_info_label_2.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: rgb(255, 0, 0);")

        self.monitoring_horizontalLayout.addWidget(self.thumbnail_info_label_2)

        self.logo = QPushButton(self.centralwidget)
        self.logo.setObjectName(u"logo")
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMinimumSize(QSize(0, 50))
        self.logo.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon1 = QIcon()
        icon1.addFile(u"asset/f_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.logo.setIcon(icon1)
        self.logo.setIconSize(QSize(156, 50))
        self.logo.setAutoRepeatDelay(300)
        self.logo.setAutoDefault(True)
        self.logo.setFlat(True)

        self.monitoring_horizontalLayout.addWidget(self.logo)

        self.monitoring_label = QLabel(self.centralwidget)
        self.monitoring_label.setObjectName(u"monitoring_label")
        sizePolicy1.setHeightForWidth(self.monitoring_label.sizePolicy().hasHeightForWidth())
        self.monitoring_label.setSizePolicy(sizePolicy1)
        self.monitoring_label.setMinimumSize(QSize(50, 50))
        font2 = QFont()
        font2.setFamilies([u"FrutigerNeue1450W04-Regular"])
        font2.setPointSize(29)
        self.monitoring_label.setFont(font2)
        self.monitoring_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:rgb(28,136,227);")

        self.monitoring_horizontalLayout.addWidget(self.monitoring_label)

        self.thumbnail_info_label = QLabel(self.centralwidget)
        self.thumbnail_info_label.setObjectName(u"thumbnail_info_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.thumbnail_info_label.sizePolicy().hasHeightForWidth())
        self.thumbnail_info_label.setSizePolicy(sizePolicy2)
        self.thumbnail_info_label.setMinimumSize(QSize(0, 50))
        self.thumbnail_info_label.setFont(font1)
        self.thumbnail_info_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: rgb(255, 0, 0);")

        self.monitoring_horizontalLayout.addWidget(self.thumbnail_info_label)

        self.maxfev_alert = QPushButton(self.centralwidget)
        self.maxfev_alert.setObjectName(u"maxfev_alert")
        sizePolicy1.setHeightForWidth(self.maxfev_alert.sizePolicy().hasHeightForWidth())
        self.maxfev_alert.setSizePolicy(sizePolicy1)
        self.maxfev_alert.setMinimumSize(QSize(0, 50))
        self.maxfev_alert.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon2 = QIcon()
        icon2.addFile(u"asset/alert.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maxfev_alert.setIcon(icon2)
        self.maxfev_alert.setIconSize(QSize(30, 30))
        self.maxfev_alert.setAutoDefault(True)
        self.maxfev_alert.setFlat(True)

        self.monitoring_horizontalLayout.addWidget(self.maxfev_alert)

        self.blank_label_2 = QLabel(self.centralwidget)
        self.blank_label_2.setObjectName(u"blank_label_2")
        sizePolicy1.setHeightForWidth(self.blank_label_2.sizePolicy().hasHeightForWidth())
        self.blank_label_2.setSizePolicy(sizePolicy1)
        self.blank_label_2.setMinimumSize(QSize(16, 50))
        self.blank_label_2.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")

        self.monitoring_horizontalLayout.addWidget(self.blank_label_2)

        self.alert = QPushButton(self.centralwidget)
        self.alert.setObjectName(u"alert")
        sizePolicy1.setHeightForWidth(self.alert.sizePolicy().hasHeightForWidth())
        self.alert.setSizePolicy(sizePolicy1)
        self.alert.setMinimumSize(QSize(0, 50))
        self.alert.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon3 = QIcon()
        icon3.addFile(u"asset/green.png", QSize(), QIcon.Normal, QIcon.Off)
        self.alert.setIcon(icon3)
        self.alert.setIconSize(QSize(30, 30))
        self.alert.setAutoDefault(True)
        self.alert.setFlat(True)

        self.monitoring_horizontalLayout.addWidget(self.alert)

        self.blank_label = QLabel(self.centralwidget)
        self.blank_label.setObjectName(u"blank_label")
        sizePolicy1.setHeightForWidth(self.blank_label.sizePolicy().hasHeightForWidth())
        self.blank_label.setSizePolicy(sizePolicy1)
        self.blank_label.setMinimumSize(QSize(16, 50))
        self.blank_label.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")

        self.monitoring_horizontalLayout.addWidget(self.blank_label)

        self.setting_button = QPushButton(self.centralwidget)
        self.setting_button.setObjectName(u"setting_button")
        self.setting_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.setting_button.sizePolicy().hasHeightForWidth())
        self.setting_button.setSizePolicy(sizePolicy1)
        self.setting_button.setMinimumSize(QSize(0, 50))
        self.setting_button.setCursor(QCursor(Qt.OpenHandCursor))
        self.setting_button.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon4 = QIcon()
        icon4.addFile(u"asset/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setting_button.setIcon(icon4)
        self.setting_button.setIconSize(QSize(40, 40))
        self.setting_button.setAutoDefault(True)
        self.setting_button.setFlat(True)

        self.monitoring_horizontalLayout.addWidget(self.setting_button)


        self.verticalLayout.addLayout(self.monitoring_horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.front_label = QLabel(self.centralwidget)
        self.front_label.setObjectName(u"front_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.front_label.sizePolicy().hasHeightForWidth())
        self.front_label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.front_label)

        self.rear_label = QLabel(self.centralwidget)
        self.rear_label.setObjectName(u"rear_label")
        sizePolicy3.setHeightForWidth(self.rear_label.sizePolicy().hasHeightForWidth())
        self.rear_label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.rear_label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.camera_verticalLayout = QVBoxLayout()
        self.camera_verticalLayout.setSpacing(0)
        self.camera_verticalLayout.setObjectName(u"camera_verticalLayout")
        self.camera_verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.video_horizontalLayout = QHBoxLayout()
        self.video_horizontalLayout.setSpacing(0)
        self.video_horizontalLayout.setObjectName(u"video_horizontalLayout")
        self.video_horizontalLayout.setContentsMargins(-1, 0, -1, 0)

        self.camera_verticalLayout.addLayout(self.video_horizontalLayout)


        self.verticalLayout.addLayout(self.camera_verticalLayout)

        self.thumbnail_horizontalLayout = QHBoxLayout()
        self.thumbnail_horizontalLayout.setSpacing(2)
        self.thumbnail_horizontalLayout.setObjectName(u"thumbnail_horizontalLayout")
        self.ago6hour_verticalLayout = QVBoxLayout()
        self.ago6hour_verticalLayout.setSpacing(0)
        self.ago6hour_verticalLayout.setObjectName(u"ago6hour_verticalLayout")
        self.label_6hour = QLabel(self.centralwidget)
        self.label_6hour.setObjectName(u"label_6hour")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_6hour.sizePolicy().hasHeightForWidth())
        self.label_6hour.setSizePolicy(sizePolicy4)
        self.label_6hour.setMinimumSize(QSize(0, 0))
        self.label_6hour.setMaximumSize(QSize(16777215, 131))
        self.label_6hour.setStyleSheet(u"")

        self.ago6hour_verticalLayout.addWidget(self.label_6hour)

        self.label_6hour_time = QLabel(self.centralwidget)
        self.label_6hour_time.setObjectName(u"label_6hour_time")
        sizePolicy3.setHeightForWidth(self.label_6hour_time.sizePolicy().hasHeightForWidth())
        self.label_6hour_time.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setFamilies([u"Noto Sans"])
        font3.setPointSize(11)
        font3.setBold(True)
        self.label_6hour_time.setFont(font3)
        self.label_6hour_time.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:#ffffff;")
        self.label_6hour_time.setAlignment(Qt.AlignCenter)

        self.ago6hour_verticalLayout.addWidget(self.label_6hour_time)


        self.thumbnail_horizontalLayout.addLayout(self.ago6hour_verticalLayout)

        self.ago5hour_verticalLayout = QVBoxLayout()
        self.ago5hour_verticalLayout.setSpacing(0)
        self.ago5hour_verticalLayout.setObjectName(u"ago5hour_verticalLayout")
        self.label_5hour = QLabel(self.centralwidget)
        self.label_5hour.setObjectName(u"label_5hour")
        sizePolicy4.setHeightForWidth(self.label_5hour.sizePolicy().hasHeightForWidth())
        self.label_5hour.setSizePolicy(sizePolicy4)
        self.label_5hour.setMinimumSize(QSize(0, 0))
        self.label_5hour.setMaximumSize(QSize(16777215, 131))
        self.label_5hour.setStyleSheet(u"")

        self.ago5hour_verticalLayout.addWidget(self.label_5hour)

        self.label_5hour_time = QLabel(self.centralwidget)
        self.label_5hour_time.setObjectName(u"label_5hour_time")
        sizePolicy3.setHeightForWidth(self.label_5hour_time.sizePolicy().hasHeightForWidth())
        self.label_5hour_time.setSizePolicy(sizePolicy3)
        self.label_5hour_time.setFont(font3)
        self.label_5hour_time.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:#ffffff;")
        self.label_5hour_time.setAlignment(Qt.AlignCenter)

        self.ago5hour_verticalLayout.addWidget(self.label_5hour_time)


        self.thumbnail_horizontalLayout.addLayout(self.ago5hour_verticalLayout)

        self.ago4hour_verticalLayout = QVBoxLayout()
        self.ago4hour_verticalLayout.setSpacing(0)
        self.ago4hour_verticalLayout.setObjectName(u"ago4hour_verticalLayout")
        self.label_4hour = QLabel(self.centralwidget)
        self.label_4hour.setObjectName(u"label_4hour")
        sizePolicy4.setHeightForWidth(self.label_4hour.sizePolicy().hasHeightForWidth())
        self.label_4hour.setSizePolicy(sizePolicy4)
        self.label_4hour.setMinimumSize(QSize(0, 0))
        self.label_4hour.setMaximumSize(QSize(16777215, 131))
        self.label_4hour.setStyleSheet(u"")

        self.ago4hour_verticalLayout.addWidget(self.label_4hour)

        self.label_4hour_time = QLabel(self.centralwidget)
        self.label_4hour_time.setObjectName(u"label_4hour_time")
        sizePolicy3.setHeightForWidth(self.label_4hour_time.sizePolicy().hasHeightForWidth())
        self.label_4hour_time.setSizePolicy(sizePolicy3)
        self.label_4hour_time.setFont(font3)
        self.label_4hour_time.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:#ffffff;")
        self.label_4hour_time.setAlignment(Qt.AlignCenter)

        self.ago4hour_verticalLayout.addWidget(self.label_4hour_time)


        self.thumbnail_horizontalLayout.addLayout(self.ago4hour_verticalLayout)

        self.ago3hour_verticalLayout = QVBoxLayout()
        self.ago3hour_verticalLayout.setSpacing(0)
        self.ago3hour_verticalLayout.setObjectName(u"ago3hour_verticalLayout")
        self.label_3hour = QLabel(self.centralwidget)
        self.label_3hour.setObjectName(u"label_3hour")
        sizePolicy4.setHeightForWidth(self.label_3hour.sizePolicy().hasHeightForWidth())
        self.label_3hour.setSizePolicy(sizePolicy4)
        self.label_3hour.setMinimumSize(QSize(0, 0))
        self.label_3hour.setMaximumSize(QSize(16777215, 131))
        self.label_3hour.setStyleSheet(u"")

        self.ago3hour_verticalLayout.addWidget(self.label_3hour)

        self.label_3hour_time = QLabel(self.centralwidget)
        self.label_3hour_time.setObjectName(u"label_3hour_time")
        sizePolicy3.setHeightForWidth(self.label_3hour_time.sizePolicy().hasHeightForWidth())
        self.label_3hour_time.setSizePolicy(sizePolicy3)
        self.label_3hour_time.setFont(font3)
        self.label_3hour_time.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:#ffffff;")
        self.label_3hour_time.setAlignment(Qt.AlignCenter)

        self.ago3hour_verticalLayout.addWidget(self.label_3hour_time)


        self.thumbnail_horizontalLayout.addLayout(self.ago3hour_verticalLayout)

        self.ago2hour_verticalLayout = QVBoxLayout()
        self.ago2hour_verticalLayout.setSpacing(0)
        self.ago2hour_verticalLayout.setObjectName(u"ago2hour_verticalLayout")
        self.label_2hour = QLabel(self.centralwidget)
        self.label_2hour.setObjectName(u"label_2hour")
        sizePolicy4.setHeightForWidth(self.label_2hour.sizePolicy().hasHeightForWidth())
        self.label_2hour.setSizePolicy(sizePolicy4)
        self.label_2hour.setMinimumSize(QSize(0, 0))
        self.label_2hour.setMaximumSize(QSize(16777215, 131))
        self.label_2hour.setStyleSheet(u"")

        self.ago2hour_verticalLayout.addWidget(self.label_2hour)

        self.label_2hour_time = QLabel(self.centralwidget)
        self.label_2hour_time.setObjectName(u"label_2hour_time")
        sizePolicy3.setHeightForWidth(self.label_2hour_time.sizePolicy().hasHeightForWidth())
        self.label_2hour_time.setSizePolicy(sizePolicy3)
        self.label_2hour_time.setFont(font3)
        self.label_2hour_time.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:#ffffff;")
        self.label_2hour_time.setAlignment(Qt.AlignCenter)

        self.ago2hour_verticalLayout.addWidget(self.label_2hour_time)


        self.thumbnail_horizontalLayout.addLayout(self.ago2hour_verticalLayout)

        self.ago1hour_verticalLayout = QVBoxLayout()
        self.ago1hour_verticalLayout.setSpacing(0)
        self.ago1hour_verticalLayout.setObjectName(u"ago1hour_verticalLayout")
        self.label_1hour = QLabel(self.centralwidget)
        self.label_1hour.setObjectName(u"label_1hour")
        sizePolicy4.setHeightForWidth(self.label_1hour.sizePolicy().hasHeightForWidth())
        self.label_1hour.setSizePolicy(sizePolicy4)
        self.label_1hour.setMinimumSize(QSize(0, 0))
        self.label_1hour.setMaximumSize(QSize(16777215, 131))
        self.label_1hour.setStyleSheet(u"")

        self.ago1hour_verticalLayout.addWidget(self.label_1hour)

        self.label_1hour_time = QLabel(self.centralwidget)
        self.label_1hour_time.setObjectName(u"label_1hour_time")
        sizePolicy3.setHeightForWidth(self.label_1hour_time.sizePolicy().hasHeightForWidth())
        self.label_1hour_time.setSizePolicy(sizePolicy3)
        self.label_1hour_time.setFont(font3)
        self.label_1hour_time.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color:#ffffff;")
        self.label_1hour_time.setAlignment(Qt.AlignCenter)

        self.ago1hour_verticalLayout.addWidget(self.label_1hour_time)


        self.thumbnail_horizontalLayout.addLayout(self.ago1hour_verticalLayout)


        self.verticalLayout.addLayout(self.thumbnail_horizontalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.data_horizontalLayout = QHBoxLayout()
        self.data_horizontalLayout.setObjectName(u"data_horizontalLayout")
        self.data_horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.timeseries_label_2 = QLabel(self.centralwidget)
        self.timeseries_label_2.setObjectName(u"timeseries_label_2")
        sizePolicy2.setHeightForWidth(self.timeseries_label_2.sizePolicy().hasHeightForWidth())
        self.timeseries_label_2.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setFamilies([u"Noto Sans"])
        font4.setPointSize(23)
        self.timeseries_label_2.setFont(font4)
        self.timeseries_label_2.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.horizontalLayout_2.addWidget(self.timeseries_label_2)

        self.timeseries_button_2 = QPushButton(self.centralwidget)
        self.timeseries_button_2.setObjectName(u"timeseries_button_2")
        sizePolicy1.setHeightForWidth(self.timeseries_button_2.sizePolicy().hasHeightForWidth())
        self.timeseries_button_2.setSizePolicy(sizePolicy1)
        self.timeseries_button_2.setMinimumSize(QSize(0, 42))
        self.timeseries_button_2.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon5 = QIcon()
        icon5.addFile(u"asset/graph.png", QSize(), QIcon.Normal, QIcon.Off)
        self.timeseries_button_2.setIcon(icon5)
        self.timeseries_button_2.setIconSize(QSize(32, 32))
        self.timeseries_button_2.setAutoDefault(True)
        self.timeseries_button_2.setFlat(True)

        self.horizontalLayout_2.addWidget(self.timeseries_button_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.graph_horizontalLayout = QVBoxLayout()
        self.graph_horizontalLayout.setObjectName(u"graph_horizontalLayout")

        self.verticalLayout_2.addLayout(self.graph_horizontalLayout)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.timeseries_verticalLayout = QVBoxLayout()
        self.timeseries_verticalLayout.setSpacing(0)
        self.timeseries_verticalLayout.setObjectName(u"timeseries_verticalLayout")
        self.timeseries_verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.timeseries_verticalLayout.setContentsMargins(-1, -1, 6, -1)
        self.timeseries_horizontalLayout = QHBoxLayout()
        self.timeseries_horizontalLayout.setSpacing(0)
        self.timeseries_horizontalLayout.setObjectName(u"timeseries_horizontalLayout")
        self.timeseries_label = QLabel(self.centralwidget)
        self.timeseries_label.setObjectName(u"timeseries_label")
        sizePolicy2.setHeightForWidth(self.timeseries_label.sizePolicy().hasHeightForWidth())
        self.timeseries_label.setSizePolicy(sizePolicy2)
        self.timeseries_label.setFont(font4)
        self.timeseries_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.timeseries_horizontalLayout.addWidget(self.timeseries_label)

        self.timeseries_button = QPushButton(self.centralwidget)
        self.timeseries_button.setObjectName(u"timeseries_button")
        sizePolicy1.setHeightForWidth(self.timeseries_button.sizePolicy().hasHeightForWidth())
        self.timeseries_button.setSizePolicy(sizePolicy1)
        self.timeseries_button.setMinimumSize(QSize(0, 42))
        self.timeseries_button.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon6 = QIcon()
        icon6.addFile(u"asset/polar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.timeseries_button.setIcon(icon6)
        self.timeseries_button.setIconSize(QSize(35, 35))
        self.timeseries_button.setAutoDefault(True)
        self.timeseries_button.setFlat(True)

        self.timeseries_horizontalLayout.addWidget(self.timeseries_button)


        self.timeseries_verticalLayout.addLayout(self.timeseries_horizontalLayout)

        self.polar_horizontalLayout = QHBoxLayout()
        self.polar_horizontalLayout.setObjectName(u"polar_horizontalLayout")

        self.timeseries_verticalLayout.addLayout(self.polar_horizontalLayout)


        self.horizontalLayout.addLayout(self.timeseries_verticalLayout)


        self.data_horizontalLayout.addLayout(self.horizontalLayout)

        self.etc_verticalLayout = QVBoxLayout()
        self.etc_verticalLayout.setObjectName(u"etc_verticalLayout")
        self.etc_verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.time_horizontalLayout = QHBoxLayout()
        self.time_horizontalLayout.setSpacing(0)
        self.time_horizontalLayout.setObjectName(u"time_horizontalLayout")
        self.time_horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.time_label = QLabel(self.centralwidget)
        self.time_label.setObjectName(u"time_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.time_label.sizePolicy().hasHeightForWidth())
        self.time_label.setSizePolicy(sizePolicy5)
        self.time_label.setFont(font4)
        self.time_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.time_horizontalLayout.addWidget(self.time_label)

        self.time_button = QPushButton(self.centralwidget)
        self.time_button.setObjectName(u"time_button")
        sizePolicy1.setHeightForWidth(self.time_button.sizePolicy().hasHeightForWidth())
        self.time_button.setSizePolicy(sizePolicy1)
        self.time_button.setMinimumSize(QSize(0, 42))
        self.time_button.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon7 = QIcon()
        icon7.addFile(u"asset/clock.png", QSize(), QIcon.Normal, QIcon.Off)
        self.time_button.setIcon(icon7)
        self.time_button.setIconSize(QSize(32, 32))

        self.time_horizontalLayout.addWidget(self.time_button)


        self.etc_verticalLayout.addLayout(self.time_horizontalLayout)

        self.real_time_label = QLabel(self.centralwidget)
        self.real_time_label.setObjectName(u"real_time_label")
        sizePolicy.setHeightForWidth(self.real_time_label.sizePolicy().hasHeightForWidth())
        self.real_time_label.setSizePolicy(sizePolicy)
        font5 = QFont()
        font5.setFamilies([u"Noto Sans"])
        font5.setPointSize(40)
        self.real_time_label.setFont(font5)
        self.real_time_label.setStyleSheet(u"color:#ffffff;")
        self.real_time_label.setAlignment(Qt.AlignCenter)

        self.etc_verticalLayout.addWidget(self.real_time_label)

        self.prevailing_vis_horizontalLayout = QHBoxLayout()
        self.prevailing_vis_horizontalLayout.setSpacing(0)
        self.prevailing_vis_horizontalLayout.setObjectName(u"prevailing_vis_horizontalLayout")
        self.prevailing_vis_horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.prevailing_vis_label = QLabel(self.centralwidget)
        self.prevailing_vis_label.setObjectName(u"prevailing_vis_label")
        sizePolicy5.setHeightForWidth(self.prevailing_vis_label.sizePolicy().hasHeightForWidth())
        self.prevailing_vis_label.setSizePolicy(sizePolicy5)
        self.prevailing_vis_label.setFont(font4)
        self.prevailing_vis_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.prevailing_vis_horizontalLayout.addWidget(self.prevailing_vis_label)

        self.prevailing_vis_button = QPushButton(self.centralwidget)
        self.prevailing_vis_button.setObjectName(u"prevailing_vis_button")
        sizePolicy1.setHeightForWidth(self.prevailing_vis_button.sizePolicy().hasHeightForWidth())
        self.prevailing_vis_button.setSizePolicy(sizePolicy1)
        self.prevailing_vis_button.setMinimumSize(QSize(0, 42))
        self.prevailing_vis_button.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;")
        icon8 = QIcon()
        icon8.addFile(u"asset/vis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.prevailing_vis_button.setIcon(icon8)
        self.prevailing_vis_button.setIconSize(QSize(32, 32))

        self.prevailing_vis_horizontalLayout.addWidget(self.prevailing_vis_button)


        self.etc_verticalLayout.addLayout(self.prevailing_vis_horizontalLayout)

        self.c_vis_label = QLabel(self.centralwidget)
        self.c_vis_label.setObjectName(u"c_vis_label")
        sizePolicy.setHeightForWidth(self.c_vis_label.sizePolicy().hasHeightForWidth())
        self.c_vis_label.setSizePolicy(sizePolicy)
        self.c_vis_label.setFont(font5)
        self.c_vis_label.setStyleSheet(u"color:#ffffff;")
        self.c_vis_label.setAlignment(Qt.AlignCenter)

        self.etc_verticalLayout.addWidget(self.c_vis_label)

        self.prediction_vis_horizontalLayout = QHBoxLayout()
        self.prediction_vis_horizontalLayout.setSpacing(0)
        self.prediction_vis_horizontalLayout.setObjectName(u"prediction_vis_horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy5.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy5)
        self.label.setFont(font4)
        self.label.setStyleSheet(u"background-color:rgb(27,49,70);color: rgb(69, 165, 255);")

        self.prediction_vis_horizontalLayout.addWidget(self.label)

        self.button = QPushButton(self.centralwidget)
        self.button.setObjectName(u"button")
        sizePolicy1.setHeightForWidth(self.button.sizePolicy().hasHeightForWidth())
        self.button.setSizePolicy(sizePolicy1)
        self.button.setMinimumSize(QSize(0, 42))
        self.button.setStyleSheet(u"background-color:rgb(27,49,70);color: rgb(69, 165, 255);")
        icon9 = QIcon()
        icon9.addFile(u"asset/pre_vis_1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button.setIcon(icon9)
        self.button.setIconSize(QSize(32, 32))

        self.prediction_vis_horizontalLayout.addWidget(self.button)


        self.etc_verticalLayout.addLayout(self.prediction_vis_horizontalLayout)

        self.p_vis_label = QLabel(self.centralwidget)
        self.p_vis_label.setObjectName(u"p_vis_label")
        sizePolicy.setHeightForWidth(self.p_vis_label.sizePolicy().hasHeightForWidth())
        self.p_vis_label.setSizePolicy(sizePolicy)
        self.p_vis_label.setFont(font5)
        self.p_vis_label.setStyleSheet(u"color: rgb(69, 165, 255);")
        self.p_vis_label.setAlignment(Qt.AlignCenter)

        self.etc_verticalLayout.addWidget(self.p_vis_label)


        self.data_horizontalLayout.addLayout(self.etc_verticalLayout)


        self.verticalLayout.addLayout(self.data_horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)

        self.logo.setDefault(True)
        self.maxfev_alert.setDefault(True)
        self.alert.setDefault(True)
        self.setting_button.setDefault(True)
        self.timeseries_button_2.setDefault(True)
        self.timeseries_button.setDefault(True)


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
        self.thumbnail_info_label_2.setText("")
        self.logo.setText("")
        self.monitoring_label.setText(QCoreApplication.translate("MainWindow", u"  JS-08 ", None))
        self.thumbnail_info_label.setText("")
#if QT_CONFIG(tooltip)
        self.maxfev_alert.setToolTip(QCoreApplication.translate("MainWindow", u"Optimal parameters not found: Number of calls to function has reached max fev = 5000.", None))
#endif // QT_CONFIG(tooltip)
        self.maxfev_alert.setText("")
        self.blank_label_2.setText("")
        self.alert.setText("")
        self.blank_label.setText("")
        self.setting_button.setText("")
        self.front_label.setText("")
        self.rear_label.setText("")
        self.label_6hour.setText("")
        self.label_6hour_time.setText("")
        self.label_5hour.setText("")
        self.label_5hour_time.setText("")
        self.label_4hour.setText("")
        self.label_4hour_time.setText("")
        self.label_3hour.setText("")
        self.label_3hour_time.setText("")
        self.label_2hour.setText("")
        self.label_2hour_time.setText("")
        self.label_1hour.setText("")
        self.label_1hour_time.setText("")
        self.timeseries_label_2.setText(QCoreApplication.translate("MainWindow", u"   Time series", None))
        self.timeseries_button_2.setText("")
        self.timeseries_label.setText(QCoreApplication.translate("MainWindow", u"   Discernment", None))
        self.timeseries_button.setText("")
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"   Current time", None))
        self.time_button.setText("")
        self.real_time_label.setText("")
        self.prevailing_vis_label.setText(QCoreApplication.translate("MainWindow", u"   Prevailing Visibility", None))
        self.prevailing_vis_button.setText("")
        self.c_vis_label.setText(QCoreApplication.translate("MainWindow", u"- m", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"  Prediction Visibility", None))
        self.button.setText("")
        self.p_vis_label.setText(QCoreApplication.translate("MainWindow", u"- m", None))
    # retranslateUi

