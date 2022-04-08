#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import collections
import sys
import os
import time

import vlc
import random
import numpy as np
import pandas as pd
import pyqtgraph as pg
import multiprocessing as mp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from multiprocessing import Process, Queue

from PyQt5.QtGui import (QPixmap, QIcon, QPainter,
                         QColor, QPaintEvent, QPen,
                         QFont)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFrame,
                             QVBoxLayout, QLabel, QGraphicsOpacityEffect,
                             QInputDialog)
from PyQt5.QtCore import (Qt, pyqtSlot, pyqtSignal,
                          QRect, QTimer, QObject,
                          QThread, QPointF, QDateTime,
                          QPoint)
from PyQt5.QtChart import (QChartView, QLegend, QLineSeries,
                           QPolarChart, QScatterSeries, QValueAxis,
                           QChart, QDateTimeAxis)
from PyQt5 import uic

from login_view import LoginWindow
from video_thread_mp import producer
from nd01_settings import ND01SettingWidget
from model import JS06Settings
from controller import JS08MainCtrl
from curve_thread import CurveThread


def clock(queue):
    """Real-time clock
    Current time to be expressed on JS-06

    :param queue: MultiProcessing Queue
    """
    while True:
        now = str(time.time())
        queue.put(now)
        time.sleep(1)


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

        self.epoch = None
        self.vis = None

        now = QDateTime.currentSecsSinceEpoch()
        zeros = [(t * 1000, -1) for t in range(now - maxlen * 60, now, 60)]
        self.data = collections.deque(zeros, maxlen=maxlen)

        self.setRenderHint(QPainter.Antialiasing)

        chart = QChart()
        chart.legend().setVisible(False)
        self.series = QLineSeries()

        self.setChart(chart)
        chart.addSeries(self.series)

        axis_x = QDateTimeAxis()
        axis_x.setFormat('hh:mm')
        axis_x.setTitleText('Time')
        # axis_x.setLabelsColor(QColor(255, 255, 255, 255))
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

        # data_point = [QPointF(t, v) for t, v in self.data]
        # self.series.append(data_point)

    @pyqtSlot(list, list)
    # def refresh_stats(self, epoch: int, vis_list: list):
    def refresh_stats(self, epoch: list, vis: list):

        # if len(data) == 0:
        #     vis_list = [0]
        # prev_vis = self.prevailing_visibility(vis_list)

        # for i in range(len(epoch)):
        #     self.data.append((epoch[i] * 1000, prev_vis))

        # self.data.append((epoch * 1000, prev_vis))
        # print(data)

        # self.series.append(epoch, vis)
        self.epoch = epoch
        self.vis = vis

        # self.data.append((1649141890000, 5))
        # self.data.append((1649144490000, 20))

        # left = QDateTime.fromMSecsSinceEpoch(self.data[0][0])
        # right = QDateTime.fromMSecsSinceEpoch(self.data[-1][0])
        # self.chart().axisX().setRange(left, right)
        #
        # data_point = [QPointF(t, v) for t, v in self.data]
        # self.series.replace(data_point)
        pass

    def prevailing_visibility(self, vis: list) -> float:
        if None in vis:
            return 0

        sorted_vis = sorted(vis, reverse=True)
        prevailing = sorted_vis[(len(sorted_vis) - 1) // 2]

        return prevailing

    def mouseDoubleClickEvent(self, event):
        print('hi')


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

        self.positives = QScatterSeries(name='Positive')
        self.negatives = QScatterSeries(name='Negative')
        self.positives.setColor(QColor('green'))
        self.negatives.setColor(QColor('red'))
        self.positives.setMarkerSize(10)
        self.negatives.setMarkerSize(10)
        chart.addSeries(self.positives)
        chart.addSeries(self.negatives)

        axis_x = QValueAxis()
        axis_x.setTickCount(9)
        # axis_x.setLabelsColor(QColor(255, 255, 255, 255))
        axis_x.setRange(0, 360)
        axis_x.setLabelFormat('%d \xc2\xb0')
        axis_x.setTitleText('Azimuth (deg)')
        axis_x.setTitleVisible(False)
        chart.setAxisX(axis_x, self.positives)
        chart.setAxisX(axis_x, self.negatives)

        axis_y = QValueAxis()
        # axis_y.setLabelsColor(QColor(255, 255, 255, 255))
        axis_y.setRange(0, 20)
        axis_y.setLabelFormat('%d km')
        axis_y.setTitleText('Distance (km)')
        axis_y.setTitleVisible(False)
        chart.setAxisY(axis_y, self.positives)
        chart.setAxisY(axis_y, self.negatives)

    def refresh_stats(self):
        az0 = 22.5      # 0 ~ 45°
        az1 = 67.5      # 45 ~ 90°
        az2 = 112.5     # 90 ~ 135°
        az3 = 157.5     # 135 ~ 180°
        az4 = 202.5     # 180 ~ 225°
        az5 = 247.5     # 225 ~ 270°
        az6 = 292.5     # 270 ~ 315°
        az7 = 337.5     # 315 ~ 360°

        positives = []
        # negatives = [(0, 4), (0, 9), (0, 14),
        #              (45, 5), (45, 10), (45, 15),
        #              (90, 5), (90, 10), (90, 15),
        #              (135, 5), (135, 10), (135, 15),
        #              (180, 5), (180, 10), (180, 15),
        #              (225, 5), (225, 10), (225, 15),
        #              (270, 5), (270, 10), (270, 15),
        #              (315, 5), (315, 10), (315, 15)]
        negatives = [(az0, 4), (az1, 7), (az2, 8), (az3, 6), (az4, 8), (az5, 7), (az6, 8), (az7, 9)]

        pos_point = [QPointF(a, d) for a, d in positives]
        self.positives.replace(pos_point)
        neg_point = [QPointF(a, d) for a, d in negatives]
        self.negatives.replace(neg_point)


class PolarPlot(QChartView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(600, 400)

        data = pd.DataFrame({'distance': [5, 10, 15, 20, 15, 10, 5, 10]})
        compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        # index = []

        dist = data['distance']
        dist_list = dist.values.tolist()
        min_value = min(dist_list)

        # for i in range(len(dist_list)):
        #     if dist_list[i] == min_value:
        #         index.append(i)

        self.fig, self.ax = plt.subplots(1, 1, subplot_kw={'projection': 'polar'})
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)

        # for i in range(len(dist_list)):
        #     if i in index:
        #         plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(dist_list[i]), width=0.25 * np.pi, color=['red'])
        #     else:
        #         plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(dist_list[i]), width=0.25 * np.pi, color=['green'])

        self.canvas = FigureCanvas(self.fig)
        self.canvas.resize(600, 400)

        self.ax.set_xlabel('Visibility', fontsize=10)
        self.ax.set_rgrids(np.arange(0, 20, 5))
        # self.ax.set_xticklabels(compass)
        self.ax.set_rorigin(-10)

        self.refresh_stats(dist_list)

    @pyqtSlot(list)
    def refresh_stats(self, distance: list):
        self.ax.clear()

        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_xlabel('Visibility', fontsize=10)

        # self.ax.set_rgrids(np.arange(0, 20, 5))
        self.ax.set_rgrids([0, 5, 10, 15, 20])
        self.ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        self.ax.set_rorigin(-10)

        # index = []
        min_value = min(distance)

        for i in range(len(distance)):
            if distance[i] == min_value:
                # index.append(i)
            # if i in index:
                plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(distance[i]), width=0.25 * np.pi, color=['red'])
            else:
                plt.bar(0.25 * np.pi * (1 + 2 * i) / 2, int(distance[i]), width=0.25 * np.pi, color=['green'])

        self.canvas.draw()

    def mouseDoubleClickEvent(self, event):
        print('hi22')


