# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_menu.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(421, 517)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gridWidget.sizePolicy().hasHeightForWidth())
        self.gridWidget.setSizePolicy(sizePolicy1)
        self.gridWidget.setStyleSheet(u"background-color:rgb(22,32,42);")
        self.gridLayout_2 = QGridLayout(self.gridWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.etc_verticalLayout = QVBoxLayout()
        self.etc_verticalLayout.setObjectName(u"etc_verticalLayout")
        self.setting_label = QLabel(self.gridWidget)
        self.setting_label.setObjectName(u"setting_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.setting_label.sizePolicy().hasHeightForWidth())
        self.setting_label.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setPointSize(23)
        self.setting_label.setFont(font)
        self.setting_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.etc_verticalLayout.addWidget(self.setting_label)

        self.data_csv_horizontalLayout = QHBoxLayout()
        self.data_csv_horizontalLayout.setSpacing(0)
        self.data_csv_horizontalLayout.setObjectName(u"data_csv_horizontalLayout")
        self.data_csv_path_label = QLabel(self.gridWidget)
        self.data_csv_path_label.setObjectName(u"data_csv_path_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.data_csv_path_label.sizePolicy().hasHeightForWidth())
        self.data_csv_path_label.setSizePolicy(sizePolicy3)
        self.data_csv_path_label.setMinimumSize(QSize(0, 50))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR Medium"])
        font1.setPointSize(10)
        self.data_csv_path_label.setFont(font1)
        self.data_csv_path_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.data_csv_horizontalLayout.addWidget(self.data_csv_path_label)

        self.data_csv_path_textBrowser = QTextBrowser(self.gridWidget)
        self.data_csv_path_textBrowser.setObjectName(u"data_csv_path_textBrowser")
        sizePolicy3.setHeightForWidth(self.data_csv_path_textBrowser.sizePolicy().hasHeightForWidth())
        self.data_csv_path_textBrowser.setSizePolicy(sizePolicy3)
        self.data_csv_path_textBrowser.setMinimumSize(QSize(0, 50))
        self.data_csv_path_textBrowser.setMaximumSize(QSize(16777215, 50))
        self.data_csv_path_textBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.data_csv_horizontalLayout.addWidget(self.data_csv_path_textBrowser)

        self.data_csv_path_button = QPushButton(self.gridWidget)
        self.data_csv_path_button.setObjectName(u"data_csv_path_button")
        sizePolicy3.setHeightForWidth(self.data_csv_path_button.sizePolicy().hasHeightForWidth())
        self.data_csv_path_button.setSizePolicy(sizePolicy3)
        self.data_csv_path_button.setMinimumSize(QSize(0, 50))
        self.data_csv_path_button.setMaximumSize(QSize(50, 50))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(17)
        self.data_csv_path_button.setFont(font2)
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
        self.target_csv_path_label.setMinimumSize(QSize(0, 50))
        self.target_csv_path_label.setFont(font1)
        self.target_csv_path_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.target_csv_horizontalLayout.addWidget(self.target_csv_path_label)

        self.target_csv_path_textBrowser = QTextBrowser(self.gridWidget)
        self.target_csv_path_textBrowser.setObjectName(u"target_csv_path_textBrowser")
        sizePolicy3.setHeightForWidth(self.target_csv_path_textBrowser.sizePolicy().hasHeightForWidth())
        self.target_csv_path_textBrowser.setSizePolicy(sizePolicy3)
        self.target_csv_path_textBrowser.setMinimumSize(QSize(0, 50))
        self.target_csv_path_textBrowser.setMaximumSize(QSize(16777215, 50))
        self.target_csv_path_textBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.target_csv_horizontalLayout.addWidget(self.target_csv_path_textBrowser)

        self.target_csv_path_button = QPushButton(self.gridWidget)
        self.target_csv_path_button.setObjectName(u"target_csv_path_button")
        sizePolicy3.setHeightForWidth(self.target_csv_path_button.sizePolicy().hasHeightForWidth())
        self.target_csv_path_button.setSizePolicy(sizePolicy3)
        self.target_csv_path_button.setMinimumSize(QSize(0, 50))
        self.target_csv_path_button.setMaximumSize(QSize(50, 50))
        self.target_csv_path_button.setFont(font2)
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
        self.image_save_path_label.setMinimumSize(QSize(0, 50))
        self.image_save_path_label.setFont(font1)
        self.image_save_path_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.image_save_horizontalLayout.addWidget(self.image_save_path_label)

        self.image_save_path_textBrowser = QTextBrowser(self.gridWidget)
        self.image_save_path_textBrowser.setObjectName(u"image_save_path_textBrowser")
        sizePolicy3.setHeightForWidth(self.image_save_path_textBrowser.sizePolicy().hasHeightForWidth())
        self.image_save_path_textBrowser.setSizePolicy(sizePolicy3)
        self.image_save_path_textBrowser.setMinimumSize(QSize(0, 50))
        self.image_save_path_textBrowser.setMaximumSize(QSize(16777215, 50))
        self.image_save_path_textBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.image_save_horizontalLayout.addWidget(self.image_save_path_textBrowser)

        self.image_save_path_button = QPushButton(self.gridWidget)
        self.image_save_path_button.setObjectName(u"image_save_path_button")
        sizePolicy3.setHeightForWidth(self.image_save_path_button.sizePolicy().hasHeightForWidth())
        self.image_save_path_button.setSizePolicy(sizePolicy3)
        self.image_save_path_button.setMinimumSize(QSize(0, 50))
        self.image_save_path_button.setMaximumSize(QSize(50, 50))
        self.image_save_path_button.setFont(font2)
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
        self.vis_limit_label_2.setMinimumSize(QSize(0, 34))
        self.vis_limit_label_2.setFont(font1)
        self.vis_limit_label_2.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.vis_limit_horizontalLayout_2.addWidget(self.vis_limit_label_2)

        self.image_size_comboBox = QComboBox(self.gridWidget)
        self.image_size_comboBox.addItem("")
        self.image_size_comboBox.addItem("")
        self.image_size_comboBox.addItem("")
        self.image_size_comboBox.setObjectName(u"image_size_comboBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.image_size_comboBox.sizePolicy().hasHeightForWidth())
        self.image_size_comboBox.setSizePolicy(sizePolicy4)
        self.image_size_comboBox.setMinimumSize(QSize(0, 34))
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
        self.vis_limit_label.setMinimumSize(QSize(0, 34))
        self.vis_limit_label.setFont(font1)
        self.vis_limit_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.vis_limit_horizontalLayout.addWidget(self.vis_limit_label)

        self.vis_limit_spinBox = QSpinBox(self.gridWidget)
        self.vis_limit_spinBox.setObjectName(u"vis_limit_spinBox")
        sizePolicy3.setHeightForWidth(self.vis_limit_spinBox.sizePolicy().hasHeightForWidth())
        self.vis_limit_spinBox.setSizePolicy(sizePolicy3)
        self.vis_limit_spinBox.setMinimumSize(QSize(0, 34))
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
        self.id_label.setMinimumSize(QSize(0, 34))
        font3 = QFont()
        font3.setFamilies([u"Noto Sans"])
        font3.setPointSize(10)
        self.id_label.setFont(font3)
        self.id_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.id_horizontalLayout.addWidget(self.id_label)

        self.id_lineEdit = QTextBrowser(self.gridWidget)
        self.id_lineEdit.setObjectName(u"id_lineEdit")
        sizePolicy3.setHeightForWidth(self.id_lineEdit.sizePolicy().hasHeightForWidth())
        self.id_lineEdit.setSizePolicy(sizePolicy3)
        self.id_lineEdit.setMinimumSize(QSize(0, 34))
        self.id_lineEdit.setMaximumSize(QSize(196, 34))
        self.id_lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.id_horizontalLayout.addWidget(self.id_lineEdit)


        self.etc_verticalLayout.addLayout(self.id_horizontalLayout)

        self.pw_horizontalLayout_3 = QHBoxLayout()
        self.pw_horizontalLayout_3.setSpacing(6)
        self.pw_horizontalLayout_3.setObjectName(u"pw_horizontalLayout_3")
        self.pw_label_3 = QLabel(self.gridWidget)
        self.pw_label_3.setObjectName(u"pw_label_3")
        sizePolicy3.setHeightForWidth(self.pw_label_3.sizePolicy().hasHeightForWidth())
        self.pw_label_3.setSizePolicy(sizePolicy3)
        self.pw_label_3.setMinimumSize(QSize(0, 34))
        self.pw_label_3.setFont(font1)
        self.pw_label_3.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.pw_horizontalLayout_3.addWidget(self.pw_label_3)

        self.current_pw = QLineEdit(self.gridWidget)
        self.current_pw.setObjectName(u"current_pw")
        sizePolicy3.setHeightForWidth(self.current_pw.sizePolicy().hasHeightForWidth())
        self.current_pw.setSizePolicy(sizePolicy3)
        self.current_pw.setMinimumSize(QSize(0, 34))
        self.current_pw.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.pw_horizontalLayout_3.addWidget(self.current_pw)


        self.etc_verticalLayout.addLayout(self.pw_horizontalLayout_3)

        self.pw_horizontalLayout = QHBoxLayout()
        self.pw_horizontalLayout.setSpacing(6)
        self.pw_horizontalLayout.setObjectName(u"pw_horizontalLayout")
        self.pw_label = QLabel(self.gridWidget)
        self.pw_label.setObjectName(u"pw_label")
        sizePolicy3.setHeightForWidth(self.pw_label.sizePolicy().hasHeightForWidth())
        self.pw_label.setSizePolicy(sizePolicy3)
        self.pw_label.setMinimumSize(QSize(0, 34))
        self.pw_label.setFont(font1)
        self.pw_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.pw_horizontalLayout.addWidget(self.pw_label)

        self.new_pw = QLineEdit(self.gridWidget)
        self.new_pw.setObjectName(u"new_pw")
        sizePolicy3.setHeightForWidth(self.new_pw.sizePolicy().hasHeightForWidth())
        self.new_pw.setSizePolicy(sizePolicy3)
        self.new_pw.setMinimumSize(QSize(0, 34))
        self.new_pw.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.pw_horizontalLayout.addWidget(self.new_pw)


        self.etc_verticalLayout.addLayout(self.pw_horizontalLayout)

        self.pw_horizontalLayout_4 = QHBoxLayout()
        self.pw_horizontalLayout_4.setSpacing(6)
        self.pw_horizontalLayout_4.setObjectName(u"pw_horizontalLayout_4")
        self.pw_label_4 = QLabel(self.gridWidget)
        self.pw_label_4.setObjectName(u"pw_label_4")
        sizePolicy3.setHeightForWidth(self.pw_label_4.sizePolicy().hasHeightForWidth())
        self.pw_label_4.setSizePolicy(sizePolicy3)
        self.pw_label_4.setMinimumSize(QSize(0, 34))
        self.pw_label_4.setFont(font1)
        self.pw_label_4.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.pw_horizontalLayout_4.addWidget(self.pw_label_4)

        self.new_pw_check = QLineEdit(self.gridWidget)
        self.new_pw_check.setObjectName(u"new_pw_check")
        sizePolicy3.setHeightForWidth(self.new_pw_check.sizePolicy().hasHeightForWidth())
        self.new_pw_check.setSizePolicy(sizePolicy3)
        self.new_pw_check.setMinimumSize(QSize(0, 34))
        self.new_pw_check.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.pw_horizontalLayout_4.addWidget(self.new_pw_check)


        self.etc_verticalLayout.addLayout(self.pw_horizontalLayout_4)

        self.buttonBox = QDialogButtonBox(self.gridWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy5)
        font4 = QFont()
        font4.setFamilies([u"Noto Sans KR Medium"])
        font4.setPointSize(9)
        self.buttonBox.setFont(font4)
        self.buttonBox.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.etc_verticalLayout.addWidget(self.buttonBox)


        self.gridLayout_2.addLayout(self.etc_verticalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.gridWidget, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.image_size_comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Setting", None))
        self.setting_label.setText(QCoreApplication.translate("Dialog", u"   Settings", None))
        self.data_csv_path_label.setText(QCoreApplication.translate("Dialog", u" \ub370\uc774\ud130 \ud30c\uc77c \uacbd\ub85c", None))
        self.data_csv_path_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
        self.target_csv_path_label.setText(QCoreApplication.translate("Dialog", u" \ud0c0\uac9f \ud30c\uc77c \uacbd\ub85c", None))
        self.target_csv_path_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
        self.image_save_path_label.setText(QCoreApplication.translate("Dialog", u" \uc774\ubbf8\uc9c0 \uc800\uc7a5 \uacbd\ub85c", None))
        self.image_save_path_button.setText(QCoreApplication.translate("Dialog", u"\u21a9", None))
        self.vis_limit_label_2.setText(QCoreApplication.translate("Dialog", u" \uc774\ubbf8\uc9c0 \ud06c\uae30 \uc9c0\uc815 ", None))
        self.image_size_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Original (PNG)", None))
        self.image_size_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Reduce (JPG)", None))
        self.image_size_comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Resize to FHD (PNG)", None))

        self.vis_limit_label.setText(QCoreApplication.translate("Dialog", u" \ucd5c\uc800 \uc2dc\uc815 \uc54c\ub9bc \uae30\uc900", None))
        self.vis_limit_spinBox.setSuffix(QCoreApplication.translate("Dialog", u" m", None))
        self.vis_limit_spinBox.setPrefix("")
        self.id_label.setText(QCoreApplication.translate("Dialog", u" ID", None))
        self.pw_label_3.setText(QCoreApplication.translate("Dialog", u" \ud604\uc7ac \ube44\ubc00\ubc88\ud638", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u" \uc0c8 \ube44\ubc00\ubc88\ud638", None))
        self.pw_label_4.setText(QCoreApplication.translate("Dialog", u" \uc0c8 \ube44\ubc00\ubc88\ud638 \ud655\uc778", None))
    # retranslateUi

