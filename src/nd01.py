#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     popskim@gmail.com (Songyoung Kim)
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import sys
import os
import time

import vlc
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Queue
import multiprocessing as mp

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QGraphicsScene, QFrame, QVBoxLayout,
                             QLabel, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import (Qt, pyqtSlot, pyqtSignal, QRect,
                          QTimer, QUrl, QObject, QThread)
from PyQt5 import uic

from video_thread_mp import producer, VideoThread
from nd01_settings import ND01SettingWidget
import save_db

# from controller import MainCtrl


def clock(q):
    while True:
        now = str(time.time())
        # now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        q.put(now)
        time.sleep(1)


class Consumer(QThread):
    poped = pyqtSignal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time (sec)', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        """
        override 하여, tick 옆에 써지는 문자를 원하는대로 수정함.
        values --> x축 값들   ; 숫자로 이루어진 Itarable data --> ex) List[int]
        """
        # print("--tickStrings valuse ==>", values)
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

        self.plotData = {'x': [], 'y': []}

    def update_plot(self, new_time_data: int):
        self.plotData['y'].append(np.random.randint(10, 15))
        self.plotData['x'].append(new_time_data)

        self.pw.setXRange(new_time_data - 3600 * 3, new_time_data + 600, padding=0)   # 항상 x축 시간을 최근 범위만 보여줌.
        self.pw.setYRange(-1, 21, padding=0)

        self.pdi.setData(self.plotData['x'], self.plotData['y'])
        # past_value = [x for x in self.plotData['x'] if x <= new_time_data - 3600 * 3]


class ThumbnailView(QMainWindow):

    def __init__(self, image_file_name: str):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/thumbnail_view.ui")
        uic.loadUi(ui_path, self)

        self.front_image.setPixmap(QPixmap(f'D:/ND-01/vista/{image_file_name}.png')
                                   .scaled(self.front_image.width(), self.front_image.height()))
        self.rear_image.setPixmap(QPixmap(f'D:/ND-01/vista/{image_file_name}.png')
                                  .scaled(self.rear_image.width(), self.rear_image.height()))


class ND01MainWindow(QMainWindow):

    def __init__(self, q):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/main_window.ui")
        uic.loadUi(ui_path, self)
        self.showFullScreen()
        # self._ctrl = MainCtrl
        self._plot = PlotWidget()
        self.view = None

        self.front_video_widget = VideoWidget(self)
        self.front_video_widget.on_camera_change("rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp")

        self.rear_video_widget = VideoWidget(self)
        self.rear_video_widget.on_camera_change("rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp")

        self.video_horizontalLayout.addWidget(self.front_video_widget)
        self.video_horizontalLayout.addWidget(self.rear_video_widget)

        self.scene = QGraphicsScene()
        self.graphView.setScene(self.scene)
        self.plotWidget = self._plot.pw
        self.plotWidget.resize(1200, 400)
        self.scene.addWidget(self.plotWidget)

        self.timeseries_verticalLayout.addWidget(self.graphView)

        self.setting_button.enterEvent = self.btn_on
        self.setting_button.leaveEvent = self.btn_off

        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.clock)
        self.consumer.start()

        self.click_style = 'border: 1px solid red;'

        # self.label_1hour.setPixmap(QPixmap(f'D:/ND-01/resize/20220114112000.png'))
        # self.label_2hour.setPixmap(QPixmap(f'D:/ND-01/resize/20220114132300.png'))
        # self.label_3hour.setPixmap(QPixmap(f'D:/ND-01/resize/20220114134000.png'))
        # self.label_4hour.setPixmap(QPixmap(f'D:/ND-01/resize/20220117144800.png'))
        # self.label_5hour.setPixmap(QPixmap(f'D:/ND-01/resize/20220117153300.png'))
        # self.label_6hour.setPixmap(QPixmap(f'D:/ND-01/resize/20220117172600.png'))

        self.label_1hour.mouseDoubleClickEvent = self.thumbnail_click1
        self.label_2hour.mouseDoubleClickEvent = self.thumbnail_click2
        self.label_3hour.mouseDoubleClickEvent = self.thumbnail_click3
        self.label_4hour.mouseDoubleClickEvent = self.thumbnail_click4
        self.label_5hour.mouseDoubleClickEvent = self.thumbnail_click5
        self.label_6hour.mouseDoubleClickEvent = self.thumbnail_click6

        self.setting_button.clicked.connect(self.setting_btn_click)

        self.show()

    def reset_StyleSheet(self):
        self.label_1hour.setStyleSheet('')
        self.label_2hour.setStyleSheet('')
        self.label_3hour.setStyleSheet('')
        self.label_4hour.setStyleSheet('')
        self.label_5hour.setStyleSheet('')
        self.label_6hour.setStyleSheet('')

    def thumbnail_view(self, file_name: str):
        self.view = ThumbnailView(file_name)
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

        # self.front_video_widget.media_player.play()
        # self.rear_video_widget.media_player.play()

    @pyqtSlot()
    def setting_btn_click(self):
        self.front_video_widget.media_player.stop()
        self.rear_video_widget.media_player.stop()
        # self.front_video_widget.media_player.pause()
        # self.rear_video_widget.media_player.pause()

        dlg = ND01SettingWidget()
        dlg.show()
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

        self.front_video_widget.media_player.play()
        self.rear_video_widget.media_player.play()

    def btn_on(self, event):
        self.setting_button.setIcon(QIcon('ui/resources/icon/settings_on.png'))

    def btn_off(self, event):
        self.setting_button.setIcon(QIcon('ui/resources/icon/settings.png'))

    @pyqtSlot(str)
    def clock(self, data):
        data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data)))
        self.real_time_label.setText(data_time)
        self._plot.update_plot(int(float(data)))

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

        self.label_1hour.setPixmap(QPixmap(f'D:/ND-01/resize/{one_hour_ago}.png'))
        self.label_2hour.setPixmap(QPixmap(f'D:/ND-01/resize/{two_hour_ago}.png'))
        self.label_3hour.setPixmap(QPixmap(f'D:/ND-01/resize/{three_hour_ago}.png'))
        self.label_4hour.setPixmap(QPixmap(f'D:/ND-01/resize/{four_hour_ago}.png'))
        self.label_5hour.setPixmap(QPixmap(f'D:/ND-01/resize/{five_hour_ago}.png'))
        self.label_6hour.setPixmap(QPixmap(f'D:/ND-01/resize/{six_hour_ago}.png'))

        # self.label_1hour.setPixmap(QPixmap(f'D:/ND-01/vista/20220113071000.png').scaled(315, 131))
        # self.label_2hour.setPixmap(QPixmap(f'D:/ND-01/vista/20220113090400.png').scaled(315, 131))
        # self.label_3hour.setPixmap(QPixmap(f'D:/ND-01/vista/20220113110300.png').scaled(315, 131))
        # self.label_4hour.setPixmap(QPixmap(f'D:/ND-01/vista/20220113130900.png').scaled(315, 131))
        # self.label_5hour.setPixmap(QPixmap(f'D:/ND-01/vista/20220113150500.png').scaled(315, 131))
        # self.label_6hour.setPixmap(QPixmap(f'D:/ND-01/vista/20220113160300.png').scaled(315, 131))

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

        self.instance = vlc.Instance()
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

    def mousePressEvent(self, e):
        print(self.media_player.get_fps())


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
