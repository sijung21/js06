# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'visibility_test_ui.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1926, 785)
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
        font.setFamilies([u"Noto Sans KR Medium"])
        font.setPointSize(23)
        self.target_setting_label.setFont(font)
        self.target_setting_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.setting_horizontalLayout.addWidget(self.target_setting_label)

        self.load_img = QPushButton(self.gridWidget)
        self.load_img.setObjectName(u"load_img")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.load_img.sizePolicy().hasHeightForWidth())
        self.load_img.setSizePolicy(sizePolicy2)
        self.load_img.setMaximumSize(QSize(16777215, 45))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans KR Medium"])
        self.load_img.setFont(font1)
        self.load_img.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.setting_horizontalLayout.addWidget(self.load_img)


        self.setting_verticalLayout.addLayout(self.setting_horizontalLayout)

        self.image_label = QLabel(self.gridWidget)
        self.image_label.setObjectName(u"image_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy3)
        self.image_label.setMinimumSize(QSize(1902, 464))
        self.image_label.setMaximumSize(QSize(16777215, 16777215))

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


        self.value_verticalLayout.addLayout(self.horizontalLayout)


        self.bottom_horizontalLayout.addLayout(self.value_verticalLayout)

        self.etc_verticalLayout = QVBoxLayout()
        self.etc_verticalLayout.setSpacing(3)
        self.etc_verticalLayout.setObjectName(u"etc_verticalLayout")
        self.setting_label = QLabel(self.gridWidget)
        self.setting_label.setObjectName(u"setting_label")
        sizePolicy1.setHeightForWidth(self.setting_label.sizePolicy().hasHeightForWidth())
        self.setting_label.setSizePolicy(sizePolicy1)
        self.setting_label.setFont(font)
        self.setting_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")

        self.etc_verticalLayout.addWidget(self.setting_label)

        self.afd_horizontalLayout = QHBoxLayout()
        self.afd_horizontalLayout.setSpacing(6)
        self.afd_horizontalLayout.setObjectName(u"afd_horizontalLayout")
        self.vis_label = QLabel(self.gridWidget)
        self.vis_label.setObjectName(u"vis_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.vis_label.sizePolicy().hasHeightForWidth())
        self.vis_label.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR Medium"])
        font2.setPointSize(25)
        self.vis_label.setFont(font2)
        self.vis_label.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")
        self.vis_label.setAlignment(Qt.AlignCenter)

        self.afd_horizontalLayout.addWidget(self.vis_label)

        self.vis_btn = QPushButton(self.gridWidget)
        self.vis_btn.setObjectName(u"vis_btn")
        sizePolicy4.setHeightForWidth(self.vis_btn.sizePolicy().hasHeightForWidth())
        self.vis_btn.setSizePolicy(sizePolicy4)
        self.vis_btn.setFont(font2)
        self.vis_btn.setStyleSheet(u"background-color:rgb(255, 255, 255);")

        self.afd_horizontalLayout.addWidget(self.vis_btn)


        self.etc_verticalLayout.addLayout(self.afd_horizontalLayout)

        self.afd_horizontalLayout_2 = QHBoxLayout()
        self.afd_horizontalLayout_2.setSpacing(6)
        self.afd_horizontalLayout_2.setObjectName(u"afd_horizontalLayout_2")
        self.vis_result = QLabel(self.gridWidget)
        self.vis_result.setObjectName(u"vis_result")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.vis_result.sizePolicy().hasHeightForWidth())
        self.vis_result.setSizePolicy(sizePolicy5)
        font3 = QFont()
        font3.setFamilies([u"Noto Sans KR Medium"])
        font3.setPointSize(50)
        self.vis_result.setFont(font3)
        self.vis_result.setStyleSheet(u"background-color:rgb(27,49,70);\n"
"color: #ffffff;")
        self.vis_result.setAlignment(Qt.AlignCenter)

        self.afd_horizontalLayout_2.addWidget(self.vis_result)


        self.etc_verticalLayout.addLayout(self.afd_horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(self.gridWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy6)
        font4 = QFont()
        font4.setFamilies([u"Noto Sans"])
        font4.setPointSize(9)
        self.buttonBox.setFont(font4)
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

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Setting", None))
        self.target_setting_label.setText(QCoreApplication.translate("Dialog", u"  \ud0c0\uac9f \uc138\ud305", None))
        self.load_img.setText(QCoreApplication.translate("Dialog", u"\uc774\ubbf8\uc9c0 \ubd88\ub7ec\uc624\uae30", None))
        self.image_label.setText("")
        self.target_list_label.setText(QCoreApplication.translate("Dialog", u"   \ud0c0\uac9f \ub9ac\uc2a4\ud2b8", None))
        self.value_label.setText(QCoreApplication.translate("Dialog", u"   \u03b1 \uadf8\ub798\ud504", None))
        self.setting_label.setText(QCoreApplication.translate("Dialog", u"   \uac00\uc2dc\uac70\ub9ac \ucd9c\ub825", None))
        self.vis_label.setText(QCoreApplication.translate("Dialog", u"\uac00\uc2dc\uac70\ub9ac", None))
        self.vis_btn.setText(QCoreApplication.translate("Dialog", u"\ucd9c\ub825", None))
        self.vis_result.setText(QCoreApplication.translate("Dialog", u"- km", None))
    # retranslateUi

