# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1024)
        MainWindow.setMinimumSize(QtCore.QSize(1920, 0))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1024))
        MainWindow.setStatusTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(1920, 1024))
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1921, 551))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 1919, 549))
        self.image_label.setText("")
        self.image_label.setScaledContents(True)
        self.image_label.setObjectName("image_label")
        self.capture_label = QtWidgets.QLabel(self.centralwidget)
        self.capture_label.setGeometry(QtCore.QRect(0, 550, 640, 440))
        self.capture_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.capture_label.setFont(font)
        self.capture_label.setLineWidth(0)
        self.capture_label.setAlignment(QtCore.Qt.AlignCenter)
        self.capture_label.setObjectName("capture_label")
        self.graph_label = QtWidgets.QLabel(self.centralwidget)
        self.graph_label.setGeometry(QtCore.QRect(640, 550, 640, 440))
        self.graph_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.graph_label.setFont(font)
        self.graph_label.setAlignment(QtCore.Qt.AlignCenter)
        self.graph_label.setObjectName("graph_label")
        self.print_label = QtWidgets.QLabel(self.centralwidget)
        self.print_label.setGeometry(QtCore.QRect(1280, 550, 640, 440))
        self.print_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.print_label.setFont(font)
        self.print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.print_label.setObjectName("print_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setToolTipsVisible(True)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(False)
        self.statusbar.setMaximumSize(QtCore.QSize(0, 0))
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionstart = QtWidgets.QAction(MainWindow)
        self.actionstart.setObjectName("actionstart")
        self.menuFile.addAction(self.actionstart)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.capture_label.setText(_translate("MainWindow", "캡쳐이미지"))
        self.graph_label.setText(_translate("MainWindow", "기울기 그래프"))
        self.print_label.setText(_translate("MainWindow", "소산계수 및 시정 출력"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionstart.setText(_translate("MainWindow", "start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

