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
import numpy as np
import pyqtgraph as pg
import multiprocessing as mp
from multiprocessing import Process, Queue

from PyQt5.QtGui import (QPixmap, QIcon, QPainter,
                         QColor, QPaintEvent, QPen)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QFrame,
                             QVBoxLayout, QLabel)
from PyQt5.QtCore import (Qt, pyqtSlot, pyqtSignal,
                          QRect, QTimer, QObject,
                          QThread, QPointF, QDateTime)
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


# class TimeAxisItem(pg.AxisItem):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setLabel(text='Time (sec)', units=None)
#         self.enableAutoSIPrefix(False)
#
#     def tickStrings(self, values, scale, spacing):
#         """
#         override 하여, tick 옆에 써지는 문자를 원하는대로 수정함.
#         values --> x축 값들
#         숫자로 이루어진 Iterable data(하나씩 차례로 반환 가능한 object -> ex) List[int]) list, str, tuple 등등
#         """
#         return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]


class VisibilityView(QChartView):

    def __init__(self, parent: QWidget, maxlen: int):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(600, 400)

        now = QDateTime.currentSecsSinceEpoch()
        zeros = [(t * 1000, -1) for t in range(now - maxlen * 60, now, 60)]
        self.data = collections.deque(zeros, maxlen=maxlen)

        self.setRenderHint(QPainter.Antialiasing)

        chart = QChart()
        chart.legend().setVisible(False)
        # chart.legend().setColor(QColor(255, 255, 255, 255))
        # chart.setTitleBrush(QColor(255, 255, 255, 255))
        # chart.setBackgroundBrush(QColor(0, 0, 0, 255))
        self.setChart(chart)
        self.series = QLineSeries(name='Prevailing Visibility')
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

        data_point = [QPointF(t, v) for t, v in self.data]
        self.series.append(data_point)

    # @pyqtSlot(int, dict)
    def refresh_stats(self, epoch: int, vis_list: list):
        # vis_list = list(vis.values())

        if len(vis_list) == 0:
            vis_list = [0]
        prev_vis = self.prevailing_visibility(vis_list)
        # epoch = QDateTime.currentSecsSinceEpoch()
        self.data.append((epoch * 1000, prev_vis))

        left = QDateTime.fromMSecsSinceEpoch(self.data[0][0])
        right = QDateTime.fromMSecsSinceEpoch(self.data[-1][0])
        self.chart().axisX().setRange(left, right)

        data_point = [QPointF(t, v) for t, v in self.data]
        self.series.replace(data_point)

    def prevailing_visibility(self, vis: list) -> float:
        if None in vis:
            return 0

        sorted_vis = sorted(vis, reverse=True)
        prevailing = sorted_vis[(len(sorted_vis) - 1) // 2]

        return prevailing


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

        positives = []
        negatives = [(0, 4), (0, 9), (0, 14),
                     (45, 5), (45, 10), (45, 15),
                     (90, 5), (90, 10), (90, 15),
                     (135, 5), (135, 10), (135, 15),
                     (180, 5), (180, 10), (180, 15),
                     (225, 5), (225, 10), (225, 15),
                     (270, 5), (270, 10), (270, 15),
                     (315, 5), (315, 10), (315, 15)]
        pos_point = [QPointF(a, d) for a, d in positives]
        self.positives.replace(pos_point)
        neg_point = [QPointF(a, d) for a, d in negatives]
        self.negatives.replace(neg_point)


class ThumbnailView(QMainWindow):

    def __init__(self, image_file_name: str, date: int):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "resources/thumbnail_view.ui")
        uic.loadUi(ui_path, self)

        self.front_image.setPixmap(
            QPixmap(
                f'{JS06Settings.get("image_save_path")}/vista/{date}/{image_file_name}.png').scaled(
                self.front_image.width(),
                self.front_image.height()))
        self.rear_image.setPixmap(
            QPixmap(
                f'{JS06Settings.get("image_save_path")}/vista/{date}/{image_file_name}.png').scaled(
                self.rear_image.width(),
                self.rear_image.height()))


