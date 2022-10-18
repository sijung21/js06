# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rtsp_setting.ui'
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
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(493, 416)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)

        self.front_rtsp_lineEdit = QLineEdit(self.groupBox)
        self.front_rtsp_lineEdit.setObjectName(u"front_rtsp_lineEdit")

        self.gridLayout_4.addWidget(self.front_rtsp_lineEdit, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_3, 2, 0, 1, 1)

        self.front_resize_rtsp_lineEdit = QLineEdit(self.groupBox)
        self.front_resize_rtsp_lineEdit.setObjectName(u"front_resize_rtsp_lineEdit")

        self.gridLayout_4.addWidget(self.front_resize_rtsp_lineEdit, 2, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)

        self.front_model_lineEdit = QLineEdit(self.groupBox)
        self.front_model_lineEdit.setObjectName(u"front_model_lineEdit")

        self.gridLayout_4.addWidget(self.front_model_lineEdit, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_5, 1, 0, 1, 1)

        self.rear_model_lineEdit = QLineEdit(self.groupBox_2)
        self.rear_model_lineEdit.setObjectName(u"rear_model_lineEdit")

        self.gridLayout_5.addWidget(self.rear_model_lineEdit, 0, 1, 1, 1)

        self.rear_rtsp_lineEdit = QLineEdit(self.groupBox_2)
        self.rear_rtsp_lineEdit.setObjectName(u"rear_rtsp_lineEdit")

        self.gridLayout_5.addWidget(self.rear_rtsp_lineEdit, 1, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_6, 2, 0, 1, 1)

        self.rear_resize_rtsp_lineEdit = QLineEdit(self.groupBox_2)
        self.rear_resize_rtsp_lineEdit.setObjectName(u"rear_resize_rtsp_lineEdit")

        self.gridLayout_5.addWidget(self.rear_resize_rtsp_lineEdit, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_6 = QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_7, 0, 0, 1, 1)

        self.data_path_lineEdit = QLineEdit(self.groupBox_3)
        self.data_path_lineEdit.setObjectName(u"data_path_lineEdit")

        self.gridLayout_6.addWidget(self.data_path_lineEdit, 0, 1, 1, 1)

        self.rgb_path_lineEdit = QLineEdit(self.groupBox_3)
        self.rgb_path_lineEdit.setObjectName(u"rgb_path_lineEdit")

        self.gridLayout_6.addWidget(self.rgb_path_lineEdit, 2, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_8, 1, 0, 1, 1)

        self.target_path_lineEdit = QLineEdit(self.groupBox_3)
        self.target_path_lineEdit.setObjectName(u"target_path_lineEdit")

        self.gridLayout_6.addWidget(self.target_path_lineEdit, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_10, 3, 0, 1, 1)

        self.image_path_lineEdit = QLineEdit(self.groupBox_3)
        self.image_path_lineEdit.setObjectName(u"image_path_lineEdit")

        self.gridLayout_6.addWidget(self.image_path_lineEdit, 3, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"JS-08 Setting", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Front Camera", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"RTSP", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Resize RTSP", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Model", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Rear Camera", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Model", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"RTSP", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Resize RTSP", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Path", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Data", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Target", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"RGB", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Image", None))
    # retranslateUi

