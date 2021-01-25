
import os
import sys
import time

import cv2
import numpy as np
import pandas as pd

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QPoint, QRect, Qt

from video_thread import VideoThread
from mainwindow import Ui_MainWindow

class Js06MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.camera_name = ""
        self.video_thread = None
        self.ipcam_start()

    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        super().setupUi(MainWindow)

    def ipcam_start(self):
        """Connect to webcam"""
        if self.video_thread is not None:
            self.video_thread.stop()

        self.camera_name = "PNM-9030V"
        # create the video capture thread
        self.video_thread = VideoThread('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
        # connect its signal to the update_image slot
        self.video_thread.update_pixmap_signal.connect(self.update_image)
        # start the thread
        self.video_thread.start()

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width, ch = rgb_image.shape

        self.label_width = self.image_label.width()
        self.label_height = self.image_label.height()

        bytes_per_line = ch * self.img_width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, self.img_width, self.img_height, bytes_per_line,
                                            QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), QtCore.Qt.KeepAspectRatio,
                                        QtCore.Qt.SmoothTransformation)
        return QtGui.QPixmap.fromImage(p)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Js06MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())