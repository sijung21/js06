# !/usr/bin/env python3
"""
A sample implementation of a main window for JS-08.
"""
#
# This example illustrates the following techniques:
# * Layout design using Qt Designer
# * Open RTSP video source
#
#
#
# Reference: https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1

# pylint: disable=line-too-long
# pylint: disable-msg=E0611, E1101

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
import atexit
import traceback

import numpy as np
import pandas as pd
import pyqtgraph as pg
import matplotlib.pyplot as plt
from pymongo import MongoClient

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtGui import QPainter, QPen, QCursor
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMenu
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from cv2 import imwrite, destroyAllWindows, cvtColor, COLOR_BGR2RGB, split, merge, \
    VideoCapture, waitKey, error, resize, INTER_LINEAR
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView

import tflite_runtime.interpreter as tflite

# from save_db import SaveDB
# from video_thread import VideoThread
# from main_window import Ui_MainWindow
# from tflite_thread import TfliteThread


def error_log(error: str, path: str = "log", verbose: int = 3):
    """
    Write the error to a log file.

    :param error: Error string to print out. Required.
    :param path: A path of the log file.
        This parameter defaults to `log`.

    :param verbose: Verbosity level. 0 is quiet.
        This parameter defaults to `3`.

    :return:
    """
    if verbose == 3:
        print(error)

    current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))
    cur_day = time.strftime("%m%d", time.localtime(time.time()))
    with open(os.path.join(path, f"{cur_day}.txt"), "a") as txt:
        txt.write(f"[{current_time}] - {error}\n")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setEnabled(True)
        width = QApplication.primaryScreen().size().width()
        height = QApplication.primaryScreen().size().height()
        MainWindow.resize(width, height)
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(width, height))
        MainWindow.setMouseTracking(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(width, height))
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.blank_lbl = QtWidgets.QLabel(self.centralwidget)
        self.blank_lbl.setMinimumSize(QtCore.QSize(0, 0))
        self.blank_lbl.setMaximumSize(QtCore.QSize(16777215, 16777215))

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicView = QtWidgets.QGraphicsView(self.scene)
        self.graphicView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.video_item = QGraphicsVideoItem()
        self.scene.addItem(self.video_item)
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.video_item)
        self.verticalLayout.addWidget(self.graphicView)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webEngineView = QWebView()

        # self.verticalLayout.addWidget(self.video_item)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        # self.centralwidget.setLayout(self.gridLayout)

        self.menubar = QtWidgets.QMainWindow.menuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, width, 0.0195 * height))
        self.menubar.setAutoFillBackground(False)
        # self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuSource = QtWidgets.QMenu(self.menubar)
        self.menuSource.setObjectName("menuSource")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        MainWindow.setMenuBar(self.menubar)
        self.actionImage_File = QtWidgets.QAction(MainWindow)
        self.actionImage_File.setObjectName("actionImage_File")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionInference = QtWidgets.QAction(MainWindow)
        self.actionInference.setCheckable(True)
        self.actionInference.setChecked(False)
        self.actionInference.setObjectName("actionInference")
        self.actionEdit_target = QtWidgets.QAction(MainWindow)
        self.actionEdit_target.setCheckable(True)
        self.actionEdit_target.setObjectName("actionEdit_target")
        self.actionAWS = QtWidgets.QAction(MainWindow)
        self.actionAWS.setCheckable(True)
        self.actionAWS.setObjectName("actionAWS")
        self.actionHorizontal = QtWidgets.QAction(MainWindow)
        self.actionHorizontal.setCheckable(True)
        self.actionHorizontal.setObjectName("actionHorizontal")
        self.menuSource.addAction(self.actionExit)
        self.menuMode.addAction(self.actionEdit_target)
        self.menuMode.addSeparator()
        self.menuMode.addAction(self.actionInference)
        self.menuMode.addAction(self.actionAWS)
        self.menuMode.addAction(self.actionHorizontal)
        self.menubar.addAction(self.menuSource.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JS-06"))
        self.menuSource.setTitle(_translate("MainWindow", "File"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.actionImage_File.setText(_translate("MainWindow", "Image File"))
        self.actionImage_File.setStatusTip(_translate("MainWindow", "Open an image file"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit JS-06"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionInference.setText(_translate("MainWindow", "Inference"))
        self.actionInference.setShortcut(_translate("MainWindow", "I"))
        self.actionEdit_target.setText(_translate("MainWindow", "Edit_target"))
        self.actionEdit_target.setShortcut(_translate("MainWindow", "E"))
        self.actionAWS.setText(_translate("MainWindow", "AWS Sensor"))
        self.actionAWS.setShortcut(_translate("MainWindow", "A"))
        self.actionHorizontal.setText(_translate("MainWindow", "Horizontal line ranging"))
        self.actionHorizontal.setShortcut(_translate("MainWindow", "H"))

    def exit(self):
        sys.exit()


class VideoThread(QtCore.QThread):
    """
    Video output running as QThread
    QThread로 실행되는 OpenCV 비디오 출력
    """
    update_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, src: str = ""):
        super().__init__()
        self._run_flag = True
        self.cap = None
        self.src = src

    def run(self):
        try:
            time.sleep(0)
            if self.src == "":
                self.cap = VideoCapture(0)
            else:
                self.cap = VideoCapture(self.src)

            while self._run_flag:
                ret, cv_img = self.cap.read()
                if ret:
                    self.update_pixmap_signal.emit(cv_img)
                    waitKey(1)

            # Shut down capture system
            self.cap.release()
            destroyAllWindows()
            del cv_img

        except error:
            self.cap.release()
            destroyAllWindows()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class Js06MainWindow(Ui_MainWindow):
    """JS06 main window"""

    def __init__(self):
        super().__init__()
        self.target = []
        self.prime_x = []
        self.prime_y = []
        self.target_x = []
        self.target_y = []
        self.label_x = []
        self.label_y = []
        self.distance = []
        self.oxlist = []

        self.horizontal_y1 = None
        self.horizontal_y2 = None
        self.horizontal_y3 = None
        self.horizontal_flag = False

        self.camera_name = ""
        self.video_thread = None
        self.crop_imagelist100 = []
        self.target_process = False
        self.tflite_thread = None
        self.visibility = 0
        self.qtimer = None
        self.vis_km = 0
        self.vis_m = 0
        self.result = None
        self.crop_img = None

        self.save_db = None

        self.epoch = None
        self.list_flag = False

        # Draw target
        self.painter = None

        # Required for Target Plot function
        self._plot_ref_red = None
        self._plot_ref_green = None
        self.annotate = None
        self.ylabel = None
        self.xlabel = None

        self.fig = plt.Figure(figsize=(5, 4), dpi=100, facecolor=(0.9686, 0.9725, 0.9803), tight_layout=False)
        self.fig.suptitle("Target Distribution")
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='polar')
        pi = np.pi
        self.axes.set_thetamin(-90)
        self.axes.set_thetamax(90)
        self.axes.set_xticks([-pi / 2, -pi / 6, -pi / 3, 0, pi / 6, pi / 3, pi / 2])
        self.axes.set_theta_zero_location("N")
        self.axes.set_theta_direction(-1)
        self.ylabel = self.axes.set_ylabel("(km)", fontsize=7)
        self.ylabel.set_position((2, 0.2))
        self.ylabel.set_rotation(45)
        plt.rcParams.update({'font.size': 7})

        # TODO(Kyungwon): Set adequate action for the exception.
        self.filepath = os.path.join(os.getcwd(), "target")
        self.filepath_log = os.path.join(os.getcwd(), "log")
        try:
            # TODO(Jongjin): Replace InfluxDB with installation form or the other.
            os.startfile("influxd.exe")
            os.makedirs(self.filepath, exist_ok=True)
            os.makedirs(self.filepath_log, exist_ok=True)
        except OSError:
            pass

    def setupUi(self, MainWindow: QMainWindow):
        try:
            super().setupUi(MainWindow)

            # Link the webEngineView widget to the address below.
            self.webEngineView.load(
                QUrl(
                    "http://localhost:3000/d/TWQ9hKoGz/visibility?orgId=1&from=now-3h&to=now&refresh=5s&kiosk"
                ))
            self.open_cam()
            self.update_plot()

            ##
            # pg.setConfigOption('background', 'w')
            # plot = pg.plot()
            # plot.setAspectLocked()
            # plot.addLine(x=0, pen=0.2)
            # plot.addLine(y=0, pen=0.2)
            #
            # for r in range(2, 20, 2):
            #     circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            #     circle.setPen(pg.mkPen(0.3))
            #     plot.addItem(circle)
            #
            # theta = np.linspace(0, 1 * np.pi, 50)
            # radius = np.random.normal(loc=10, size=50)
            #
            # x = radius * np.cos(theta)
            # y = radius * np.sin(theta)
            # plot.plot(x, y)
            # plot.resize(600, 300)
            ##

            self.actionEdit_target.triggered.connect(self.target_mode)
            self.actionHorizontal.triggered.connect(self.replace_horizontal)
            self.horizontalLayout.addWidget(self.canvas, 0)
            self.horizontalLayout.addWidget(self.webEngineView, 1)

            # Event
            self.blank_lbl.mousePressEvent = self.mousePressEvent
            self.blank_lbl.mouseMoveEvent = self.mouseMoveEvent
            self.blank_lbl.mouseReleaseEvent = self.mouseReleaseEvent
            self.blank_lbl.contextMenuEvent = self.contextMenuEvent
            self.blank_lbl.paintEvent = self.paintEvent
        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def update_plot(self):
        """Update Target Plot with read information."""
        try:
            plot_x = np.array(self.prime_x) * np.pi / 2

            # Clear Target Plot canvas and redraw.
            self.axes.clear()
            self.plot_canvas()

            # pylint: disable=invalid-name
            for i, xy in enumerate(zip(plot_x, self.distance), start=0):
                if self.oxlist[i] == 0:
                    self._plot_ref_red, = self.axes.plot(plot_x[i], self.distance[i], 'ro')
                else:
                    self._plot_ref_green, = self.axes.plot(plot_x[i], self.distance[i], 'go')

            self.canvas.draw()

            # if self.save_db is not None:
            #     self.save_db.c_visibility = self.vis_m

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def plot_canvas(self):
        """Target Plot Axes"""
        try:
            pi = np.pi

            self.axes.set_thetamin(-90)
            self.axes.set_thetamax(90)
            self.axes.set_xticks([-pi / 2, -pi / 6, -pi / 3, 0, pi / 6, pi / 3, pi / 2])
            self.axes.set_theta_zero_location("N")
            self.axes.set_theta_direction(-1)
            self.ylabel = self.axes.set_ylabel("(km)", fontsize=7)
            self.ylabel.set_position((2, 0.2))
            self.ylabel.set_rotation(45)
            self.xlabel = self.axes.set_xlabel(f"Visibility: {self.visibility}", fontsize=20)
            plt.rcParams.update({'font.size': 7})

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def open_cam(self):
        """Get video from Hanwha PNM-9030V"""
        ADD = "rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp"
        self.camera_name = "PNM-9030V"

        # Create the video capture thread
        self.player.setMedia(QMediaContent(QUrl(ADD)))
        self.player.play()
        self.blank_lbl.raise_()

        self.video_thread = VideoThread(ADD)
        self.video_thread.update_pixmap_signal.connect(self.convert_cv_qt)
        self.video_thread.start()

        self.get_target()

        self.qtimer = QTimer()
        self.qtimer.setInterval(2000)
        self.qtimer.timeout.connect(self.inference_clicked)
        self.qtimer.start()

    def convert_cv_qt(self, cv_img):
        try:
            rgb_image = cvtColor(cv_img, COLOR_BGR2RGB)
            self.crop_image(rgb_image)
            self.epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            self.restoration()

            if self.epoch[-2:] == "00":
                self.save_frame(cv_img, self.epoch)
                self.save_target_frame(self.epoch)
        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def paintEvent(self, event):
        self.painter = QPainter(self.blank_lbl)
        self.draw_rect(self.painter)

        ############################
        if self.horizontal_flag:
            self.painter.setPen(QPen(Qt.black, 2, Qt.DotLine))
            self.x1 = self.painter.drawLine(self.blank_lbl.width() * (1 / 4), 0,
                                            self.blank_lbl.width() * (1 / 4), self.blank_lbl.height())
            self.x2 = self.painter.drawLine(self.blank_lbl.width() * (1 / 2), 0,
                                            self.blank_lbl.width() * (1 / 2), self.blank_lbl.height())
            self.x3 = self.painter.drawLine(self.blank_lbl.width() * (3 / 4), 0,
                                            self.blank_lbl.width() * (3 / 4), self.blank_lbl.height())

            self.y1 = self.painter.drawLine(0, self.horizontal_y1, self.blank_lbl.width(), self.horizontal_y1)
            self.y2 = self.painter.drawLine(0, self.horizontal_y2, self.blank_lbl.width(), self.horizontal_y2)
            self.y3 = self.painter.drawLine(0, self.horizontal_y3, self.blank_lbl.width(), self.horizontal_y3)
        else:
            self.x1 = None
            self.x2 = None
            self.x3 = None
            self.y1 = None
            self.y2 = None
            self.y3 = None
        ############################

        self.painter.end()

    def draw_rect(self, qp):
        setGreen = QPen(Qt.green, 3)
        setRed = QPen(Qt.red, 3)

        if self.target_x:
            for name, x, y in zip(self.target, self.label_x, self.label_y):
                if self.oxlist[self.label_x.index(x)] == 0:
                    qp.setPen(QPen(Qt.red, 2))
                else:
                    qp.setPen(QPen(Qt.green, 2))
                qp.drawRect(x - (25 / 4), y - (25 / 4), 25 / 2, 25 / 2)
                qp.drawText(x - 4, y - 10, f"{name}")

            ############################
            if self.tflite_thread and self.horizontal_flag:
                if self.oxlist[0] + self.oxlist[1] + self.oxlist[2] > 1:
                    # 5000~10000m target visible.
                    qp.setPen(setGreen)
                    self.rec1_1 = qp.drawRect(0, 0, self.blank_lbl.width() * (1 / 4), self.horizontal_y1 - 1)
                else:
                    # 5000~10000m target invisible.
                    qp.setPen(setRed)
                    self.rec1_1 = qp.drawRect(0, 0, self.blank_lbl.width() * (1 / 4), self.horizontal_y1 - 1)

                    qp.setPen(setRed)
                    self.rec1_2 = qp.drawRect(0, self.horizontal_y1,
                                self.blank_lbl.width() * (1 / 4), self.horizontal_y2 - self.horizontal_y1 - 1)

                    if self.oxlist[3] + self.oxlist[4] + self.oxlist[5] > 1:
                        # 2500~5000m target visible.
                        qp.setPen(setGreen)
                        self.rec1_2 = qp.drawRect(0, self.horizontal_y1,
                                    self.blank_lbl.width() * (1 / 4), self.horizontal_y2 - self.horizontal_y1 - 1)
                    else:
                        # 2500~5000m target invisible.
                        qp.setPen(setRed)
                        self.rec1_3 = qp.drawRect(0, self.horizontal_y2,
                                    self.blank_lbl.width() * (1 / 4), self.horizontal_y3 - self.horizontal_y2 - 1)

                        qp.setPen(setRed)
                        self.rec1_3 = qp.drawRect(0, self.horizontal_y2,
                                    self.blank_lbl.width() * (1 / 4), self.horizontal_y3 - self.horizontal_y2 - 1)

                        if self.oxlist[6] + self.oxlist[7] + self.oxlist[8] > 1:
                            # 800~2500m target visible.
                            qp.setPen(setGreen)
                            self.rec1_3 = qp.drawRect(0, self.horizontal_y2,
                                        self.blank_lbl.width() * (1 / 4), self.horizontal_y3 - self.horizontal_y2 - 1)
                        else:
                            # 800~2500m target invisible, RVR Sensor ON.
                            qp.setPen(setRed)
                            self.rec1_3 = qp.drawRect(0, self.horizontal_y2,
                                        self.blank_lbl.width() * (1 / 4), self.horizontal_y3 - self.horizontal_y2 - 1)
                            self.rec1_4 = qp.drawRect(0, self.horizontal_y3,
                                        self.blank_lbl.width() * (1 / 4), self.blank_lbl.height() - self.horizontal_y3 - 1)
            ############################

    def mousePressEvent(self, event):
        try:
            y = int(event.pos().y() / self.graphicView.geometry().height() * self.video_item.nativeSize().height())
            x = int(event.pos().x() / self.graphicView.geometry().width() * self.video_item.nativeSize().width())

            for i in range(len(self.target)):
                if self.target_x[i] - 25 < x < self.target_x[i] + 25 and \
                                        self.target_y[i] - 25 < y < self.target_y[i] + 25:
                    if self.oxlist[i] == 0:
                        self.oxlist[i] = 1
                    else:
                        self.oxlist[i] = 0

            for i in range(len(self.target)):
                self.target[i] = i + 1
            print(self.target)

            if not self.target_process:
                return

            if event.buttons() == Qt.LeftButton:
                text, ok = QInputDialog.getText(self.centralwidget, 'Add Target', 'Distance (km)')
                if ok:
                    self.target_x.append(x)
                    self.target_y.append(y)
                    self.distance.append(float(text))
                    self.target.append(str(len(self.target_x)))
                    self.oxlist.append(0)
                    print(f"Target position: {self.target_x[-1]}, {self.target_y[-1]}")
                    self.coordinator()
                    self.save_target()
                    self.get_target()

            if event.buttons() == Qt.RightButton:
                # pylint: disable=invalid-name
                text, ok = QInputDialog.getText(self.centralwidget, 'Remove Target', 'Enter target number to remove')
                text = int(text)
                if ok:
                    if len(self.prime_x) >= 1:
                        del self.target[text - 1]
                        del self.prime_x[text - 1]
                        del self.prime_y[text - 1]
                        del self.label_x[text - 1]
                        del self.label_y[text - 1]
                        del self.distance[text - 1]
                        del self.oxlist[text - 1]
                        print(f"[Target {text}] remove.")
                        self.save_target()

                    else:
                        print("There are no targets to remove.")

        except AttributeError:
            pass

        except ValueError:
            print("Invalid distance input value.")

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.horizontal_flag:
            if self.horizontal_y1 - 5 < event.pos().y() < self.horizontal_y1 + 5:
                self.horizontal_y1 = event.pos().y()
                MainWindow.setCursor(QCursor(Qt.ClosedHandCursor))

            if self.horizontal_y2 - 5 < event.pos().y() < self.horizontal_y2 + 5:
                self.horizontal_y2 = event.pos().y()
                MainWindow.setCursor(QCursor(Qt.ClosedHandCursor))

            if self.horizontal_y3 - 5 < event.pos().y() < self.horizontal_y3 + 5:
                self.horizontal_y3 = event.pos().y()
                MainWindow.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event):
        MainWindow.setCursor(QCursor(Qt.ArrowCursor))

    def contextMenuEvent(self, event):
        contextMenu = QMenu(MainWindow)
        actionHello = contextMenu.addAction("Hello")
        action = contextMenu.exec_(MainWindow.mapToGlobal(event.pos()))
        if action == actionHello:
            print("Hello")

    def target_mode(self):
        """Set target image modification mode."""
        try:
            self.save_target()
            if self.target_process:
                self.target_process = False
                self.save_target()

            else:
                self.target_process = True
                self.actionInference.setChecked(False)
                if self.tflite_thread is not None:
                    self.tflite_thread.stop()
                    self.tflite_thread = None
                print("타겟 설정 모드로 전환합니다.")
                self.save_target()

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def get_target(self):
        """Read target information from a file"""
        try:
            # client = MongoClient("mongodb://localhost:27017")
            # my_db = client['config']
            # my_col = my_db['target']
            # my_list = my_col.find()
            # # for x in my_list:
            # #     print(x)
            # # result = list(x)
            #
            # print(self.camera_name)

            result = pd.read_csv(f"target/{self.camera_name}.csv")
            if os.path.isfile(f"target/{self.camera_name}.csv"):
                print(self.camera_name)
                self.target = result.target.tolist()
                self.prime_x = result.x.tolist()
                self.prime_y = result.y.tolist()
                self.label_x = result.label_x.tolist()
                self.label_y = result.label_y.tolist()
                self.distance = result.distance.tolist()
                self.oxlist = [0 for i in range(len(self.prime_x))]
                print("Load csv file.")

                print(self.target)
                print(self.prime_x)
                print(self.prime_y)

            elif os.path.isfile(f"target/{self.camera_name}.csv") is False:
                print("No csv file.")

            else:
                print("Unable to load csv file.")

        except AttributeError:
            err = traceback.format_exc()
            error_log(str(err))
            print(err)

    def save_target(self):
        """Save the target information for each camera."""
        try:
            if self.prime_x:
                col = ["target", "x", "y", "label_x", "label_y", "distance", "discernment"]
                self.result = pd.DataFrame(columns=col)
                self.result["target"] = self.target
                self.result["x"] = self.prime_x
                self.result["y"] = self.prime_y
                self.result["label_x"] = [round(x * self.graphicView.geometry().width() /
                                                self.video_item.nativeSize().width(), 3) for x in self.target_x]
                self.result["label_y"] = [round(y * self.graphicView.geometry().height() /
                                                self.video_item.nativeSize().height(), 3) for y in self.target_y]
                self.result["distance"] = self.distance
                self.result["discernment"] = self.oxlist
                self.result.to_csv(f"{self.filepath}/{self.camera_name}.csv", mode="w", index=False)

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def coordinator(self):
        """Normalize the coordinate value of the image target to -1 to 1."""
        try:
            self.prime_y = [y / self.video_item.nativeSize().height() for y in self.target_y]
            self.prime_x = [2 * x / self.video_item.nativeSize().width() - 1 for x in self.target_x]
        except:
            err = traceback.format_exc()
            error_log(str(err))

    def restoration(self):
        """Reinstate coordinate values."""
        try:
            self.target_x = [self.f2i((x + 1) * self.video_item.nativeSize().width() / 2) for x in self.prime_x]
            self.target_y = [self.f2i(y * self.video_item.nativeSize().height()) for y in self.prime_y]
        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    @staticmethod
    def f2i(num: float):
        """Convert float to int with round off."""
        try:
            return int(num + 0.5)
        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def save_target_frame(self, epoch: str):
        """Save 100x100 target frame in camera image"""
        try:
            for i in range(len(self.target_x)):
                image_path = os.path.join(self.filepath, "image", "100x100", f"target{i + 1}")
                if not os.path.isdir(image_path):
                    os.makedirs(image_path)
                if not os.path.isfile(f"{image_path}/target_{i + 1}_{epoch}.jpg"):
                    b, g, r = split(self.crop_imagelist100[i])
                    if self.oxlist[i] == 1:
                        imwrite(f"{image_path}/target_{i + 1}_{epoch}_Y.jpg", merge([r, g, b]))
                    else:
                        imwrite(f"{image_path}/target_{i + 1}_{epoch}_N.jpg", merge([r, g, b]))
            del self.crop_imagelist100
            destroyAllWindows()
        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def save_frame(self, image: np.ndarray, epoch: str):
        """Save frame in camera image"""
        try:
            image_path = os.path.join(self.filepath, "image", "PNM", f"{epoch[2:6]}")
            file_name = f"{epoch}_{self.vis_m}"
            if not os.path.isdir(image_path):
                os.makedirs(image_path)
            if not os.path.isfile(f"{image_path}/{file_name}.jpg"):
                imwrite(f'{image_path}/{file_name}.jpg', image)
            del image
            del image_path
            destroyAllWindows()

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def crop_image(self, image: np.ndarray):
        """영상목표를 100x100으로 잘라내 리스트로 저장하고, 리스트를 tflite_thread 에 업데이트 한다."""
        try:
            new_crop_image = []
            # 영상목표를 100x100으로 잘라 리스트에 저장한다.
            for i in range(len(self.target_x)):
                self.crop_img = image[self.target_y[i] - 50: self.target_y[i] + 50,
                                self.target_x[i] - 50: self.target_x[i] + 50]
                new_crop_image.append(self.crop_img)

            self.crop_imagelist100 = new_crop_image

            # tflite_thread가 작동시 tflite_thread에 영상목표 리스트를 업데이트한다.
            if self.actionInference.isChecked() and self.tflite_thread is not None:
                self.tflite_thread.crop_imagelist100 = new_crop_image
            del image

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def inference_clicked(self):
        """모델 쓰레드를 제어한다."""
        try:
            self.graphicView.fitInView(self.video_item)
            self.blank_lbl.resize(self.graphicView.geometry().width(), self.graphicView.geometry().height())

            if self.horizontal_y1 is None:
                self.horizontal_y1 = self.blank_lbl.height() * (1 / 4)
                self.horizontal_y2 = self.blank_lbl.height() * (1 / 2)
                self.horizontal_y3 = self.blank_lbl.height() * (3 / 4)

            if self.actionInference.isChecked():
                self.actionEdit_target.setChecked(False)
                self.update_plot()

                self.target_process = False

                if self.tflite_thread is None:
                    if not self.prime_x:
                        return
                    print("모델적용을 시작합니다.")

                    self.tflite_thread = TfliteThread(self.crop_imagelist100)
                    self.tflite_thread.run_flag = True
                    self.tflite_thread.update_oxlist_signal.connect(self.get_visibility)
                    self.tflite_thread.start()

                    # self.save_db = SaveDB()
                    # if not self.save_db.flag:
                    #     self.save_db.flag = True
                    #     self.save_db.start()

            else:
                if self.tflite_thread is None:
                    return
                if self.tflite_thread.run_flag:
                    print("모델적용을 중지합니다.")
                    self.tflite_thread.stop()
                    self.tflite_thread = False

                    # if self.save_db.flag:
                    #     self.save_db.stop()
                    #     self.save_db.flag = False
                    #     self.save_db = None

        except:  # pylint: disable=bare-except
            err = traceback.format_exc()
            error_log(str(err))

    def replace_horizontal(self):
        # print("Replace horizontal line.")
        if self.actionHorizontal.isChecked():
            self.horizontal_flag = True
        else:
            self.horizontal_flag = False

    def get_visibility(self, oxlist):
        """크롭한 이미지들을 모델에 돌려 결과를 저장하고 보이는것들 중 가장 먼 거리를 출력한다."""
        try:
            res = [self.distance[x] for x, y in enumerate(oxlist) if y == 1]
            self.vis_km = max(res)

            if res is None:
                self.vis_km = 0
            elif res:
                self.vis_km = round(max(res), 2)
                self.vis_m = int(self.vis_km * 1000)
                self.visibility = str(self.vis_km) + " km"

            self.oxlist = oxlist
            self.save_target()

            return self.oxlist

        except ValueError:
            err = traceback.format_exc()
            error_log(str(err))
            pass


def close_func():
    os.system("TASKKILL /F /IM influxd.exe")


class TfliteThread(QtCore.QThread):
    update_oxlist_signal = QtCore.pyqtSignal(list)

    def __init__(self, crop_imagelist100=None):
        super().__init__()
        if crop_imagelist100 is None:
            crop_imagelist100 = []
        self.run_flag = False
        self.crop_imagelist100 = crop_imagelist100
        self.oxlist = []
        self.interpreter = tflite.Interpreter("Model/JS06N21011201.tflite")
        self.interpreter.allocate_tensors()

    def __del__(self):
        self.wait()

    def set_input_tensor(self, interpreter, image):
        """Feed input to the model"""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image
        image = []
        tensor_index = []

    def classify_image(self, interpreter, image):
        """Returns a sorted array of classification results."""
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))
        predict = np.argmax(output)
        output_details.clear()

        return predict, output[predict]

    def run(self):
        """영상목표를 모델에 넣어 결과를 전송한다."""
        while self.run_flag:
            if self.crop_imagelist100:
                for index, image in enumerate(self.crop_imagelist100):
                    image = resize(image, dsize=(224, 224), interpolation=INTER_LINEAR)
                    _, height, width, _ = self.interpreter.get_input_details()[0]['shape']
                    label_id, prob = self.classify_image(self.interpreter, image)
                    self.oxlist.append(label_id)
                    image = []
                self.update_oxlist_signal.emit(self.oxlist)
                self.oxlist = []
                image = []
            time.sleep(5)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.run_flag = False
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Js06MainWindow()  # pylint: disable-msg=I1101
    ui.setupUi(MainWindow)
    MainWindow.show()
    atexit.register(close_func)
    sys.exit(app.exec_())
