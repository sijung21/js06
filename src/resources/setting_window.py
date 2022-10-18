# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_window.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QTableWidget,
    QTableWidgetItem, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1207, 767)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridWidget = QWidget(Dialog)
        self.gridWidget.setObjectName(u"gridWidget")
        self.gridWidget.setStyleSheet(u"background-color:rgb(22,32,42);")
        self.gridLayout_2 = QGridLayout(self.gridWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.main_verticalLayout = QVBoxLayout()
        self.main_verticalLayout.setObjectName(u"main_verticalLayout")
        self.top_horizontalLayout = QHBoxLayout()
        self.top_horizontalLayout.setObjectName(u"top_horizontalLayout")
        self.setting_verticalLayout = QVBoxLayout()
        self.setting_verticalLayout.setObjectName(u"setting_verticalLayout")
        self.setting_horizontalLayout = QHBoxLayout()
        self.setting_horizontalLayout.setSpacing(0)
        self.setting_horizontalLayout.setObjectName(u"setting_horizontalLayout")
        self.target_setting_label = QLabel(self.gridWidget)
        self.target_setting_label.setObjectName(u"target_setting_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.target_setting_label.sizePolicy().hasHeightForWidth())
        self.target_setting_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setPointSize(23)
        self.target_setting_label.setFont(font)
        self.target_setting_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.setting_horizontalLayout.addWidget(self.target_setting_label)

        self.flip_button = QPushButton(self.gridWidget)
        self.flip_button.setObjectName(u"flip_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.flip_button.sizePolicy().hasHeightForWidth())
        self.flip_button.setSizePolicy(sizePolicy2)
        self.flip_button.setMinimumSize(QSize(0, 42))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        font1.setPointSize(15)
        self.flip_button.setFont(font1)
        self.flip_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.flip_button.setStyleSheet(u"border:0px;\n"
"background-color: #1b3146;\n"
"color: #ffffff;")
        icon = QIcon()
        icon.addFile(u"asset/flip_off.png", QSize(), QIcon.Normal, QIcon.Off)
        self.flip_button.setIcon(icon)
        self.flip_button.setIconSize(QSize(40, 40))
        self.flip_button.setFlat(True)

        self.setting_horizontalLayout.addWidget(self.flip_button)


        self.setting_verticalLayout.addLayout(self.setting_horizontalLayout)

        self.image_label = QLabel(self.gridWidget)
        self.image_label.setObjectName(u"image_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy3)

        self.setting_verticalLayout.addWidget(self.image_label)


        self.top_horizontalLayout.addLayout(self.setting_verticalLayout)


        self.main_verticalLayout.addLayout(self.top_horizontalLayout)

        self.bottom_horizontalLayout = QHBoxLayout()
        self.bottom_horizontalLayout.setSpacing(12)
        self.bottom_horizontalLayout.setObjectName(u"bottom_horizontalLayout")
        self.target_list_verticalLayout = QVBoxLayout()
        self.target_list_verticalLayout.setSpacing(0)
        self.target_list_verticalLayout.setObjectName(u"target_list_verticalLayout")
        self.target_list_verticalLayout.setContentsMargins(6, -1, -1, -1)
        self.target_list_label = QLabel(self.gridWidget)
        self.target_list_label.setObjectName(u"target_list_label")
        sizePolicy1.setHeightForWidth(self.target_list_label.sizePolicy().hasHeightForWidth())
        self.target_list_label.setSizePolicy(sizePolicy1)
        self.target_list_label.setFont(font)
        self.target_list_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.target_list_verticalLayout.addWidget(self.target_list_label)

        self.tableWidget = QTableWidget(self.gridWidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMaximumSize(QSize(700, 500))

        self.target_list_verticalLayout.addWidget(self.tableWidget)


        self.bottom_horizontalLayout.addLayout(self.target_list_verticalLayout)

        self.value_verticalLayout = QVBoxLayout()
        self.value_verticalLayout.setSpacing(0)
        self.value_verticalLayout.setObjectName(u"value_verticalLayout")
        self.value_label = QLabel(self.gridWidget)
        self.value_label.setObjectName(u"value_label")
        sizePolicy1.setHeightForWidth(self.value_label.sizePolicy().hasHeightForWidth())
        self.value_label.setSizePolicy(sizePolicy1)
        self.value_label.setFont(font)
        self.value_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.value_verticalLayout.addWidget(self.value_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graph_verticalLayout = QVBoxLayout()
        self.graph_verticalLayout.setSpacing(0)
        self.graph_verticalLayout.setObjectName(u"graph_verticalLayout")

        self.horizontalLayout.addLayout(self.graph_verticalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.label = QLabel(self.gridWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.red_checkBox = QCheckBox(self.gridWidget)
        self.red_checkBox.setObjectName(u"red_checkBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.red_checkBox.sizePolicy().hasHeightForWidth())
        self.red_checkBox.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setBold(False)
        self.red_checkBox.setFont(font2)
        self.red_checkBox.setStyleSheet(u"\n"
"color: #ffffff;")
        self.red_checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.red_checkBox)

        self.green_checkBox = QCheckBox(self.gridWidget)
        self.green_checkBox.setObjectName(u"green_checkBox")
        sizePolicy4.setHeightForWidth(self.green_checkBox.sizePolicy().hasHeightForWidth())
        self.green_checkBox.setSizePolicy(sizePolicy4)
        self.green_checkBox.setFont(font2)
        self.green_checkBox.setStyleSheet(u"\n"
"color: #ffffff;")
        self.green_checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.green_checkBox)

        self.blue_checkBox = QCheckBox(self.gridWidget)
        self.blue_checkBox.setObjectName(u"blue_checkBox")
        sizePolicy4.setHeightForWidth(self.blue_checkBox.sizePolicy().hasHeightForWidth())
        self.blue_checkBox.setSizePolicy(sizePolicy4)
        self.blue_checkBox.setFont(font2)
        self.blue_checkBox.setStyleSheet(u"\n"
"color: #ffffff;")
        self.blue_checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.blue_checkBox)

        self.label_2 = QLabel(self.gridWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.value_verticalLayout.addLayout(self.horizontalLayout)


        self.bottom_horizontalLayout.addLayout(self.value_verticalLayout)

        self.etc_verticalLayout = QVBoxLayout()
        self.etc_verticalLayout.setObjectName(u"etc_verticalLayout")
        self.setting_label = QLabel(self.gridWidget)
        self.setting_label.setObjectName(u"setting_label")
        sizePolicy1.setHeightForWidth(self.setting_label.sizePolicy().hasHeightForWidth())
        self.setting_label.setSizePolicy(sizePolicy1)
        self.setting_label.setFont(font)
        self.setting_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.etc_verticalLayout.addWidget(self.setting_label)

        self.data_csv_horizontalLayout = QHBoxLayout()
        self.data_csv_horizontalLayout.setSpacing(0)
        self.data_csv_horizontalLayout.setObjectName(u"data_csv_horizontalLayout")
        self.data_csv_path_label = QLabel(self.gridWidget)
        self.data_csv_path_label.setObjectName(u"data_csv_path_label")
        sizePolicy3.setHeightForWidth(self.data_csv_path_label.sizePolicy().hasHeightForWidth())
        self.data_csv_path_label.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setFamilies([u"Noto Sans"])
        font3.setPointSize(10)
        self.data_csv_path_label.setFont(font3)
        self.data_csv_path_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.data_csv_horizontalLayout.addWidget(self.data_csv_path_label)

        self.data_csv_path_textBrowser = QTextBrowser(self.gridWidget)
        self.data_csv_path_textBrowser.setObjectName(u"data_csv_path_textBrowser")
        sizePolicy1.setHeightForWidth(self.data_csv_path_textBrowser.sizePolicy().hasHeightForWidth())
        self.data_csv_path_textBrowser.setSizePolicy(sizePolicy1)
        self.data_csv_path_textBrowser.setMaximumSize(QSize(16777215, 50))
        self.data_csv_path_textBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.data_csv_horizontalLayout.addWidget(self.data_csv_path_textBrowser)

        self.data_csv_path_button = QPushButton(self.gridWidget)
        self.data_csv_path_button.setObjectName(u"data_csv_path_button")
        sizePolicy1.setHeightForWidth(self.data_csv_path_button.sizePolicy().hasHeightForWidth())
        self.data_csv_path_button.setSizePolicy(sizePolicy1)
        self.data_csv_path_button.setMaximumSize(QSize(50, 50))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(17)
        self.data_csv_path_button.setFont(font4)
        self.data_csv_path_button.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.data_csv_horizontalLayout.addWidget(self.data_csv_path_button)


        self.etc_verticalLayout.addLayout(self.data_csv_horizontalLayout)

        self.target_csv_horizontalLayout = QHBoxLayout()
        self.target_csv_horizontalLayout.setSpacing(0)
        self.target_csv_horizontalLayout.setObjectName(u"target_csv_horizontalLayout")
        self.target_csv_path_label = QLabel(self.gridWidget)
        self.target_csv_path_label.setObjectName(u"target_csv_path_label")
        sizePolicy3.setHeightForWidth(self.target_csv_path_label.sizePolicy().hasHeightForWidth())
        self.target_csv_path_label.setSizePolicy(sizePolicy3)
        self.target_csv_path_label.setFont(font3)
        self.target_csv_path_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.target_csv_horizontalLayout.addWidget(self.target_csv_path_label)

        self.target_csv_path_textBrowser = QTextBrowser(self.gridWidget)
        self.target_csv_path_textBrowser.setObjectName(u"target_csv_path_textBrowser")
        sizePolicy1.setHeightForWidth(self.target_csv_path_textBrowser.sizePolicy().hasHeightForWidth())
        self.target_csv_path_textBrowser.setSizePolicy(sizePolicy1)
        self.target_csv_path_textBrowser.setMaximumSize(QSize(16777215, 50))
        self.target_csv_path_textBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.target_csv_horizontalLayout.addWidget(self.target_csv_path_textBrowser)

        self.target_csv_path_button = QPushButton(self.gridWidget)
        self.target_csv_path_button.setObjectName(u"target_csv_path_button")
        sizePolicy1.setHeightForWidth(self.target_csv_path_button.sizePolicy().hasHeightForWidth())
        self.target_csv_path_button.setSizePolicy(sizePolicy1)
        self.target_csv_path_button.setMaximumSize(QSize(50, 50))
        self.target_csv_path_button.setFont(font4)
        self.target_csv_path_button.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.target_csv_horizontalLayout.addWidget(self.target_csv_path_button)


        self.etc_verticalLayout.addLayout(self.target_csv_horizontalLayout)

        self.image_save_horizontalLayout = QHBoxLayout()
        self.image_save_horizontalLayout.setSpacing(0)
        self.image_save_horizontalLayout.setObjectName(u"image_save_horizontalLayout")
        self.image_save_path_label = QLabel(self.gridWidget)
        self.image_save_path_label.setObjectName(u"image_save_path_label")
        sizePolicy3.setHeightForWidth(self.image_save_path_label.sizePolicy().hasHeightForWidth())
        self.image_save_path_label.setSizePolicy(sizePolicy3)
        self.image_save_path_label.setFont(font3)
        self.image_save_path_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.image_save_horizontalLayout.addWidget(self.image_save_path_label)

        self.image_save_path_textBrowser = QTextBrowser(self.gridWidget)
        self.image_save_path_textBrowser.setObjectName(u"image_save_path_textBrowser")
        sizePolicy1.setHeightForWidth(self.image_save_path_textBrowser.sizePolicy().hasHeightForWidth())
        self.image_save_path_textBrowser.setSizePolicy(sizePolicy1)
        self.image_save_path_textBrowser.setMaximumSize(QSize(16777215, 50))
        self.image_save_path_textBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.image_save_horizontalLayout.addWidget(self.image_save_path_textBrowser)

        self.image_save_path_button = QPushButton(self.gridWidget)
        self.image_save_path_button.setObjectName(u"image_save_path_button")
        sizePolicy1.setHeightForWidth(self.image_save_path_button.sizePolicy().hasHeightForWidth())
        self.image_save_path_button.setSizePolicy(sizePolicy1)
        self.image_save_path_button.setMaximumSize(QSize(50, 50))
        self.image_save_path_button.setFont(font4)
        self.image_save_path_button.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.image_save_horizontalLayout.addWidget(self.image_save_path_button)


        self.etc_verticalLayout.addLayout(self.image_save_horizontalLayout)

        self.vis_limit_horizontalLayout_2 = QHBoxLayout()
        self.vis_limit_horizontalLayout_2.setSpacing(6)
        self.vis_limit_horizontalLayout_2.setObjectName(u"vis_limit_horizontalLayout_2")
        self.vis_limit_label_2 = QLabel(self.gridWidget)
        self.vis_limit_label_2.setObjectName(u"vis_limit_label_2")
        sizePolicy3.setHeightForWidth(self.vis_limit_label_2.sizePolicy().hasHeightForWidth())
        self.vis_limit_label_2.setSizePolicy(sizePolicy3)
        self.vis_limit_label_2.setFont(font3)
        self.vis_limit_label_2.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.vis_limit_horizontalLayout_2.addWidget(self.vis_limit_label_2)

        self.image_size_comboBox = QComboBox(self.gridWidget)
        self.image_size_comboBox.addItem("")
        self.image_size_comboBox.addItem("")
        self.image_size_comboBox.setObjectName(u"image_size_comboBox")
        self.image_size_comboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.vis_limit_horizontalLayout_2.addWidget(self.image_size_comboBox)


        self.etc_verticalLayout.addLayout(self.vis_limit_horizontalLayout_2)

        self.vis_limit_horizontalLayout = QHBoxLayout()
        self.vis_limit_horizontalLayout.setSpacing(6)
        self.vis_limit_horizontalLayout.setObjectName(u"vis_limit_horizontalLayout")
        self.vis_limit_label = QLabel(self.gridWidget)
        self.vis_limit_label.setObjectName(u"vis_limit_label")
        sizePolicy3.setHeightForWidth(self.vis_limit_label.sizePolicy().hasHeightForWidth())
        self.vis_limit_label.setSizePolicy(sizePolicy3)
        self.vis_limit_label.setFont(font3)
        self.vis_limit_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.vis_limit_horizontalLayout.addWidget(self.vis_limit_label)

        self.vis_limit_spinBox = QSpinBox(self.gridWidget)
        self.vis_limit_spinBox.setObjectName(u"vis_limit_spinBox")
        sizePolicy1.setHeightForWidth(self.vis_limit_spinBox.sizePolicy().hasHeightForWidth())
        self.vis_limit_spinBox.setSizePolicy(sizePolicy1)
        self.vis_limit_spinBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.vis_limit_spinBox.setMaximum(20000)
        self.vis_limit_spinBox.setSingleStep(1)
        self.vis_limit_spinBox.setDisplayIntegerBase(10)

        self.vis_limit_horizontalLayout.addWidget(self.vis_limit_spinBox)


        self.etc_verticalLayout.addLayout(self.vis_limit_horizontalLayout)

        self.id_horizontalLayout = QHBoxLayout()
        self.id_horizontalLayout.setSpacing(6)
        self.id_horizontalLayout.setObjectName(u"id_horizontalLayout")
        self.id_label = QLabel(self.gridWidget)
        self.id_label.setObjectName(u"id_label")
        sizePolicy3.setHeightForWidth(self.id_label.sizePolicy().hasHeightForWidth())
        self.id_label.setSizePolicy(sizePolicy3)
        self.id_label.setFont(font3)
        self.id_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.id_horizontalLayout.addWidget(self.id_label)

        self.id_lineEdit = QLineEdit(self.gridWidget)
        self.id_lineEdit.setObjectName(u"id_lineEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.id_lineEdit.sizePolicy().hasHeightForWidth())
        self.id_lineEdit.setSizePolicy(sizePolicy5)
        self.id_lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.id_horizontalLayout.addWidget(self.id_lineEdit)


        self.etc_verticalLayout.addLayout(self.id_horizontalLayout)

        self.pw_horizontalLayout = QHBoxLayout()
        self.pw_horizontalLayout.setSpacing(6)
        self.pw_horizontalLayout.setObjectName(u"pw_horizontalLayout")
        self.pw_label = QLabel(self.gridWidget)
        self.pw_label.setObjectName(u"pw_label")
        sizePolicy3.setHeightForWidth(self.pw_label.sizePolicy().hasHeightForWidth())
        self.pw_label.setSizePolicy(sizePolicy3)
        self.pw_label.setFont(font3)
        self.pw_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.pw_horizontalLayout.addWidget(self.pw_label)

        self.pw_lineEdit = QLineEdit(self.gridWidget)
        self.pw_lineEdit.setObjectName(u"pw_lineEdit")
        sizePolicy5.setHeightForWidth(self.pw_lineEdit.sizePolicy().hasHeightForWidth())
        self.pw_lineEdit.setSizePolicy(sizePolicy5)
        self.pw_lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.pw_horizontalLayout.addWidget(self.pw_lineEdit)


        self.etc_verticalLayout.addLayout(self.pw_horizontalLayout)

        self.afd_horizontalLayout = QHBoxLayout()
        self.afd_horizontalLayout.setSpacing(6)
        self.afd_horizontalLayout.setObjectName(u"afd_horizontalLayout")
        self.afd_label = QLabel(self.gridWidget)
        self.afd_label.setObjectName(u"afd_label")
        sizePolicy3.setHeightForWidth(self.afd_label.sizePolicy().hasHeightForWidth())
        self.afd_label.setSizePolicy(sizePolicy3)
        self.afd_label.setFont(font3)
        self.afd_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.afd_horizontalLayout.addWidget(self.afd_label)

        self.afd_button = QPushButton(self.gridWidget)
        self.afd_button.setObjectName(u"afd_button")
        sizePolicy3.setHeightForWidth(self.afd_button.sizePolicy().hasHeightForWidth())
        self.afd_button.setSizePolicy(sizePolicy3)
        self.afd_button.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setPointSize(17)
        self.afd_button.setFont(font5)
        self.afd_button.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.afd_horizontalLayout.addWidget(self.afd_button)


        self.etc_verticalLayout.addLayout(self.afd_horizontalLayout)

        self.buttonBox = QDialogButtonBox(self.gridWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy4.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy4)
        font6 = QFont()
        font6.setFamilies([u"Noto Sans"])
        font6.setPointSize(9)
        self.buttonBox.setFont(font6)
        self.buttonBox.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.etc_verticalLayout.addWidget(self.buttonBox)


        self.bottom_horizontalLayout.addLayout(self.etc_verticalLayout)


        self.main_verticalLayout.addLayout(self.bottom_horizontalLayout)


        self.gridLayout_2.addLayout(self.main_verticalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.gridWidget, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.flip_button.setDefault(True)
        self.image_size_comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Setting", None))
        self.target_setting_label.setText(QCoreApplication.translate("Dialog", u"  Front Target Setting", None))
        self.flip_button.setText("")
        self.image_label.setText("")
        self.target_list_label.setText(QCoreApplication.translate("Dialog", u"   Target list", None))
        self.value_label.setText(QCoreApplication.translate("Dialog", u"   ext \u03b1 Value", None))
        self.label.setText("")
        self.red_checkBox.setText(QCoreApplication.translate("Dialog", u"Red", None))
        self.green_checkBox.setText(QCoreApplication.translate("Dialog", u"Green", None))
        self.blue_checkBox.setText(QCoreApplication.translate("Dialog", u"Blue", None))
        self.label_2.setText("")
        self.setting_label.setText(QCoreApplication.translate("Dialog", u"   Settings", None))
        self.data_csv_path_label.setText(QCoreApplication.translate("Dialog", u" Data file Path: ", None))
        self.data_csv_path_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
        self.target_csv_path_label.setText(QCoreApplication.translate("Dialog", u" Target file Path: ", None))
        self.target_csv_path_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
        self.image_save_path_label.setText(QCoreApplication.translate("Dialog", u" Image save Path: ", None))
        self.image_save_path_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
        self.vis_limit_label_2.setText(QCoreApplication.translate("Dialog", u" Image size: ", None))
        self.image_size_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Original", None))
        self.image_size_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"FHD", None))

        self.vis_limit_label.setText(QCoreApplication.translate("Dialog", u" Visibility alert limit: ", None))
        self.vis_limit_spinBox.setSuffix(QCoreApplication.translate("Dialog", u" m", None))
        self.vis_limit_spinBox.setPrefix("")
        self.id_label.setText(QCoreApplication.translate("Dialog", u" ID: ", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u" P/W: ", None))
        self.afd_label.setText(QCoreApplication.translate("Dialog", u" File delete: ", None))
        self.afd_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
    # retranslateUi