class ThumbnailView(QMainWindow):

    def __init__(self, image_file_name: str, date: int):
        super().__init__()

        print(f'{JS06Settings.get("image_save_path")}/vista/PNM_9030V/{date}/{image_file_name}_PNM_9030V.png')

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'resources/thumbnail_view.ui')
        uic.loadUi(ui_path, self)

        self.front_image.setPixmap(
            QPixmap(
                f'{JS06Settings.get("image_save_path")}/vista/PNM_9030V/{date}/{image_file_name}_PNM_9030V.png').scaled(
                self.front_image.width(),
                self.front_image.height()))
        self.rear_image.setPixmap(
            QPixmap(
                f'{JS06Settings.get("image_save_path")}/vista/PNM_9030V/{date}/{image_file_name}_PNM_9030V.png').scaled(
                self.rear_image.width(),
                self.rear_image.height()))


class ND01MainWindow(QMainWindow):

    def __init__(self, q, _q):
        super().__init__()

        # login_window = LoginWindow()
        # login_window.exec_()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'resources/main_window.ui')
        uic.loadUi(ui_path, self)
        self.showFullScreen()

        # self._ctrl = JS08MainCtrl

        self._plot = VisibilityView(self, 1440)
        # self._polar = DiscernmentView(self)
        self._polar = PolarPlot(self)

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

        # self.blank_label_front.paintEvent = self.blank_label_paintEvent

        self.front_video_widget = VideoWidget(self)
        self.front_video_widget.on_camera_change('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')

        self.rear_video_widget = VideoWidget(self)
        self.rear_video_widget.on_camera_change('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')

        self.video_horizontalLayout.addWidget(self.front_video_widget)
        self.video_horizontalLayout.addWidget(self.rear_video_widget)
        # self.video_horizontalLayout.addWidget(self.blank_label_front)
        # self.video_horizontalLayout.addWidget(self.blank_label_rear)
        # self.video_horizontalLayout.setSpacing(1)

        self.graph_horizontalLayout.addWidget(self._plot)
        # self._polar를 addWidget 하면
        self.graph_horizontalLayout.addWidget(self._polar.canvas)

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
        self.p_vis_label.mousePressEvent = self.unit_convert

        self.label_1hour.mouseDoubleClickEvent = self.thumbnail_click1
        self.label_2hour.mouseDoubleClickEvent = self.thumbnail_click2
        self.label_3hour.mouseDoubleClickEvent = self.thumbnail_click3
        self.label_4hour.mouseDoubleClickEvent = self.thumbnail_click4
        self.label_5hour.mouseDoubleClickEvent = self.thumbnail_click5
        self.label_6hour.mouseDoubleClickEvent = self.thumbnail_click6

        self.setting_button.clicked.connect(self.setting_btn_click)

        self.show()

    def front_camera_pause(self, event):
        self.front_video_widget.media_player.pause()

    def rear_camera_pause(self, event):
        self.rear_video_widget.media_player.pause()

    def alert_test(self):
        self.alert.setIcon(QIcon('resources/asset/red.png'))
        print(len(self.data_date))
        a = [5, 10, 15, 20, 15, 10, 5, 10]
        random.shuffle(a)
        self._polar.refresh_stats(a)

    def reset_StyleSheet(self):
        self.label_1hour.setStyleSheet('')
        self.label_2hour.setStyleSheet('')
        self.label_3hour.setStyleSheet('')
        self.label_4hour.setStyleSheet('')
        self.label_5hour.setStyleSheet('')
        self.label_6hour.setStyleSheet('')

    def thumbnail_view(self, file_name: str):
        self.view = ThumbnailView(file_name, int(file_name[2:8]))
        self.view.setGeometry(QRect(self.video_horizontalLayout.geometry().x(),
                                    self.video_horizontalLayout.geometry().y() + 21,
                                    self.video_horizontalLayout.geometry().width(),
                                    self.video_horizontalLayout.geometry().height()))
        self.view.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.view.setWindowModality(Qt.ApplicationModal)
        self.view.raise_()

    def thumbnail_click1(self, e):

        name = self.label_1hour_time.text()[:2] + self.label_1hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_1hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_1hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click2(self, e):
        name = self.label_2hour_time.text()[:2] + self.label_2hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_2hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_2hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click3(self, e):
        name = self.label_3hour_time.text()[:2] + self.label_3hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_3hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_3hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click4(self, e):
        name = self.label_4hour_time.text()[:2] + self.label_4hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_4hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_4hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click5(self, e):
        name = self.label_5hour_time.text()[:2] + self.label_5hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_5hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_5hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click6(self, e):
        name = self.label_6hour_time.text()[:2] + self.label_6hour_time.text()[3:]
        epoch = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.thumbnail_view(epoch + name + '00')

        self.reset_StyleSheet()
        self.label_6hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_6hour_time.text()} image')

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

        dlg = ND01SettingWidget()
        dlg.show()
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

        self.front_video_widget.media_player.play()
        self.rear_video_widget.media_player.play()
        self.consumer.resume()
        self.consumer.start()

    def btn_on(self, event):
        self.setting_button.setIcon(QIcon('resources/asset/settings_on.png'))

    def btn_off(self, event):
        self.setting_button.setIcon(QIcon('resources/asset/settings.png'))

    def unit_convert(self, event):
        if self.km_mile_convert:
            self.km_mile_convert = False
        elif self.km_mile_convert is False:
            self.km_mile_convert = True

    def get_data(self, year, month_day):
        save_path = os.path.join(f'{JS06Settings.get("data_csv_path")}/PNM_9030V/{year}')

        if os.path.isfile(f'{save_path}/{month_day}.csv'):
            result = pd.read_csv(f'{save_path}/{month_day}.csv')
            data_datetime = result['date'].tolist()
            data_epoch = result['epoch'].tolist()
            data_visibility = result['visibility'].tolist()

            return data_datetime, data_epoch, data_visibility

        else:
            return [], [], []

    @pyqtSlot(str)
    def print_data(self, visibility):
        # self.data_date, self.data_time, self.data_vis = [], [], []
        # self.epoch, self.q_list = [], []

        visibility_float = round(float(visibility), 3)
        epoch = QDateTime.currentSecsSinceEpoch()
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
        year = current_time[:4]
        md = current_time[5:7] + current_time[8:10]

        get_date, get_epoch, self.q_list = self.get_data(year, md)
        for i in range(len(get_date)):
            get_epoch[i] = get_epoch[i] * 1000
            # print(f'{get_date[i]} - {get_epoch[i]} - {self.q_list[i]}')
            self._plot.refresh_stats(get_epoch[i], self.q_list[i])

        if len(self.q_list) == 0 or self.q_list_scale != len(self.q_list):
            self.q_list = []
            for i in range(self.q_list_scale):
                self.q_list.append(visibility_float)
            result_vis = np.mean(self.q_list)
        else:
            self.q_list.pop(0)
            self.q_list.append(visibility_float)
            result_vis = np.mean(self.q_list)

        if len(self.data_date) >= self.q_list_scale or len(self.data_vis) >= self.q_list_scale:
            print('data scale over!')
            self.data_date.pop(0)
            self.data_time.pop(0)
            self.data_vis.pop(0)

        self.data_date.append(current_time)
        self.data_time.append(epoch)
        self.data_vis.append(visibility_float)

        save_path = os.path.join(f'{JS06Settings.get("data_csv_path")}/PNM_9030V/{year}')
        file = f'{save_path}/{md}.csv'

        if os.path.isfile(f'{file}') is False:
            os.makedirs(f'{save_path}', exist_ok=True)
            result = pd.DataFrame(columns=['date', 'epoch', 'visibility'])
            result.to_csv(f'{file}', mode='w', index=False)

        result = pd.DataFrame(columns=['date', 'epoch', 'visibility'])
        result['date'] = [self.data_date[-1]]
        result['epoch'] = [self.data_time[-1]]
        result['visibility'] = [self.data_vis[-1]]
        result.to_csv(f'{file}', mode='a', index=False, header=False)

        self.visibility = round(float(result_vis), 3)

        # self._plot.refresh_stats(epoch, self.q_list)

    @pyqtSlot(str)
    def clock(self, data):
        self.blank_label_front.setGeometry(self.front_video_widget.geometry())
        self.blank_label_rear.setGeometry(self.rear_video_widget.geometry())

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data)))
        self.year_date = current_time[2:4] + current_time[5:7] + current_time[8:10]
        self.real_time_label.setText(current_time)
        self.p_vis_label.setText(f'{self.pm_text} ㎍/㎥')

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

        if int(self.visibility * 1000) <= JS06Settings.get('visibility_alert_limit'):
            self.alert.setIcon(QIcon('resources/asset/red.png'))
        else:
            self.alert.setIcon(QIcon('resources/asset/green.png'))

    def thumbnail_refresh(self):
        # one_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600))
        # two_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 2))
        # three_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 3))
        # four_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 4))
        # five_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 5))
        # six_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 3600 * 6))

        one_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60))
        two_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 2))
        three_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 3))
        four_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 4))
        five_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 5))
        six_min_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time() - 60 * 6))

        # self.label_1hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600)))
        # self.label_2hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 2)))
        # self.label_3hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 3)))
        # self.label_4hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 4)))
        # self.label_5hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 5)))
        # self.label_6hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 3600 * 6)))

        self.label_1hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60)))
        self.label_2hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 2)))
        self.label_3hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 3)))
        self.label_4hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 4)))
        self.label_5hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 5)))
        self.label_6hour_time.setText(time.strftime('%H:%M', time.localtime(time.time() - 60 * 6)))

        self.label_1hour.setPixmap(
            QPixmap(f'{JS06Settings.get("image_save_path")}/resize/PNM_9030V/{self.year_date}/{one_min_ago}.jpg'))
        self.label_2hour.setPixmap(
            QPixmap(f'{JS06Settings.get("image_save_path")}/resize/PNM_9030V/{self.year_date}/{two_min_ago}.jpg'))
        self.label_3hour.setPixmap(
            QPixmap(f'{JS06Settings.get("image_save_path")}/resize/PNM_9030V/{self.year_date}/{three_min_ago}.jpg'))
        self.label_4hour.setPixmap(
            QPixmap(f'{JS06Settings.get("image_save_path")}/resize/PNM_9030V/{self.year_date}/{four_min_ago}.jpg'))
        self.label_5hour.setPixmap(
            QPixmap(f'{JS06Settings.get("image_save_path")}/resize/PNM_9030V/{self.year_date}/{five_min_ago}.jpg'))
        self.label_6hour.setPixmap(
            QPixmap(f'{JS06Settings.get("image_save_path")}/resize/PNM_9030V/{self.year_date}/{six_min_ago}.jpg'))

    def keyPressEvent(self, e):
        """Override function QMainwindow KeyPressEvent that works when key is pressed"""
        if e.key() == Qt.Key_F:
            self.showFullScreen()
        if e.key() == Qt.Key_D:
            self.showNormal()

    def blank_label_paintEvent(self, event: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.white, 1, Qt.DotLine)

        qp.setPen(pen)
        qp.drawLine(240, 0, 240, 411)
        qp.drawLine(480, 0, 480, 411)
        qp.drawLine(720, 0, 720, 411)


