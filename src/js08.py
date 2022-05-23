#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import sys
import os
import time
import random
import collections

import vlc
import numpy as np
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue

from PyQt5.QtGui import (QPixmap, QIcon, QPainter,
                         QColor, QPen, QFont)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFrame,
                             QVBoxLayout, QLabel, QInputDialog,
                             QMessageBox)
from PyQt5.QtCore import (Qt, pyqtSlot, pyqtSignal,
                          QRect, QTimer, QObject,
                          QThread, QPointF, QDateTime,
                          QPoint)
from PyQt5.QtChart import (QChartView, QLegend, QLineSeries,
                           QPolarChart, QValueAxis, QChart,
                           QDateTimeAxis)
from PyQt5 import uic

from login_view import LoginWindow
from video_thread_mp import producer
from js08_settings import JS08SettingWidget
from model import JS08Settings
from curve_thread import CurveThread
from clock import clockclock

os.environ['VLC_VERBOSE'] = '-1'


def resource_path(relative_path: str):
    """
    Get absolute path to resource, works for dev and for PyInstaller

    :param relative_path: Files to reference
    :return: os.path.join
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


class Consumer(QThread):
    poped = pyqtSignal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True


class VisibilityView(QChartView):

    def __init__(self, parent: QWidget, maxlen: int):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(600, 400)

        self.maxlen = maxlen
        self.epoch = []
        self.vis = []
        self.flag = False

        now = QDateTime.currentSecsSinceEpoch()
        str_now = str(now)
        sequence = '0'
        indicies = (10, 10)
        # print(sequence.join([str_now[:indicies[0] - 1], str_now[indicies[1]:]]))
        now = int(sequence.join([str_now[:indicies[0] - 1], str_now[indicies[1]:]]))

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
        year = current_time[:4]
        md = current_time[5:7] + current_time[8:10]
        # zeros = [(t * 1000, -1) for t in range(now - maxlen * 60, now, 60)]
        # self.data = collections.deque(zeros, maxlen=maxlen)

        self.setRenderHint(QPainter.Antialiasing)

        chart = QChart(title='Visibility')
        chart.legend().setVisible(False)

        self.setChart(chart)
        self.series = QLineSeries()
        chart.addSeries(self.series)

        axis_x = QDateTimeAxis()
        axis_x.setFormat('hh:mm')
        axis_x.setTitleText('Time')

        save_path = os.path.join(f'{JS08Settings.get("data_csv_path")}/PNM_9031RV_front/{year}')
        file = f'{save_path}/{md}.csv'
        if os.path.isfile(f'{file}') is False:

            zeros = [(t * 1000, -1) for t in range(now - maxlen * 60, now, 60)]
            self.data = collections.deque(zeros, maxlen=maxlen)

            left = QDateTime.fromMSecsSinceEpoch(self.data[0][0])
            right = QDateTime.fromMSecsSinceEpoch(self.data[-1][0])
            # left = QDateTime.fromMSecsSinceEpoch(now - 3600 * 24)
            # right = QDateTime.fromMSecsSinceEpoch(now * 1000)
            axis_x.setRange(left, right)
            chart.setAxisX(axis_x, self.series)
        else:

            result = pd.read_csv(f'{save_path}/{md}.csv')
            epoch = result['epoch'].tolist()
            vis_list = result['visibility'].tolist()

            # data = [(t * 1000, -1) for t in range(now - maxlen * 60, now, 60)]
            data = []

            for i in range(len(epoch)):
                # zeros = [(t * 1000, vis_list[i]) for t in range(now - maxlen * 60, now, 60)]
                data.append((epoch[i] * 1000, vis_list[i]))
                # if epoch[i] * 1000 in self.data[i]:
                #     print('!!!!!!!!!!')
                # self.data.append((epoch[i] * 1000, vis_list[i]))
            self.data = collections.deque(data, maxlen=maxlen)
            # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch[i])))

            left = QDateTime.fromMSecsSinceEpoch(self.data[0][0])
            right = QDateTime.fromMSecsSinceEpoch(self.data[-1][0])
            axis_x.setRange(left, right)
            chart.setAxisX(axis_x, self.series)

        axis_y = QValueAxis()
        axis_y.setRange(0, 20)
        # axis_y.setLabelsColor(QColor(255, 255, 255, 255))
        axis_y.setLabelFormat('%d')
        axis_y.setTitleText('Distance (km)')
        chart.setAxisY(axis_y, self.series)

        data_point = [QPointF(t, v) for t, v in self.data]
        self.series.append(data_point)

    @pyqtSlot(int, list)
    def refresh_stats(self, epoch: int, vis_list: list):

        # print(len(epoch), len(vis))

        # now = QDateTime.currentSecsSinceEpoch()

        if len(vis_list) == 0:
            vis_list = [0]
        prev_vis = self.prevailing_visibility(vis_list)
        self.data.append((epoch * 1000, prev_vis))

        left = QDateTime.fromMSecsSinceEpoch(self.data[0][0])
        right = QDateTime.fromMSecsSinceEpoch(self.data[-1][0])
        # left = QDateTime.fromMSecsSinceEpoch(now - 3600 * 24 * 1000)
        # right = QDateTime.fromMSecsSinceEpoch(now * 1000)
        self.chart().axisX().setRange(left, right)

        data_point = [QPointF(t, v) for t, v in self.data]
        self.series.replace(data_point)

        # for i in range(len(epoch)):
        #     # self.data.append((epoch[i], vis_list[i]))
        #     self.series.append(epoch[i], vis_list[i])

        # self.series.replace([QPointF(1649725277.0, 5)])

        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.data[-1][0] / 1000)))

        # self.axis_x.setRange(left, right)
        # self.chart.setAxisX(self.axis_x, self.series)

        # print(self.flag)
        # if self.flag is False:
        #     for i in range(len(epoch)):
        #         self.series.append(epoch[i], vis[i])
        #     self.flag = True
        # else:
        #     self.series.append(epoch[-1], vis[-1])

        # self.epoch = epoch
        # self.vis = vis

        # self.chart.removeSeries(self.series)

        # now = QDateTime.currentSecsSinceEpoch()
        # zeros = [(t * 1000, -1) for t in range(now - self.maxlen * 60, now, 60)]
        # self.data = collections.deque(zeros, maxlen=self.maxlen)

        # self.setRenderHint(QPainter.Antialiasing)

        # self.chart = QChart()
        # self.chart.legend().setVisible(False)
        # self.series.clear()
        # self.series = QLineSeries()

        # if len(self.epoch) == 0:
        #     for i in range(len(self.epoch)):
        #         print(i)
        #         self.series.append(self.epoch[i], self.vis[i])
        # else:
        #     self.series.append(self.epoch[-1], self.vis[-1])
        #     print(self.epoch[-1], self.vis[-1])

        # print(epoch, vis)
        # print(len(epoch), len(vis))

        # self.setChart(self.chart)
        # self.chart.addSeries(self.series)

    def prevailing_visibility(self, vis: list) -> float:
        if None in vis:
            return 0

        sorted_vis = sorted(vis, reverse=True)
        prevailing = sorted_vis[(len(sorted_vis) - 1) // 2]

        return prevailing

    def mouseDoubleClickEvent(self, event):
        # view = GraphRangeView()
        # view.exec_()
        print('?')


class DiscernmentView(QChartView):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(600, 400)

        chart = QPolarChart(title='Discernment Visibility')
        chart.legend().setAlignment(Qt.AlignRight)
        chart.legend().setMarkerShape(QLegend.MarkerShapeCircle)
        # chart.legend().setColor(QColor(255, 255, 255, 255))
        # chart.setTitleBrush(QColor(255, 255, 255, 255))
        # chart.setBackgroundBrush(QColor(0, 0, 0, 255))
        self.setChart(chart)

        # self.positives = QScatterSeries(name='Visibility')
        # self.negatives = QScatterSeries(name='Negative')
        # self.positives.setColor(QColor('green'))
        # self.negatives.setColor(QColor('red'))
        # self.positives.setMarkerSize(5)
        # self.negatives.setMarkerSize(10)
        # chart.addSeries(self.positives)
        # chart.addSeries(self.negatives)

        self.series = QLineSeries()
        self.series.setName('Visibility')
        self.series.setColor(QColor('green'))
        # self.series.append([QPointF(0, 0), QPoint(45, 10), QPoint(90, 5), QPointF(135, 5),
        #                     QPointF(180, 10), QPointF(225, 10), QPointF(270, 15), QPointF(315, 15),
        #                     QPointF(360, 0)])
        chart.addSeries(self.series)

        axis_x = QValueAxis()
        axis_x.setTickCount(9)
        # axis_x.setLabelsColor(QColor(255, 255, 255, 255))
        axis_x.setRange(0, 360)
        axis_x.setLabelFormat('%d \xc2\xb0')
        axis_x.setTitleText('Azimuth (deg)')
        axis_x.setTitleVisible(False)
        # chart.setAxisX(axis_x, self.positives)
        # chart.setAxisX(axis_x, self.negatives)
        chart.setAxisX(axis_x, self.series)

        axis_y = QValueAxis()
        # axis_y.setLabelsColor(QColor(255, 255, 255, 255))
        axis_y.setRange(0, 20)
        axis_y.setLabelFormat('%d km')
        axis_y.setTitleText('Distance (km)')
        axis_y.setTitleVisible(False)
        # chart.setAxisY(axis_y, self.positives)
        # chart.setAxisY(axis_y, self.negatives)
        chart.setAxisY(axis_y, self.series)

        # self.refresh_stats()

    def refresh_stats(self, visibility: dict):
        # az0 = 22.5      # 0 ~ 45°
        # az1 = 67.5      # 45 ~ 90°
        # az2 = 112.5     # 90 ~ 135°
        # az3 = 157.5     # 135 ~ 180°
        # az4 = 202.5     # 180 ~ 225°
        # az5 = 247.5     # 225 ~ 270°
        # az6 = 292.5     # 270 ~ 315°
        # az7 = 337.5     # 315 ~ 360°
        #
        # positives = []
        # negatives = [(0, 4), (0, 9), (0, 14),
        #              (45, 5), (45, 10), (45, 15),
        #              (90, 5), (90, 10), (90, 15),
        #              (135, 5), (135, 10), (135, 15),
        #              (180, 5), (180, 10), (180, 15),
        #              (225, 5), (225, 10), (225, 15),
        #              (270, 5), (270, 10), (270, 15),
        #              (315, 5), (315, 10), (315, 15)]
        # negatives = [(az0, 4), (az1, 7), (az2, 8), (az3, 6), (az4, 8), (az5, 7), (az6, 8), (az7, 9)]
        #
        # pos_point = [QPointF(a, d) for a, d in positives]
        # self.positives.replace(pos_point)
        # neg_point = [QPointF(a, d) for a, d in negatives]
        # self.negatives.replace(neg_point)

        a = random.randint(0, 20)
        b = random.randint(0, 20)
        c = random.randint(0, 20)
        d = random.randint(0, 20)
        e = random.randint(0, 20)
        f = random.randint(0, 20)
        g = random.randint(0, 20)
        h = random.randint(0, 20)

        self.series.replace([
            QPointF(0, float(visibility.get('front_N'))), QPointF(45, float(visibility.get('front_NE'))),
            QPointF(90, float(visibility.get('front_E'))), QPointF(135, float(visibility.get('rear_SE'))),
            QPointF(180, float(visibility.get('rear_S'))), QPointF(225, float(visibility.get('rear_SW'))),
            QPointF(270, float(visibility.get('rear_W'))), QPointF(315, float(visibility.get('front_NW'))),
            QPointF(360, float(visibility.get('front_N')))
        ])

    def random_refresh(self):
        # az0 = 22      # 0 ~ 45°
        # az1 = 67      # 45 ~ 90°
        # az2 = 112     # 90 ~ 135°
        # az3 = 157     # 135 ~ 180°
        # az4 = 202     # 180 ~ 225°
        # az5 = 247     # 225 ~ 270°
        # az6 = 292     # 270 ~ 315°
        # az7 = 337     # 315 ~ 360°

        a = random.randint(0, 20)
        b = random.randint(0, 20)
        c = random.randint(0, 20)
        d = random.randint(0, 20)
        e = random.randint(0, 20)
        f = random.randint(0, 20)
        g = random.randint(0, 20)
        h = random.randint(0, 20)
        # print(a, b, c, d, e, f, g, h)

        self.series.replace([QPointF(0, a), QPointF(45, b), QPointF(90, c), QPointF(135, d),
                             QPointF(180, e), QPointF(225, f), QPointF(270, g), QPointF(315, h),
                             QPointF(360, a)])
        # self.series.replace([QPointF(0, 5), QPoint(45, 6), QPoint(90, 7), QPointF(135, 8),
        #                      QPointF(180, 9), QPointF(225, 10), QPointF(270, 11), QPointF(315, 12),
        #                      QPointF(360, 13)])

    def mouseDoubleClickEvent(self, event):
        print('ddable click76')


# class PolarPlot(QChartView):
#     def __init__(self, parent: QWidget):
#         super().__init__(parent)
#         self.setRenderHint(QPainter.Antialiasing)
#         self.setMinimumSize(200, 200)
#         self.setMaximumSize(600, 400)
#
#         # self.main_widget = QWidget()
#         # self.setCentralWidget(self.main_widget)
#         #
#         chart = QChart()
#         chart.legend().setVisible(False)
#         # vbox = QVBoxLayout(self.main_widget)
#         # vbox.addWidget()
#
#         data = pd.DataFrame({'distance': [5, 10, 15, 20, 15, 10, 5, 10]})
#         compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
#         # index = []
#
#         dist = data['distance']
#         dist_list = dist.values.tolist()
#         min_value = min(dist_list)
#
#         # for i in range(len(dist_list)):
#         #     if dist_list[i] == min_value:
#         #         index.append(i)
#
#         self.fig, self.ax = plt.subplots(1, 1, subplot_kw={'projection': 'polar'})
#         self.ax.set_theta_zero_location('N')
#         self.ax.set_theta_direction(-1)
#
#         # for i in range(len(dist_list)):
#         #     if i in index:
#         #         plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(dist_list[i]), width=0.25 * np.pi, color=['red'])
#         #     else:
#         #         plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(dist_list[i]), width=0.25 * np.pi, color=['green'])
#
#         self.canvas = FigureCanvas(self.fig)
#         self.canvas.resize(600, 400)
#         # self.setChart(self.canvas)
#
#         self.ax.set_xlabel('Visibility', fontsize=10)
#         self.ax.set_rgrids(np.arange(0, 20, 5))
#         # self.ax.set_xticklabels(compass)
#         self.ax.set_rorigin(-10)
#
#         self.refresh_stats(dist_list)
#
#     @pyqtSlot(list)
#     def refresh_stats(self, distance: list):
#         self.ax.clear()
#
#         self.ax.set_theta_zero_location('N')
#         self.ax.set_theta_direction(-1)
#         self.ax.set_xlabel('Visibility', fontsize=10)
#
#         # self.ax.set_rgrids(np.arange(0, 20, 5))
#         self.ax.set_rgrids([0, 5, 10, 15, 20])
#         self.ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
#         self.ax.set_rorigin(-10)
#
#         # index = []
#         min_value = min(distance)
#
#         for i in range(len(distance)):
#             if distance[i] == min_value:
#                 # index.append(i)
#             # if i in index:
#                 plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(distance[i]), width=0.25 * np.pi, color=['red'])
#             else:
#                 plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(distance[i]), width=0.25 * np.pi, color=['green'])
#
#         self.canvas.draw()
#
#     def mouseDoubleClickEvent(self, event):
#         print('hi22')


class ThumbnailView(QMainWindow):

    def __init__(self, image_file_name: str, date: int):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'resources/thumbnail_view.ui')
        uic.loadUi(resource_path(ui_path), self)

        if os.path.isfile(
                f'{JS08Settings.get("image_save_path")}/vista/PNM_9031RV_front/{date}/{image_file_name}.png') and \
                os.path.isfile(f'{JS08Settings.get("image_save_path")}/vista/PNM_9031RV_rear/{date}/{image_file_name}.png'):

            front_image = f'{JS08Settings.get("image_save_path")}/vista/PNM_9031RV_front/{date}/{image_file_name}.png'
            rear_image = f'{JS08Settings.get("image_save_path")}/vista/PNM_9031RV_rear/{date}/{image_file_name}.png'

            self.front_image.setPixmap(
                QPixmap(front_image).scaled(self.width(), self.height(), Qt.KeepAspectRatio))
            self.rear_image.setPixmap(
                QPixmap(rear_image).scaled(self.width(), self.height(), Qt.KeepAspectRatio))

            # self.front_image.setPixmap(QPixmap(front_image))
            # self.rear_image.setPixmap(QPixmap(rear_image))
        else:
            print('no file')


class Js08MainWindow(QMainWindow):

    def __init__(self, q, _q):
        super().__init__()

        # login_window = LoginWindow()
        # login_window.exec_()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'resources/main_window.ui')
        uic.loadUi(resource_path(ui_path), self)
        # self.showFullScreen()

        self._plot = VisibilityView(self, 1440)
        # self._polar = PolarPlot(self)
        self._polar = DiscernmentView(self)

        self.view = None
        self.km_mile_convert = False
        self.visibility = 0
        self.pm_text = 0
        self.year_date = None
        self.epoch = []
        self.q_list = []
        self.q_list_scale = 1440
        self.data_date = []
        self.data_time = []
        self.data_vis = []

        self.blank_label_front = QLabel()
        self.blank_label_rear = QLabel()
        self.blank_label_front.setStyleSheet('background-color: #FFFFFF')
        self.blank_label_rear.setStyleSheet('background-color: #FFFFFF')
        # self.blank_label_front.raise_()
        # self.blank_label_rear.raise_()

        self.front_video_widget = VideoWidget(self)
        self.front_video_widget.on_camera_change(JS08Settings.get('front_main'))

        self.rear_video_widget = VideoWidget(self)
        self.rear_video_widget.on_camera_change(JS08Settings.get('rear_main'))

        self.video_horizontalLayout.addWidget(self.front_video_widget.video_frame)
        self.video_horizontalLayout.addWidget(self.rear_video_widget.video_frame)

        self.graph_horizontalLayout.addWidget(self._plot)
        self.polar_horizontalLayout.addWidget(self._polar)

        self.setting_button.enterEvent = self.btn_on
        self.setting_button.leaveEvent = self.btn_off

        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.clock)
        self.consumer.start()

        self.video_thread = CurveThread(_q)
        self.video_thread.poped.connect(self.print_data)
        self.video_thread.start()

        self.click_style = 'border: 1px solid red;'

        self.alert.clicked.connect(self.alert_test)

        self.c_vis_label.mousePressEvent = self.unit_convert
        self.p_vis_label.mousePressEvent = self.test

        self.label_1hour_front.mouseDoubleClickEvent = self.thumbnail_click1_front
        self.label_1hour_rear.mouseDoubleClickEvent = self.thumbnail_click1_rear
        self.label_2hour_front.mouseDoubleClickEvent = self.thumbnail_click2_front
        self.label_2hour_rear.mouseDoubleClickEvent = self.thumbnail_click2_rear
        self.label_3hour_front.mouseDoubleClickEvent = self.thumbnail_click3_front
        self.label_3hour_rear.mouseDoubleClickEvent = self.thumbnail_click3_rear

        self.setting_button.clicked.connect(self.setting_btn_click)
        self.azimuth_button.clicked.connect(self.azimuth_btn_click)
        # self.button.clicked.connect(self.button_click)

        self.show()

    def front_camera_pause(self, event):
        self.front_video_widget.media_player.pause()

    def rear_camera_pause(self, event):
        self.rear_video_widget.media_player.pause()

    def alert_test(self):
        self.alert.setIcon(QIcon('resources/red.png'))
        # a = [5, 10, 15, 20, 15, 10, 5, 10]
        # random.shuffle(a)
        # self._polar.refresh_stats(a)

    def reset_StyleSheet(self):
        self.label_1hour_front.setStyleSheet('')
        self.label_1hour_rear.setStyleSheet('')
        self.label_2hour_front.setStyleSheet('')
        self.label_2hour_rear.setStyleSheet('')
        self.label_3hour_front.setStyleSheet('')
        self.label_3hour_rear.setStyleSheet('')

    def thumbnail_view(self, file_name: str):
        if self.isFullScreen():
            self.view = ThumbnailView(file_name, int(file_name[2:8]))
            self.view.setGeometry(QRect(self.video_horizontalLayout.geometry().x(),
                                        self.video_horizontalLayout.geometry().y() + 21,
                                        self.video_horizontalLayout.geometry().width(),
                                        self.video_horizontalLayout.geometry().height()))
            self.view.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.view.setWindowModality(Qt.ApplicationModal)
            self.view.show()
            self.view.raise_()

        else:
            self.view = QMainWindow()

    def thumbnail_click1_front(self, e):

        name = self.label_1hour_time.text()[:2] + self.label_1hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_1hour_front.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_1hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click1_rear(self, e):
        name = self.label_1hour_time.text()[:2] + self.label_1hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_1hour_rear.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_1hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click2_front(self, e):
        name = self.label_2hour_time.text()[:2] + self.label_2hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_2hour_front.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_2hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click2_rear(self, e):
        name = self.label_2hour_time.text()[:2] + self.label_2hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_2hour_rear.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_2hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click3_front(self, e):
        name = self.label_3hour_time.text()[:2] + self.label_3hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_3hour_front.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_3hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click3_rear(self, e):
        name = self.label_3hour_time.text()[:2] + self.label_3hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_3hour_rear.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_3hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_show(self):
        self.monitoring_label.setText('   Monitoring')
        self.reset_StyleSheet()
        self.view.close()

    @pyqtSlot()
    def setting_btn_click(self):
        self.front_video_widget.media_player.stop()
        self.rear_video_widget.media_player.stop()
        self.consumer.pause()

        dlg = JS08SettingWidget()
        dlg.show()
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

        self.front_video_widget.media_player.play()
        self.rear_video_widget.media_player.play()
        self.consumer.resume()
        self.consumer.start()

    def azimuth_btn_click(self):
        # self.front_video_widget.flag_status()
        # self.rear_video_widget.flag_status()
        # self.front_video_widget.update()
        # self.rear_video_widget.update()
        print(self.front_video_widget.media_player.video_get_width(0))
        print(self.front_video_widget.media_player.video_get_size())

    def button_click(self):
        pass

    def btn_on(self, event):
        self.setting_button.setIcon(QIcon('resources/settings_on.png'))

    def btn_off(self, event):
        self.setting_button.setIcon(QIcon('resources/settings.png'))

    def unit_convert(self, event):
        if self.km_mile_convert:
            self.km_mile_convert = False
        elif self.km_mile_convert is False:
            self.km_mile_convert = True

    def test(self, event):
        print(self.front_video_widget.media_player.video_get_width(0))

    def get_data(self, year, month_day):
        """
        Prevailing visibility of front camera data

        :param year: Name of the year folder to access
        :param month_day: Name of the month and day folder to access
        :return: date, epoch, visibility in list type

        """

        save_path = os.path.join(f'{JS08Settings.get("data_csv_path")}/PNM_9031RV_front/{year}')

        if os.path.isfile(f'{save_path}/{month_day}.csv'):
            result = pd.read_csv(f'{save_path}/{month_day}.csv')
            data_datetime = result['date'].tolist()
            data_epoch = result['epoch'].tolist()
            data_visibility = result['visibility'].tolist()

            return data_datetime, data_epoch, data_visibility

        else:
            return [], [], []

    @pyqtSlot(dict)
    def print_data(self, visibility: dict):

        visibility_front = round(float(visibility.get('visibility_front')), 3)
        visibility_rear = round(float(visibility.get('visibility_rear')), 3)

        epoch = QDateTime.currentSecsSinceEpoch()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
        year = current_time[:4]
        md = current_time[5:7] + current_time[8:10]

        get_date, get_epoch, self.q_list = self.get_data(year, md)

        if len(self.q_list) == 0 or self.q_list_scale != len(self.q_list):
            self.q_list = []
            get_date = []
            get_epoch = []
            for i in range(self.q_list_scale):
                self.q_list.append(visibility_front)
            result_vis = np.mean(self.q_list)
        else:
            self.q_list.pop(0)
            self.q_list.append(visibility_front)
            result_vis = np.mean(self.q_list)

        if len(self.data_date) >= self.q_list_scale or len(self.data_vis) >= self.q_list_scale:
            self.data_date.pop(0)
            self.data_time.pop(0)
            self.data_vis.pop(0)

        self.data_date.append(current_time)
        self.data_time.append(epoch)
        self.data_vis.append(visibility_front)

        save_path_front = os.path.join(f'{JS08Settings.get("data_csv_path")}/PNM_9031RV_front/{year}')
        save_path_rear = os.path.join(f'{JS08Settings.get("data_csv_path")}/PNM_9031RV_rear/{year}')

        file_front = f'{save_path_front}/{md}.csv'
        file_rear = f'{save_path_rear}/{md}.csv'

        result_front = pd.DataFrame(columns=['date', 'epoch', 'visibility', 'W', 'NW', 'N', 'NE', 'E'])
        result_rear = pd.DataFrame(columns=['date', 'epoch', 'visibility', 'E', 'SE', 'S', 'SW', 'W'])

        if os.path.isfile(f'{file_front}') is False or os.path.isfile(f'{file_rear}') is False:
            os.makedirs(f'{save_path_front}', exist_ok=True)
            os.makedirs(f'{save_path_rear}', exist_ok=True)
            result_front.to_csv(f'{file_front}', mode='w', index=False)
            result_rear.to_csv(f'{file_rear}', mode='w', index=False)

        result_front['date'] = [self.data_date[-1]]
        result_front['epoch'] = [self.data_time[-1]]
        result_front['visibility'] = [self.data_vis[-1]]
        result_front['W'] = round(float(visibility.get('front_W')), 3)
        result_front['NW'] = round(float(visibility.get('front_NW')), 3)
        result_front['N'] = round(float(visibility.get('front_N')), 3)
        result_front['NE'] = round(float(visibility.get('front_NE')), 3)
        result_front['E'] = round(float(visibility.get('front_E')), 3)
        result_front.to_csv(f'{file_front}', mode='a', index=False, header=False)

        result_rear['date'] = [self.data_date[-1]]
        result_rear['epoch'] = [self.data_time[-1]]
        result_rear['visibility'] = visibility_rear
        result_rear['E'] = round(float(visibility.get('rear_E')), 3)
        result_rear['SE'] = round(float(visibility.get('rear_SE')), 3)
        result_rear['S'] = round(float(visibility.get('rear_S')), 3)
        result_rear['SW'] = round(float(visibility.get('rear_SW')), 3)
        result_rear['W'] = round(float(visibility.get('rear_W')), 3)
        result_rear.to_csv(f'{file_rear}', mode='a', index=False, header=False)

        self.visibility = round(float(result_vis), 3)

        self._plot.refresh_stats(epoch, self.q_list)
        self._polar.refresh_stats(visibility)
        # self._polar.random_refresh()
        # print(f'visibility: {visibility}')

    @pyqtSlot(str)
    def clock(self, data):
        self.blank_label_front.setGeometry(self.front_video_widget.geometry())
        self.blank_label_rear.setGeometry(self.rear_video_widget.geometry())

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data)))
        self.year_date = current_time[2:4] + current_time[5:7] + current_time[8:10]
        self.real_time_label.setText(current_time)
        # self.p_vis_label.setText(f'{self.pm_text} ㎍/㎥')

        if self.visibility != 0:
            ext = 3.912 / self.visibility
            hd = 89
            self.pm_text = round((ext * 1000 / 4 / 2.5) / (1 + 5.67 * ((hd / 100) ** 5.8)), 2)

        if self.km_mile_convert:
            self.c_vis_label.setText(f'{format(round(self.visibility / 1.609, 2), ",")} mile')

        elif self.km_mile_convert is False:
            self.c_vis_label.setText(f'{format(int(self.visibility * 1000), ",")} m')

        if current_time[-1:] == '0':
            self.thumbnail_refresh()
            # self._plot.refresh_stats(QDateTime.currentSecsSinceEpoch(), self.q_list)

        if int(self.visibility * 1000) <= JS08Settings.get('visibility_alert_limit'):
            self.alert.setIcon(QIcon('resources/red.png'))
        else:
            self.alert.setIcon(QIcon('resources/green.png'))

    def thumbnail_refresh(self):

        one_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600))
        two_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 2))
        three_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 3))
        # four_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 4))
        # five_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 5))
        # six_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 6))

        # one_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60))
        # two_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 2))
        # three_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 3))
        # four_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 4))
        # five_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 5))
        # six_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 6))

        self.label_1hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600)))
        self.label_2hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 2)))
        self.label_3hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 3)))
        # self.label_4hour_time.setText(time.strftime('%H:%M', time.localtime(time.time(w) - 3600 * 4)))
        # self.label_5hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 5)))
        # self.label_6hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 6)))

        # self.label_1hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60)))
        # self.label_2hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 2)))
        # self.label_3hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 3)))
        # self.label_4hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 4)))
        # self.label_5hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 5)))
        # self.label_6hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 6)))

        # self.label_1hour_front.setPixmap(
        #     QPixmap(
        #         f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{one_min_ago}.jpg')
        #         .scaled(self.label_1hour_front.width(), self.label_1hour_front.height() - 5, Qt.IgnoreAspectRatio))
        # self.label_1hour_rear.setPixmap(
        #     QPixmap(
        #         f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_rear/{self.year_date}/{one_min_ago}.jpg')
        #         .scaled(self.label_1hour_rear.width(), self.label_1hour_rear.height() - 5, Qt.IgnoreAspectRatio))
        # self.label_2hour_front.setPixmap(
        #     QPixmap(
        #         f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{two_min_ago}.jpg')
        #         .scaled(self.label_2hour_front.width(), self.label_2hour_front.height() - 5, Qt.IgnoreAspectRatio))
        # self.label_2hour_rear.setPixmap(
        #     QPixmap(
        #         f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_rear/{self.year_date}/{two_min_ago}.jpg')
        #         .scaled(self.label_2hour_rear.width(), self.label_2hour_rear.height() - 5, Qt.IgnoreAspectRatio))
        # self.label_3hour_front.setPixmap(
        #     QPixmap(
        #         f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{three_min_ago}.jpg')
        #         .scaled(self.label_3hour_front.width(), self.label_3hour_front.height() - 5, Qt.IgnoreAspectRatio))
        # self.label_3hour_rear.setPixmap(
        #     QPixmap(
        #         f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_rear/{self.year_date}/{three_min_ago}.jpg')
        #         .scaled(self.label_3hour_rear.width(), self.label_3hour_rear.height() - 5, Qt.IgnoreAspectRatio))

        if os.path.isfile(
                f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{one_hour_ago}.jpg'):
            self.label_1hour_front.setPixmap(
                QPixmap(
                    f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{one_hour_ago}.jpg')
                    .scaled(self.label_1hour_front.width(), self.label_1hour_front.height() - 5, Qt.IgnoreAspectRatio))
            self.label_1hour_rear.setPixmap(
                QPixmap(
                    f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_rear/{self.year_date}/{one_hour_ago}.jpg')
                    .scaled(self.label_1hour_rear.width(), self.label_1hour_rear.height() - 5, Qt.IgnoreAspectRatio))

        if os.path.isfile(
                f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{two_hour_ago}.jpg'):
            self.label_2hour_front.setPixmap(
                QPixmap(
                    f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{two_hour_ago}.jpg')
                    .scaled(self.label_2hour_front.width(), self.label_2hour_front.height() - 5, Qt.IgnoreAspectRatio))
            self.label_2hour_rear.setPixmap(
                QPixmap(
                    f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_rear/{self.year_date}/{two_hour_ago}.jpg')
                    .scaled(self.label_2hour_rear.width(), self.label_2hour_rear.height() - 5, Qt.IgnoreAspectRatio))

        if os.path.isfile(
                f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{three_hour_ago}.jpg'):
            self.label_3hour_front.setPixmap(
                QPixmap(
                    f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{three_hour_ago}.jpg')
                    .scaled(self.label_3hour_front.width(), self.label_3hour_front.height() - 5, Qt.IgnoreAspectRatio))
            self.label_3hour_rear.setPixmap(
                QPixmap(
                    f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_rear/{self.year_date}/{three_hour_ago}.jpg')
                    .scaled(self.label_3hour_rear.width(), self.label_3hour_rear.height() - 5, Qt.IgnoreAspectRatio))

        # self.label_1hour.setPixmap(
        #     QPixmap(f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{one_hour_ago}.jpg'))
        # self.label_2hour.setPixmap(
        #     QPixmap(f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{two_hour_ago}.jpg'))
        # self.label_3hour.setPixmap(
        #     QPixmap(f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{three_hour_ago}.jpg'))
        # self.label_4hour.setPixmap(
        #     QPixmap(f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{four_hour_ago}.jpg'))
        # self.label_5hour.setPixmap(
        #     QPixmap(f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{five_hour_ago}.jpg'))
        # self.label_6hour.setPixmap(
        #     QPixmap(f'{JS08Settings.get("image_save_path")}/resize/PNM_9031RV_front/{self.year_date}/{six_hour_ago}.jpg'))

    def keyPressEvent(self, e):
        """Override function QMainwindow KeyPressEvent that works when key is pressed"""
        if e.key() == Qt.Key_F:
            self.showFullScreen()
            self.thumbnail_refresh()
        if e.key() == Qt.Key_D:
            self.showNormal()
            self.thumbnail_refresh()

    def drawLines(self, qp):
        pen = QPen(Qt.white, 1, Qt.DotLine)

        qp.setPen(pen)
        qp.drawLine(240, 0, 240, 411)
        qp.drawLine(480, 0, 480, 411)
        qp.drawLine(720, 0, 720, 411)

    def closeEvent(self, event):
        self.consumer.terminate()
        self.video_thread.terminate()
        print(f'Close time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')


class VideoWidget(QWidget):
    """Video stream player using QVideoWidget"""

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.begin = QPoint()
        self.end = QPoint()
        self.flag = False

        args = [
            '--rtsp-frame-buffer-size=400000',
            '--quiet',
            # '--no-embedded-video',
            # '--no-video-deco',
            # '--no-qt-video-autoresize',
            # '--no-autoscale',
            # '--no-plugins-cache',
            # '--mouse-hide-timeout=0',
            # '--sout-x264-keyint=25',
            # '--sout-x264-ref=1'
        ]

        self.instance = vlc.Instance(args)
        self.instance.log_unset()

        self.media_player = self.instance.media_player_new()
        self.media_player.video_set_aspect_ratio('21:9')

        self.video_frame = QFrame()
        self.blank_label = QLabel()
        # self.blank_label.setStyleSheet('background-color: #83BCD4')

        if sys.platform == 'win32':
            self.media_player.set_hwnd(self.video_frame.winId())

        # layout = QVBoxLayout(self)
        # layout.addWidget(self.video_frame)

        # self.video_frame.paintEvent = self.paint

    def flag_status(self):
        if self.flag:
            self.flag = False
        elif self.flag is False:
            self.flag = True

    def paint(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        pen = QPen(Qt.white, 1, Qt.DotLine)

        qp.setPen(pen)
        qp.setFont(QFont('Arial', 6))

        if self.flag:
            # if self.end.x() >= 600:
            #     self.end.setX(600)
            #
            # elif self.end.x() <= 360:
            #     self.end.setX(360)

            self.end.setX(360)

            qp.drawLine(self.width() * 0.125, 0,
                        self.width() * 0.125, self.height())
            qp.drawLine(self.width() * 0.375, 0,
                        self.width() * 0.375, self.height())
            qp.drawLine(self.width() * 0.625, 0,
                        self.width() * 0.625, self.height())
            qp.drawLine(self.width() * 0.875, 0,
                        self.width() * 0.875, self.height())

            if self.geometry().x() == 0:
                qp.drawText(self.width() * 0.0625, 7, 'W')
                qp.drawText(self.width() * 0.25, 7, 'NW')
                qp.drawText(self.width() * 0.5, 7, 'N')
                qp.drawText(self.width() * 0.75, 7, 'NE')
                qp.drawText(self.width() * 0.9375, 7, 'E')

                qp.drawText(self.width() * 0.0625, self.height() - 2, 'W')
                qp.drawText(self.width() * 0.25, self.height() - 2, 'NW')
                qp.drawText(self.width() * 0.5, self.height() - 2, 'N')
                qp.drawText(self.width() * 0.75, self.height() - 2, 'NE')
                qp.drawText(self.width() * 0.9375, self.height() - 2, 'E')

            elif self.geometry().x() == 960:
                qp.drawText(self.width() * 0.0625, 7, 'E')
                qp.drawText(self.width() * 0.25, 7, 'SE')
                qp.drawText(self.width() * 0.5, 7, 'S')
                qp.drawText(self.width() * 0.75, 7, 'SW')
                qp.drawText(self.width() * 0.9375, 7, 'W')

                qp.drawText(self.width() * 0.0625, self.height() - 2, 'E')
                qp.drawText(self.width() * 0.25, self.height() - 2, 'SE')
                qp.drawText(self.width() * 0.5, self.height() - 2, 'S')
                qp.drawText(self.width() * 0.75, self.height() - 2, 'SW')
                qp.drawText(self.width() * 0.9375, self.height() - 2, 'W')

    @pyqtSlot(str)
    def on_camera_change(self, uri: str):
        if uri[:4] == 'rtsp':
            self.media_player.set_media(self.instance.media_new(uri))
            self.media_player.play()

        else:
            pass

    def mouseDoubleClickEvent(self, event):
        print('하윙')


class MainCtrl(QObject):
    front_camera_changed = pyqtSignal(str)
    rear_camera_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.front_target_prepared = False
        self.rear_target_prepared = False

        self.front_camera_changed.connect(self.decompose_front_targets)
        self.rear_camera_changed.connect(self.decompose_rear_targets)

    @pyqtSlot(str)
    def decompose_front_targets(self, _: str):
        self.front_target_prepared = False
        self.decompose_targets('front')
        self.front_target_prepared = True


if __name__ == '__main__':
    try:
        os.chdir(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())

    from PyQt5.QtWidgets import QApplication

    print(f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    mp.freeze_support()
    q = Queue()
    _q = Queue()

    _producer = producer

    p = Process(name='clock', target=clockclock, args=(q,), daemon=True)
    _p = Process(name='producer', target=_producer, args=(_q,), daemon=True)

    p.start()
    _p.start()

    os.makedirs(f'{JS08Settings.get("data_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS08Settings.get("target_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS08Settings.get("image_save_path")}', exist_ok=True)

    app = QApplication(sys.argv)
    screen_size = app.desktop().screenGeometry()
    width, height = screen_size.width(), screen_size.height()
    if width > 1920 or height > 1080:
        QMessageBox.warning(None, 'Warning', 'JS08 is based on FHD screen.')
    window = Js08MainWindow(q, _q)
    sys.exit(app.exec())
