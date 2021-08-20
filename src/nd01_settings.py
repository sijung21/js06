
import datetime
import sys
import os
import time
import math

import cv2
import numpy as np
import pandas as pd
# import PyQt5
# print(PyQt5.__version__)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog, QListWidgetItem, QFileDialog, QDockWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QPoint, QRect, Qt, QRectF, QSize, QCoreApplication, pyqtSlot, QTimer, QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem



class ND01_Setting_Widget(QMainWindow):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/settings.ui")
        uic.loadUi(ui_path, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    ui = ND01_Setting_Widget()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())