class VideoWidget(QWidget):
    """Video stream player using QVideoWidget"""
    video_frame = None

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.begin = QPoint()
        self.end = QPoint()
        self.flag = False

        args = [
            '--rtsp-frame-buffer-size',
            '1000000'
        ]

        self.instance = vlc.Instance(args)
        self.instance.log_unset()
        self.media_player = self.instance.media_player_new()

        self.video_frame = QFrame()
        self.blank_label = QLabel()
        self.blank_label.setStyleSheet('background-color: #83BCD4')

        if sys.platform == 'win32':
            self.media_player.set_hwnd(self.video_frame.winId())

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_frame)

    def mouseDoubleClickEvent(self, event):
        if self.flag is not True:
            self.flag = True
            self.end.setX(event.pos().x() - 120)
        else:
            self.flag = False

    def mousePressEvent(self, event):

        if event.buttons() == Qt.LeftButton:
            self.begin = event.pos()
            self.end.setX(event.pos().x() - 120)

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.LeftButton:
            self.end = event.pos()
            self.end.setX(event.pos().x() - 120)
            self.update()

    def mouseReleaseEvent(self, event):

        self.end = event.pos()
        self.end.setX(event.pos().x() - 120)
        self.update()

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        pen = QPen(Qt.white, 1, Qt.DotLine)

        qp.setPen(pen)
        qp.setFont(QFont('Arial', 6))

        if self.flag:
            if self.end.x() >= 600:
                self.end.setX(600)

            elif self.end.x() <= 360:
                self.end.setX(360)

            qp.drawLine(self.end.x() - int(self.width() / 4) * 2, 0,
                        self.end.x() - int(self.width() / 4) * 2, self.height())
            qp.drawLine(self.end.x() - int(self.width() / 4), 0,
                        self.end.x() - int(self.width() / 4), self.height())
            qp.drawLine(self.end.x(), 0, self.end.x(), self.height())
            qp.drawLine(self.end.x() + int(self.width() / 4), 0,
                        self.end.x() + int(self.width() / 4), self.height())
            qp.drawLine(self.end.x() + int(self.width() / 4) * 2, 0,
                        self.end.x() + int(self.width() / 4) * 2, self.height())

            if self.geometry().x() == 0:
                qp.drawText(self.end.x() - int(self.width() / 4 + 60), 7, 'W')
                qp.drawText(self.end.x() - int(self.width() / 4) + 120, 7, 'NW')
                qp.drawText(self.end.x() + 120, 7, 'N')
                qp.drawText(self.end.x() + int(self.width() / 4) + 120, 7, 'NE')
                qp.drawText(self.end.x() + int(self.width() / 4 * 2) + 60, 7, 'E')

                qp.drawText(self.end.x() - int(self.width() / 4 + 60), self.height() - 2, 'W')
                qp.drawText(self.end.x() - int(self.width() / 4) + 120, self.height() - 2, 'NW')
                qp.drawText(self.end.x() + 120, self.height() - 2, 'N')
                qp.drawText(self.end.x() + int(self.width() / 4) + 120, self.height() - 2, 'NE')
                qp.drawText(self.end.x() + int(self.width() / 4 * 2) + 60, self.height() - 2, 'E')

            elif self.geometry().x() == 960:
                qp.drawText(self.end.x() - int(self.width() / 4 + 60), 7, 'E')
                qp.drawText(self.end.x() - int(self.width() / 4) + 120, 7, 'SE')
                qp.drawText(self.end.x() + 120, 7, 'S')
                qp.drawText(self.end.x() + int(self.width() / 4) + 120, 7, 'SW')
                qp.drawText(self.end.x() + int(self.width() / 4 * 2) + 60, 7, 'W')

                qp.drawText(self.end.x() - int(self.width() / 4 + 60), self.height() - 2, 'E')
                qp.drawText(self.end.x() - int(self.width() / 4) + 120, self.height() - 2, 'SE')
                qp.drawText(self.end.x() + 120, self.height() - 2, 'S')
                qp.drawText(self.end.x() + int(self.width() / 4) + 120, self.height() - 2, 'SW')
                qp.drawText(self.end.x() + int(self.width() / 4 * 2) + 60, self.height() - 2, 'W')

            # pen = QPen(Qt.white, 1, Qt.SolidLine)
            # qp.setPen(pen)
            # qp.drawLine(0, 0, self.width(), 0)
            # qp.drawLine(0, 0, 0, self.height())
            # qp.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

    @pyqtSlot(str)
    def on_camera_change(self, uri: str):
        if uri[:4] == 'rtsp':
            self.media_player.set_media(self.instance.media_new(uri))
            self.media_player.play()
        else:
            pass


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
    from PyQt5.QtWidgets import QApplication

    mp.freeze_support()
    q = Queue()
    _q = Queue()

    _producer = producer

    p = Process(name='clock', target=clock, args=(q,), daemon=True)
    _p = Process(name='producer', target=_producer, args=(_q,), daemon=True)

    p.start()
    _p.start()

    os.makedirs(f'{JS06Settings.get("data_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS06Settings.get("target_csv_path")}', exist_ok=True)
    os.makedirs(f'{JS06Settings.get("image_save_path")}', exist_ok=True)

    app = QApplication(sys.argv)
    window = ND01MainWindow(q, _q)
    sys.exit(app.exec())
