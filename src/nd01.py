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

import vlc
import numpy as np
import pyqtgraph as pg
import multiprocessing as mp
from multiprocessing import Process, Queue

from PyQt5.QtGui import (QPixmap, QIcon, QPainter, QColor)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGraphicsScene,
                             QFrame, QVBoxLayout)
from PyQt5.QtCore import (Qt, pyqtSlot, pyqtSignal, QRect,
                          QTimer, QObject, QThread)
from PyQt5.QtChart import (QChartView, QLegend, QLineSeries,
                           QPolarChart, QScatterSeries, QValueAxis)
from PyQt5 import uic

from video_thread_mp import producer, VideoThread
from nd01_settings import ND01SettingWidget
from save_db import main


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


class TimeAxisItem(pg.AxisItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time (sec)', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        """
        override 하여, tick 옆에 써지는 문자를 원하는대로 수정함.
        values --> x축 값들
        숫자로 이루어진 Iterable data(하나씩 차례로 반환 가능한 object -> ex) List[int]) list, str, tuple 등등
        """
        return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]


class PlotWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.pw = pg.PlotWidget(
            labels={'left': 'Visibility (km)'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )

        self.pw.showGrid(x=True, y=True)
        self.pdi = self.pw.plot(pen='w')   # PlotDataItem obj 반환.

        self.p1 = self.pw.plotItem

        self.p2 = pg.ViewBox()
        self.p1.showAxis('right')
        self.p1.scene().addItem(self.p2)
        self.p1.getAxis('right').linkToView(self.p2)
        self.p2.setXLink(self.p1)
        self.p1.getAxis('right').setLabel('Axis 2', color='#ffff00')

        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
        # self.p2.addItem(pg.PlotCurveItem([10, 20, 40, 80, 400, 2000], pen='y'))
        # self.pdi.sigClicked.connect(self.onclick)

        self.plotData = {'x': [], 'y': []}
        self.pre_plotData = {'x': [], 'y': []}

    def update_plot(self, new_time_data: int):
        self.plotData['x'].append(new_time_data)
        self.plotData['y'].append(np.random.randint(10000, 15000))

        # 항상 x축 시간을 설정한 범위 ( -3 시간 전 ~ 10 분 후 )만 보여줌.
        # self.pw.setXRange(new_time_data - 3600 * 3, new_time_data + 600, padding=0)
        # self.pw.setYRange(-1, 21, padding=0)

        data = []
        for i in self.plotData['y']:
            i = i / 1000
            data.append(i)
        self.pdi.setData(self.plotData['x'], data)

        # self.pdi.setData([1643873584, 1643873585, 1643873586, 1643873587, 1643873588],
        #                  [12, 11, 10, 14, 13])

    def onclick(self, plot, points):
        for point in points:
            print(point.pos())


class PolarWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.pw = pg.plot(
            labels={'left': 'Visibility (km)'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )

        self.pw.showGrid(x=True, y=True)
        self.pdi = self.pw.plot(pen='w')

        self.pw.addLine(x=0, pen=0.2)
        self.pw.addLine(y=0, pen=0.2)
        for r in range(2, 20, 2):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen(0.2))
            self.pw.addItem(circle)

        theta = np.linspace(0, 2 * np.pi, 8)
        radius = np.random.normal(loc=10, size=8)

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        self.pw.plot(x, y)


class ThumbnailView(QMainWindow):

    def __init__(self, image_file_name: str, date: int):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/thumbnail_view.ui")
        uic.loadUi(ui_path, self)

        self.front_image.setPixmap(QPixmap(f'D:/ND-01/vista/{date}/{image_file_name}.png')
                                   .scaled(self.front_image.width(), self.front_image.height()))
        self.rear_image.setPixmap(QPixmap(f'D:/ND-01/vista/{date}/{image_file_name}.png')
                                  .scaled(self.rear_image.width(), self.rear_image.height()))


class ND01MainWindow(QMainWindow):

    def __init__(self, q):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "resources/main_window.ui")
        uic.loadUi(ui_path, self)
        self.showFullScreen()
        self._plot = PlotWidget()
        self._polar = PolarWidget()
        self.view = None
        self.km_mile_convert = False
        self.date = None

        self.front_video_widget = VideoWidget(self)
        self.front_video_widget.on_camera_change("rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp")

        self.rear_video_widget = VideoWidget(self)
        self.rear_video_widget.on_camera_change("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")

        self.video_horizontalLayout.addWidget(self.front_video_widget)
        self.video_horizontalLayout.addWidget(self.rear_video_widget)

        self.scene = QGraphicsScene()
        self.vis_plot.setScene(self.scene)
        self.plotWidget = self._plot.pw
        self.plotWidget.resize(600, 400)
        self.scene.addWidget(self.plotWidget)

        self.scene_polar = QGraphicsScene()
        self.polar_plot.setScene(self.scene_polar)
        self.polarWidget = self._polar.pw
        self.polarWidget.resize(600, 400)
        self.scene_polar.addWidget(self.polarWidget)

        self.setting_button.enterEvent = self.btn_on
        self.setting_button.leaveEvent = self.btn_off

        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.clock)
        self.consumer.start()

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
        self.view.show()

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
    def clock(self, data):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data)))
        self.date = current_time[2:4] + current_time[5:7]
        self.real_time_label.setText(current_time)
        self._plot.update_plot(int(float(data)))

        result = 0
        for i in self._plot.plotData['y']:
            result += i
        p_vis_km = f'{format(round(int(result / len(self._plot.plotData["y"])), 2), ",")}'
        p_vis_nm = f'{format(round(int(result / len(self._plot.plotData["y"])) / 1609, 2), ",")}'

        if self.km_mile_convert:
            self.c_vis_label.setText(f'{format(round(self._plot.plotData["y"][-1] / 1609, 2), ",")} mile')
            self.p_vis_label.setText(f'{p_vis_nm} mile')

        elif self.km_mile_convert is False:
            self.c_vis_label.setText(f'{format(self._plot.plotData["y"][-1], ",")} m')
            self.p_vis_label.setText(f'{p_vis_km} m')

        data_time = self._plot.plotData['x']
        if int(float(data)) - 3600 * 3 in self._plot.plotData['x']:
            index = data_time.index(int(float(data)) - 3600 * 3)
            self._plot.plotData['x'].pop(index)
            self._plot.plotData['y'].pop(index)

        one_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()-3600))
        two_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()-3600*2))
        three_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()-3600*3))
        four_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()-3600*4))
        five_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()-3600*5))
        six_hour_ago = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()-3600*6))

        self.label_1hour_time.setText(time.strftime('%H:%M', time.localtime(time.time()-3600)))
        self.label_2hour_time.setText(time.strftime('%H:%M', time.localtime(time.time()-3600*2)))
        self.label_3hour_time.setText(time.strftime('%H:%M', time.localtime(time.time()-3600*3)))
        self.label_4hour_time.setText(time.strftime('%H:%M', time.localtime(time.time()-3600*4)))
        self.label_5hour_time.setText(time.strftime('%H:%M', time.localtime(time.time()-3600*5)))
        self.label_6hour_time.setText(time.strftime('%H:%M', time.localtime(time.time()-3600*6)))

        self.label_1hour.setPixmap(QPixmap(f'D:/ND-01/resize/{self.date}/{one_hour_ago}.jpg'))
        self.label_2hour.setPixmap(QPixmap(f'D:/ND-01/resize/{self.date}/{two_hour_ago}.jpg'))
        self.label_3hour.setPixmap(QPixmap(f'D:/ND-01/resize/{self.date}/{three_hour_ago}.jpg'))
        self.label_4hour.setPixmap(QPixmap(f'D:/ND-01/resize/{self.date}/{four_hour_ago}.jpg'))
        self.label_5hour.setPixmap(QPixmap(f'D:/ND-01/resize/{self.date}/{five_hour_ago}.jpg'))
        self.label_6hour.setPixmap(QPixmap(f'D:/ND-01/resize/{self.date}/{six_hour_ago}.jpg'))

    def keyPressEvent(self, e):
        """Override function QMainwindow KeyPressEvent that works when key is pressed"""
        if e.key() == Qt.Key_F:
            self.showFullScreen()
        if e.key() == Qt.Key_D:
            self.showNormal()


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

        if sys.platform == 'win32':
            self.media_player.set_hwnd(self.video_frame.winId())

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_frame)

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

    p = Process(name='clock', target=clock, args=(q, ), daemon=True)
    _p = Process(name="producer", target=_producer, args=(_q, ), daemon=True)

    p.start()
    _p.start()

    os.makedirs('D:/ND-01/vista', exist_ok=True)
    os.makedirs('D:/ND-01/resize', exist_ok=True)

    app = QApplication(sys.argv)
    window = ND01MainWindow(q)
    sys.exit(app.exec_())

    # MainWindow = QMainWindow()
    # ui = ND01MainWindow()
    # ui.show()
    # sys.exit(app.exec_())
