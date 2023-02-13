#!/usr/bin/env python3
#
# Copyright 2021-2023 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import os
import cv2
import time
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')
from scipy.optimize import curve_fit

from PySide6.QtCore import (QPoint, QRect, Qt)
from PySide6.QtGui import (QPixmap, QPainter, QBrush,
                           QColor, QPen, QImage, QFont, QMovie)
from PySide6.QtWidgets import (QInputDialog, QDialog, QFileDialog,
                               QHeaderView, QTableWidget, QTableWidgetItem)
from PySide6.QtCharts import QChart, QChartView, QValueAxis, QLineSeries

from target_info_test import TargetInfo
from resources.visibility_test import Ui_Dialog


class JS08AdminSettingWidget(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.showFullScreen()
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.begin = QPoint()
        self.end = QPoint()

        self.upper_left = ()
        self.lower_right = ()

        self.target_name = []
        self.left_range = []
        self.right_range = []
        self.distance = []
        self.azimuth = []
        self.current_azi = ''

        self.isDrawing = False

        self.video_width = 0
        self.video_height = 0

        self.cp_image = None
        self.img = None
        self.end_drawing = True

        self.chart_view = None
        self.select_target = None
        self.select_name = None
        self.select_corner1 = None
        self.select_corner2 = None

        self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)

        self.r_list = []
        self.g_list = []
        self.b_list = []
        self.target_info = TargetInfo()

        self.current_camera = 'PNO-A9081R01'
        self.cam_flag = False
        self.movie = None

        self.image_load()

        if len(self.left_range) > 0:
            self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
            self.show_target_table()

        self.image_label.paintEvent = self.lbl_paintEvent
        self.image_label.mousePressEvent = self.lbl_mousePressEvent
        self.image_label.mouseMoveEvent = self.lbl_mouseMoveEvent
        self.image_label.mouseReleaseEvent = self.lbl_mouseReleaseEvent

        self.load_img.clicked.connect(self.load_img_btn)
        self.vis_btn.clicked.connect(self.print_data)

        self.buttonBox.accepted.connect(self.accept_click)
        self.buttonBox.rejected.connect(self.reject_click)

    def show_target_table(self):
        # min_x = []
        # min_y = []
        self.r_list = []
        self.g_list = []
        self.b_list = []

        copy_image = self.cp_image.copy()
        row_count = len(self.distance)
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(['Number', 'Distance', 'Azimuth'])

        for upper_left, lower_right in zip(self.left_range, self.right_range):
            result = self.target_info.minrgb(upper_left, lower_right, copy_image)
            # min_x.append(result[0])
            # min_y.append(result[1])

            self.r_list.append(copy_image[result[1], result[0], 0])
            self.g_list.append(copy_image[result[1], result[0], 1])
            self.b_list.append(copy_image[result[1], result[0], 2])

        for i in range(0, row_count):
            item2 = QTableWidgetItem(f'{i + 1}')
            item2.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            item2.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget.setItem(i, 0, item2)

            item3 = QTableWidgetItem(f'{self.distance[i]} km')
            item3.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            item3.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget.setItem(i, 1, item3)

            item4 = QTableWidgetItem(f'{self.azimuth[i]}')
            item4.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            item4.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget.setItem(i, 2, item4)

    def func(self, x, c1, c2, a):
        return c2 + (c1 - c2) * np.exp(-a * x)

    def chart_update(self):

        if self.gridLayout_3.count() == 0:
            new_chart_view_NE = self.chart_draw('NE')
            new_chart_view_EN = self.chart_draw('EN')
            new_chart_view_ES = self.chart_draw('ES')
            new_chart_view_SE = self.chart_draw('SE')
            self.gridLayout_3.addWidget(new_chart_view_NE, 0, 0)
            self.gridLayout_3.addWidget(new_chart_view_EN, 0, 1)
            self.gridLayout_3.addWidget(new_chart_view_ES, 1, 0)
            self.gridLayout_3.addWidget(new_chart_view_SE, 1, 1)
        else:
            new_chart_view_NE = self.chart_draw('NE')
            new_chart_view_EN = self.chart_draw('EN')
            new_chart_view_ES = self.chart_draw('ES')
            new_chart_view_SE = self.chart_draw('SE')

            self.gridLayout_3.removeWidget(self.chart_view)
            self.gridLayout_3.addWidget(new_chart_view_NE, 0, 0)
            self.gridLayout_3.addWidget(new_chart_view_EN, 0, 1)
            self.gridLayout_3.addWidget(new_chart_view_ES, 1, 0)
            self.gridLayout_3.addWidget(new_chart_view_SE, 1, 1)
            self.gridLayout_3.update()

    def chart_draw(self, azimuth: str):
        """세팅창 그래프 칸에 소산계수 차트를 그리는 함수"""

        indices = []
        for i in range(len(self.azimuth)):
            if self.azimuth[i] == azimuth:
                indices.append(i)
        # print(azimuth, indices)
        # print(self.distance)
        distance = []
        for i in indices:
            distance.append(self.distance[i])
        # print(distance)

        distance.sort()
        # self.x = np.linspace(self.distance[0], self.distance[-1], 100, endpoint=True)
        self.x = np.linspace(distance[0], distance[-1], 100, endpoint=True)
        self.x.sort()

        print(distance)
        print(self.distance)
        print()

        # hanhwa_opt_r, hanhwa_cov_r = curve_fit(self.func, self.distance, self.r_list, maxfev=5000)
        # hanhwa_opt_g, hanhwa_cov_g = curve_fit(self.func, self.distance, self.g_list, maxfev=5000)
        # hanhwa_opt_b, hanhwa_cov_b = curve_fit(self.func, self.distance, self.b_list, maxfev=5000)
        hanhwa_opt_r, hanhwa_cov_r = curve_fit(self.func, distance, self.r_list, maxfev=5000)
        hanhwa_opt_g, hanhwa_cov_g = curve_fit(self.func, distance, self.g_list, maxfev=5000)
        hanhwa_opt_b, hanhwa_cov_b = curve_fit(self.func, distance, self.b_list, maxfev=5000)

        chart = QChart()
        chart.setTheme(QChart.ChartThemeDark)
        font = QFont('Noto Sans kr')
        font.setPixelSize(20)
        font.setBold(3)
        chart.setTitleFont(font)
        chart.setTitleBrush(QBrush(QColor('#ffffff')))
        chart.setTitle(f'{azimuth} 소산계수 그래프')
        # chart.setFont(QFont(''))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

        axis_x = QValueAxis()
        axis_x.setTickCount(7)
        axis_x.setLabelFormat('%i')
        axis_x.setTitleText('Distance(km)')
        axis_x.setTitleBrush(QBrush(QColor('#ffffff')))
        axis_x.setRange(0, 6)
        chart.addAxis(axis_x, Qt.AlignBottom)

        axis_y = QValueAxis()
        axis_y.setTickCount(7)
        axis_y.setLabelFormat('%i')
        axis_y.setTitleText('Intensity')
        axis_y.setTitleBrush(QBrush('#ffffff'))
        axis_y.setRange(0, 255)
        chart.addAxis(axis_y, Qt.AlignLeft)

        # # Red Graph
        # # if self.red_checkBox.isChecked():
        series1 = QLineSeries()
        series1.setName('Red')
        pen = QPen()
        pen.setWidth(2)
        series1.setPen(pen)
        series1.setColor(QColor('Red'))

        for dis in self.x:
            series1.append(*(dis, self.func(dis, *hanhwa_opt_r)))
        chart.addSeries(series1)  # data feeding
        series1.attachAxis(axis_x)
        series1.attachAxis(axis_y)
        #
        # # Green Graph
        # # if self.green_checkBox.isChecked():
        series2 = QLineSeries()
        series2.setName('Green')
        pen = QPen()
        pen.setWidth(2)
        series2.setPen(pen)
        series2.setColor(QColor('Green'))

        for dis in self.x:
            series2.append(*(dis, self.func(dis, *hanhwa_opt_g)))
        chart.addSeries(series2)  # data feeding

        series2.attachAxis(axis_x)
        series2.attachAxis(axis_y)
        #
        # # Blue Graph
        # # if self.blue_checkBox.isChecked():
        series3 = QLineSeries()
        series3.setName('Blue')
        pen = QPen()
        pen.setWidth(2)
        series3.setPen(pen)
        series3.setColor(QColor('Blue'))

        for dis in self.x:
            series3.append(*(dis, self.func(dis, *hanhwa_opt_b)))
        chart.addSeries(series3)  # data feeding

        series3.attachAxis(axis_x)
        series3.attachAxis(axis_y)

        chart.legend().setAlignment(Qt.AlignRight)

        # displaying chart
        chart.setBackgroundBrush(QBrush(QColor(22, 32, 42)))
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        # chart_view.setMaximumSize(500, 500)

        return chart_view

    def image_load(self):
        self.left_range = None
        self.right_range = None

        src = 'rtsp://admin:sijung5520@192.168.100.210/profile2/media.smp'
        self.get_target(self.current_camera)

        cap = cv2.VideoCapture(src)
        ret, cv_img = cap.read()
        self.img = cv2.imread('image.png', cv2.IMREAD_COLOR)
        # cp_image = cv_img.copy()
        cap.release()

        # self.image_label.setPixmap(self.convert_cv_qt(cp_image))
        self.image_label.setPixmap(self.convert_cv_qt(self.img))
        self.show_target_table()
        # self.chart_update()
        self.update()

    def convert_cv_qt(self, cv_img):
        """Convert CV image to QImage."""
        cv_img = cv_img.copy()
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        self.cp_image = cv_img.copy()

        self.video_height, self.video_width, ch = cv_img.shape

        bytes_per_line = ch * self.video_width
        convert_to_Qt_format = QImage(cv_img.data, self.video_width, self.video_height,
                                      bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(),
                                        self.image_label.height(),
                                        Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        return QPixmap.fromImage(p)

    def str_to_tuple(self, before_list):
        """저장된 타겟들의 위치정보인 튜플 리스트가 문자열로 바뀌어 다시 튜플형태로 변환하는 함수"""
        tuple_list = [i.split(',') for i in before_list]
        tuple_list = [(int(i[0][1:]), int(i[1][:-1])) for i in tuple_list]
        return tuple_list

    # 타겟 조정 및 썸네일 관련 함수 시작
    def thumbnail_pos(self, end_pos):
        x = int((end_pos.x() / self.image_label.width()) * self.video_width)
        y = int((end_pos.y() / self.image_label.height()) * self.video_height)
        return x, y

    def thumbnail(self, image):
        height, width, channel = image.shape
        bytesPerLine = channel * width
        qImg = QImage(image.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg

    def save_target(self, camera: str):

        file = f'{camera}.csv'
        if self.left_range and os.path.isfile(file):
            col = ['target_name', 'left_range', 'right_range', 'distance', 'azimuth']
            result = pd.DataFrame(columns=col)
            result['target_name'] = self.target_name
            result['left_range'] = self.left_range
            result['right_range'] = self.right_range
            result['distance'] = self.distance
            result['azimuth'] = self.azimuth
            result.to_csv(file, mode='w', index=False)
            print(f'[JS-08 Setting SAVED]')

    def get_target(self, camera: str):

        file = f'{camera}.csv'

        # if os.path.isfile(f'{camera}.csv') is False:
        #     result = pd.DataFrame(columns=['target_name', 'left_range', 'right_range', 'distance', 'azimuth'])
        #     result['target_name'] = [1, 2, 3, 4]
        #     result['left_range'] = [(95, 711), (367, 716), (293, 300), (250, 124)]
        #     result['right_range'] = [(31, 831), (279, 836), (236, 350), (148, 211)]
        #     result['distance'] = [0.1, 1.0, 2.0, 3.0]
        #     result['azimuth'] = ['NE', 'NE', 'NE', 'NE']
        #     result.to_csv(file, mode='w', index=False)

        target_df = pd.read_csv(f'{camera}.csv')
        self.target_name = target_df['target_name'].tolist()
        self.left_range = self.str_to_tuple(target_df['left_range'].tolist())
        self.right_range = self.str_to_tuple(target_df['right_range'].tolist())
        self.distance = target_df['distance'].tolist()
        self.azimuth = target_df['azimuth'].tolist()

    def get_target_info(self, camera_name: str):
        """Retrieves target information of a specific camera."""

        file = f'{camera_name}.csv'
        if os.path.isfile(file):
            target_df = pd.read_csv(file)
            target_name = target_df['target_name'].tolist()
            left_range = self.str_to_tuple(target_df['left_range'].tolist())
            right_range = self.str_to_tuple(target_df['right_range'].tolist())
            distance = target_df['distance'].tolist()
            azimuth = target_df['azimuth'].tolist()
            return target_name, left_range, right_range, distance, azimuth

        else:
            return [], [], [], [], []

    def get_target_from_azimuth(self, camera_name: str, azimuth: str):
        """Retrieves target information from azimuth of a specific camera"""

        file = f'{camera_name}.csv'
        if os.path.isfile(file):
            target_df = pd.read_csv(file)
            azi_target = target_df.loc[(target_df['azimuth'] == f'{azimuth}'), :]

            target_name = azi_target['target_name'].tolist()
            left_range = self.str_to_tuple(azi_target['left_range'].tolist())
            right_range = self.str_to_tuple(azi_target['right_range'].tolist())
            distance = azi_target['distance'].tolist()
            return target_name, left_range, right_range, distance, azimuth

        else:
            return [], [], [], [], []

    def print_data(self):
        epoch = time.strftime('%Y-%m-%d %H:%M:00', time.localtime())
        # self.movie = QMovie('loading.gif', )

        # Visibility measurement start
        front_target_name, front_left_range, front_right_range, front_distance, front_azimuth = \
            self.get_target_info(self.current_camera)

        front_target_name_NE, front_left_range_NE, front_right_range_NE, front_distance_NE, front_azimuth_NE = \
            self.get_target_from_azimuth(self.current_camera, 'NE')
        front_target_name_EN, front_left_range_EN, front_right_range_EN, front_distance_EN, front_azimuth_EN = \
            self.get_target_from_azimuth(self.current_camera, 'EN')
        front_target_name_ES, front_left_range_ES, front_right_range_ES, front_distance_ES, front_azimuth_ES = \
            self.get_target_from_azimuth(self.current_camera, 'ES')
        front_target_name_SE, front_left_range_SE, front_right_range_SE, front_distance_SE, front_azimuth_SE = \
            self.get_target_from_azimuth(self.current_camera, 'SE')

        visibility_front = self.target_info.minprint(epoch[:-2], front_left_range, front_right_range,
                                                     front_distance, self.img, self.current_camera)
        visibility_NE = self.target_info.minprint(epoch[:-2], front_left_range_NE, front_right_range_NE,
                                                  front_distance_NE, self.img, self.current_camera)
        visibility_EN = self.target_info.minprint(epoch[:-2], front_left_range_EN, front_right_range_EN,
                                                  front_distance_EN, self.img, self.current_camera)
        visibility_ES = self.target_info.minprint(epoch[:-2], front_left_range_ES, front_right_range_ES,
                                                  front_distance_ES, self.img, self.current_camera)
        visibility_SE = self.target_info.minprint(epoch[:-2], front_left_range_SE, front_right_range_SE,
                                                  front_distance_SE, self.img, self.current_camera)

        self.first_vis.setText(f'{round(float(visibility_NE), 2)} km')
        self.second_vis.setText(f'{round(float(visibility_EN), 2)} km')
        self.third_vis.setText(f'{round(float(visibility_ES), 2)} km')
        self.fourth_vis.setText(f'{round(float(visibility_SE), 2)} km')
        self.vis_result.setText(f'{round(float(visibility_front), 2)} km')

    def accept_click(self):
        self.save_target(self.current_camera)
        self.close()

    def reject_click(self):
        self.close()

    # Event
    def tableWidget_doubleClicked(self, event):
        self.select_target = self.tableWidget.currentIndex().row()
        self.update()

    def load_img_btn(self, event):
        file = QFileDialog.getOpenFileName(self, '')
        if file:
            print(file[0])

    def lbl_paintEvent(self, event):
        painter = QPainter(self.image_label)

        back_ground_image = self.thumbnail(self.cp_image)
        bk_image = QPixmap.fromImage(back_ground_image)
        painter.drawPixmap(QRect(0, 0, self.image_label.width(),
                                 self.image_label.height()), bk_image)

        painter.setPen(QPen(Qt.white, 1, Qt.DotLine))

        painter.drawLine((self.image_label.width() * 0.25), 0,
                         (self.image_label.width() * 0.25), self.image_label.height())
        painter.drawLine((self.image_label.width() * 0.5), 0,
                         (self.image_label.width() * 0.5), self.image_label.height())
        painter.drawLine((self.image_label.width() * 0.75), 0,
                         (self.image_label.width() * 0.75), self.image_label.height())

        if self.cam_flag:
            painter.setPen(QPen(Qt.black, 1, Qt.DotLine))
            painter.drawText(self.image_label.width() * 0.125, 20, 'SW')
            painter.drawText(self.image_label.width() * 0.375, 20, 'WS')
            painter.drawText(self.image_label.width() * 0.625, 20, 'WN')
            painter.drawText(self.image_label.width() * 0.875, 20, 'NW')
            painter.setPen(QPen(Qt.white, 1, Qt.DotLine))
        elif self.cam_flag is False:
            painter.setPen(QPen(Qt.black, 1, Qt.DotLine))
            painter.drawText(self.image_label.width() * 0.125, 20, 'NE')
            painter.drawText(self.image_label.width() * 0.375, 20, 'EN')
            painter.drawText(self.image_label.width() * 0.625, 20, 'ES')
            painter.drawText(self.image_label.width() * 0.875, 20, 'SE')
            painter.setPen(QPen(Qt.white, 1, Qt.DotLine))

        if self.left_range and self.right_range:
            for name, corner1, corner2 in zip(self.target_name, self.left_range, self.right_range):
                br = QBrush(QColor(100, 10, 10, 40))
                painter.setBrush(br)
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                corner1_1 = int(corner1[0] / self.video_width * self.image_label.width())
                corner1_2 = int(corner1[1] / self.video_height * self.image_label.height())
                corner2_1 = int((corner2[0] - corner1[0]) / self.video_width * self.image_label.width())
                corner2_2 = int((corner2[1] - corner1[1]) / self.video_height * self.image_label.height())
                painter.drawRect(QRect(corner1_1, corner1_2, corner2_1, corner2_2))
                painter.drawText(corner1_1 + corner2_1, corner1_2 - 5, f'{name}')

        if self.isDrawing:
            br = QBrush(QColor(100, 10, 10, 40))
            painter.setBrush(br)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(QRect(self.begin, self.end))

            # th_x, th_y = self.thumbnail_pos(self.end)
            # th_qImage = self.thumbnail(self.cp_image[th_y - 50:th_y + 50, th_x - 50:th_x + 50, :])
            # thumbnail_image = QPixmap.fromImage(th_qImage)
            # painter.drawPixmap(QRect(self.end.x(), self.end.y(), 200, 200), thumbnail_image)

        if self.end_drawing:
            painter.eraseRect(QRect(self.begin, self.end))
            self.end_drawing = False
            self.isDrawing = False
            painter.end()

    def lbl_mousePressEvent(self, event):
        """마우스 클릭시 발생하는 이벤트, QLabel method overriding"""

        # 좌 클릭시 실행
        if event.buttons() == Qt.LeftButton:
            # self.begin = event.globalPosition().toPoint()
            # self.end = event.globalPosition().toPoint()
            self.begin = event.pos()
            self.end = event.pos()
            self.upper_left = (int((self.begin.x() / self.image_label.width()) * self.video_width),
                               int((self.begin.y() / self.image_label.height()) * self.video_height))

            self.isDrawing = True

        # 우 클릭시 실행
        elif event.buttons() == Qt.RightButton:
            text, ok = QInputDialog.getText(self, 'Delete target', 'Input target number to delete')
            if ok:
                if text == '':
                    del self.target_name[-1]
                    del self.left_range[-1]
                    del self.right_range[-1]
                    del self.distance[-1]
                    del self.azimuth[-1]

                else:
                    if len(self.target_name) > 0:
                        text = int(text)
                        del self.target_name[text - 1]
                        del self.left_range[text - 1]
                        del self.right_range[text - 1]
                        del self.distance[text - 1]
                        del self.azimuth[text - 1]

                    for i in range(len(self.target_name)):
                        self.target_name[i] = i + 1

            self.show_target_table()

    def lbl_mouseMoveEvent(self, event):
        """마우스가 움직일 때 발생하는 이벤트, QLabel method overriding"""
        if event.buttons() == Qt.LeftButton:
            # self.end = event.globalPosition().toPoint()
            self.end = event.pos()
            self.image_label.update()

    def lbl_mouseReleaseEvent(self, event):
        """마우스 클릭이 떼질 때 발생하는 이벤트, QLabel method overriding"""
        if self.isDrawing:
            if self.cam_flag:
                if 0 < self.upper_left[0] <= self.video_width * 0.25:
                    self.azimuth.append('SW')
                    self.current_azi = 'SW'
                elif self.video_width * 0.25 < self.upper_left[0] <= self.video_width * 0.5:
                    self.azimuth.append('WS')
                    self.current_azi = 'WS'
                elif self.video_width * 0.5 < self.upper_left[0] <= self.video_width * 0.75:
                    self.azimuth.append('WN')
                    self.current_azi = 'WN'
                elif self.video_width * 0.75 < self.upper_left[0] <= self.video_width:
                    self.azimuth.append('NW')
                    self.current_azi = 'NW'

            elif self.cam_flag is False:
                if 0 < self.upper_left[0] <= self.video_width * 0.25:
                    self.azimuth.append('NE')
                    self.current_azi = 'NE'
                elif self.video_width * 0.25 < self.upper_left[0] <= self.video_width * 0.5:
                    self.azimuth.append('EN')
                    self.current_azi = 'EN'
                elif self.video_width * 0.5 < self.upper_left[0] <= self.video_width * 0.75:
                    self.azimuth.append('ES')
                    self.current_azi = 'ES'
                elif self.video_width * 0.75 < self.upper_left[0] <= self.video_width:
                    self.azimuth.append('SE')
                    self.current_azi = 'SE'

            # self.end = event.globalPosition().toPoint()
            self.end = event.pos()
            self.image_label.update()
            self.lower_right = (int((self.end.x() / self.image_label.width()) * self.video_width),
                                int((self.end.y() / self.image_label.height()) * self.video_height))

            # text, ok = QInputDialog.getText(self, '거리 입력', '거리(km)')

            from input_target import InputTarget
            getText = InputTarget(self.current_azi)
            if getText.exec():
                dist, azi = getText.getInputs()

                self.left_range.append(self.upper_left)
                self.right_range.append(self.lower_right)
                self.distance.append(dist)
                self.target_name.append(len(self.left_range))

                self.end_drawing = True

            else:
                del self.azimuth[-1]

            self.isDrawing = False
            self.show_target_table()

            print(self.azimuth)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = JS08AdminSettingWidget()
    ui.show()
    sys.exit(app.exec())