class ND01MainWindow(QMainWindow):

    def __init__(self, q, _q):
        super().__init__()

        # login_window = LoginWindow()
        # login_window.exec_()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "resources/main_window.ui")
        uic.loadUi(ui_path, self)
        self.showFullScreen()

        # self._ctrl = JS08MainCtrl

        self._plot = VisibilityView(self, 1440)
        # self._ctrl.wedge_vis_ready.connect(self._plot.refresh_stats)
        # self._plot.refresh_stats()

        self._polar = DiscernmentView(self)
        # self._ctrl.target_assorted.connect(self._polar.refresh_stats)
        # self._polar.refresh_stats()

        self.view = None
        self.km_mile_convert = False
        self.visibility = 0
        self.pm_text = 0
        self.date = None
        self.q_list = []
        self.q_list_scale = 300

        self.front_video_widget = VideoWidget(self)
        self.front_video_widget.on_camera_change("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")

        self.rear_video_widget = VideoWidget(self)
        self.rear_video_widget.on_camera_change("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")

        self.video_horizontalLayout.addWidget(self.front_video_widget)
        self.video_horizontalLayout.addWidget(self.rear_video_widget)

        self.graph_horizontalLayout.addWidget(self._plot)
        self.graph_horizontalLayout.addWidget(self._polar)

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

    def reset_StyleSheet(self):
        self.label_1hour.setStyleSheet('')
        self.label_2hour.setStyleSheet('')
        self.label_3hour.setStyleSheet('')
        self.label_4hour.setStyleSheet('')
        self.label_5hour.setStyleSheet('')
        self.label_6hour.setStyleSheet('')

    def thumbnail_view(self, file_name: str):
        self.view = ThumbnailView(file_name, self.date)
        self.view.setGeometry(QRect(self.video_horizontalLayout.geometry().x(),
                                    self.video_horizontalLayout.geometry().y() + 21,
                                    self.video_horizontalLayout.geometry().width(),
                                    self.video_horizontalLayout.geometry().height()))
        self.view.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.view.setWindowModality(Qt.ApplicationModal)
        self.view.raise_()

    def thumbnail_click1(self, e):

        name = self.label_1hour_time.text()[:2] + self.label_1hour_time.text()[3:]
        epoch = time.strftime("%Y%m%d", time.localtime(time.time()))
        self.thumbnail_view(epoch + name + "00")

        self.reset_StyleSheet()
        self.label_1hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_1hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click2(self, e):
        name = self.label_2hour_time.text()[:2] + self.label_2hour_time.text()[3:]
        epoch = time.strftime("%Y%m%d", time.localtime(time.time()))
        self.thumbnail_view(epoch + name + "00")

        self.reset_StyleSheet()
        self.label_2hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_2hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click3(self, e):
        name = self.label_3hour_time.text()[:2] + self.label_3hour_time.text()[3:]
        epoch = time.strftime("%Y%m%d", time.localtime(time.time()))
        self.thumbnail_view(epoch + name + "00")

        self.reset_StyleSheet()
        self.label_3hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_3hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click4(self, e):
        name = self.label_4hour_time.text()[:2] + self.label_4hour_time.text()[3:]
        epoch = time.strftime("%Y%m%d", time.localtime(time.time()))
        self.thumbnail_view(epoch + name + "00")

        self.reset_StyleSheet()
        self.label_4hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_4hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click5(self, e):
        name = self.label_5hour_time.text()[:2] + self.label_5hour_time.text()[3:]
        epoch = time.strftime("%Y%m%d", time.localtime(time.time()))
        self.thumbnail_view(epoch + name + "00")

        self.reset_StyleSheet()
        self.label_5hour.setStyleSheet(self.click_style)
        self.monitoring_label.setText(f' {self.label_5hour_time.text()} image')

        QTimer.singleShot(5000, self.thumbnail_show)

    def thumbnail_click6(self, e):
        name = self.label_6hour_time.text()[:2] + self.label_6hour_time.text()[3:]
        epoch = time.strftime("%Y%m%d", time.localtime(time.time()))
        self.thumbnail_view(epoch + name + "00")

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

    @pyqtSlot(str)
    def print_data(self, visibility):
        visibility_float = round(float(visibility), 3)

        if len(self.q_list) == 0 or self.q_list_scale != len(self.q_list):
            self.q_list = []
            for i in range(self.q_list_scale):
                self.q_list.append(visibility_float)
            result_vis = np.mean(self.q_list)
        else:
            self.q_list.pop(0)
            self.q_list.append(visibility_float)
            result_vis = np.mean(self.q_list)

        self.visibility = round(float(result_vis), 3)
        # print(f'Visibility: {self.visibility} km = {int(self.visibility * 1000)} m')

    @pyqtSlot(str)
    def clock(self, data):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data)))
        self.date = current_time[5:7] + current_time[8:10]
        self.year_date = current_time[2:4] + current_time[5:7] + current_time[8:10]
        self.real_time_label.setText(current_time)

        self._plot.refresh_stats(QDateTime.currentSecsSinceEpoch(), self.q_list)

        # self._plot.update_plot(int(float(data)))

        # result = 0
        # for i in self._plot.plotData['y']:
        #     result += i
        # p_vis_km = f'{format(round(int(result / len(self._plot.plotData["y"])), 2), ",")}'
        # p_vis_nm = f'{format(round(int(result / len(self._plot.plotData["y"])) / 1609, 2), ",")}'

        if self.visibility != 0:
            ext = 3.912 / self.visibility
            hd = 89
            self.pm_text = round((ext * 1000 / 4 / 2.5) / (1 + 5.67 * ((hd / 100) ** 5.8)), 2)

        if self.km_mile_convert:
            self.c_vis_label.setText(f'{format(round(self.visibility / 1609, 2), ",")} mile')

        elif self.km_mile_convert is False:
            self.c_vis_label.setText(f'{format(int(self.visibility * 1000), ",")} m')
            self.p_vis_label.setText(f'{self.pm_text} ㎍/㎥')

        # data_time = self._plot.plotData['x']
        # if int(float(data)) - 3600 * 3 in self._plot.plotData['x']:
        #     index = data_time.index(int(float(data)) - 3600 * 3)
        #     self._plot.plotData['x'].pop(index)
        #     self._plot.plotData['y'].pop(index)

        self.thumbnail_refresh()
        if current_time[-2:] == "00":
            self.thumbnail_refresh()

        # if int(p_vis_km.replace(',', '')) <= JS06Settings.get('visibility_alert_limit'):
        #     self.alert.setIcon(QIcon('resources/asset/red.png'))

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

    # def paintEvent(self, event: QPaintEvent):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawLines(qp)
    #     qp.end()
    #
    # def drawLines(self, qp):
    #     pen = QPen(Qt.black, 20, Qt.SolidLine)
    #
    #     qp.setPen(pen)
    #     qp.drawLine(240, 0, 240, 1070)
    #     qp.drawLine(480, 0, 480, 411)
    #     qp.drawLine(720, 0, 720, 411)
    #     print('paint')


class VideoWidget(QWidget):
    """Video stream player using QVideoWidget"""
    video_frame = None

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        args = [
            "--rtsp-frame-buffer-size",
            "1000000"
        ]

        self.instance = vlc.Instance(args)
        self.instance.log_unset()
        self.media_player = self.instance.media_player_new()

        self.image_player = self.instance.media_list_player_new()
        self.image_media = self.instance.media_list_new('')

        self.video_frame = QFrame()
        self.blank_label = QLabel()

        if sys.platform == 'win32':
            self.media_player.set_hwnd(self.video_frame.winId())

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_frame)

    # def paintEvent(self, event: QPaintEvent):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawLines(qp)
    #     qp.end()
    #
    # def drawLines(self, qp):
    #     pen = QPen(Qt.white, 1, Qt.DotLine)
    #
    #     qp.setPen(pen)
    #     qp.drawLine(240, 0, 240, 411)
    #     qp.drawLine(480, 0, 480, 411)
    #     qp.drawLine(720, 0, 720, 411)

    @pyqtSlot(str)
    def on_camera_change(self, uri: str):
        # uri = "rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp"
        if uri[:4] == "rtsp":
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
