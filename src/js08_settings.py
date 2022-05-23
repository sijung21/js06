#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
import cv2
import time
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from PyQt5 import uic
from PyQt5.QtCore import (QPoint, QRect, Qt,
                          QTimer)
from PyQt5.QtGui import (QPixmap, QPainter, QBrush,
                         QColor, QPen, QImage,
                         QIcon, QFont)
from PyQt5.QtWidgets import (QApplication, QInputDialog, QDialog,
                             QMessageBox, QFileDialog, QHeaderView,
                             QTableWidget, QTableWidgetItem, QLabel)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis

from model import JS08Settings
import target_info
from auto_file_delete import FileAutoDelete


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


class JS08SettingWidget(QDialog):

    def __init__(self):

        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'resources/setting_window.ui')
        uic.loadUi(resource_path(ui_path), self)
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

        self.isDrawing = False
        self.draw_flag = False

        self.video_width = 0
        self.video_height = 0

        self.cp_image = None
        self.end_drawing = None

        self.chart_view = None
        self.select_target = None
        self.select_target_flag = False
        self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)

        self.r_list = []
        self.g_list = []
        self.b_list = []

        self.current_camera = 'PNM_9030V'
        self.cam_flag = False

        self.image_load()

        self.flag = 0
        # self.get_target(self.current_camera)

        # Add QChart Widget in value_verticalLayout
        if len(self.left_range) > 0:
            self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
            self.show_target_table()

        if len(self.distance) > 4:
            # self.chart_view = self.chart_draw()
            # self.value_verticalLayout.addWidget(self.chart_view)
            # self.chart_update()
            pass

        self.red_checkBox.clicked.connect(self.chart_update)
        self.green_checkBox.clicked.connect(self.chart_update)
        self.blue_checkBox.clicked.connect(self.chart_update)

        self.flip_button.clicked.connect(self.camera_flip)
        self.flip_button.enterEvent = self.btn_on
        self.flip_button.leaveEvent = self.btn_off

        self.data_csv_path_button.clicked.connect(self.data_csv_path)
        self.target_csv_path_button.clicked.connect(self.target_csv_path)
        self.image_save_path_button.clicked.connect(self.image_save_path)
        self.afd_button.clicked.connect(self.afd_btn_click)

        self.data_csv_path_textBrowser.setPlainText(JS08Settings.get('data_csv_path'))
        self.target_csv_path_textBrowser.setPlainText(JS08Settings.get('target_csv_path'))
        self.image_save_path_textBrowser.setPlainText(JS08Settings.get('image_save_path'))

        self.vis_limit_spinBox.setValue(JS08Settings.get('visibility_alert_limit'))
        self.id_lineEdit.setText(JS08Settings.get('login_id'))
        self.pw_lineEdit.setText(JS08Settings.get('login_pw'))

        self.image_size_comboBox.setCurrentIndex(JS08Settings.get('image_size'))

        self.image_label.paintEvent = self.lbl_paintEvent
        self.image_label.mousePressEvent = self.lbl_mousePressEvent
        self.image_label.mouseMoveEvent = self.lbl_mouseMoveEvent
        self.image_label.mouseReleaseEvent = self.lbl_mouseReleaseEvent

        self.buttonBox.accepted.connect(self.accept_click)
        self.buttonBox.rejected.connect(self.reject_click)

    def show_target_table(self):
        min_x = []
        min_y = []
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
            result = target_info.minrgb(upper_left, lower_right, copy_image)
            min_x.append(result[0])
            min_y.append(result[1])

            self.r_list.append(copy_image[result[1], result[0], 0])
            self.g_list.append(copy_image[result[1], result[0], 1])
            self.b_list.append(copy_image[result[1], result[0], 2])

        for i in range(0, row_count):
            # crop_image = copy_image[min_y[i] - 50: min_y[i] + 50, min_x[i] - 50: min_x[i] + 50, :].copy()
            # item = self.getImageLabel(crop_image)
            # self.tableWidget.setCellWidget(i, 0, item)

            item2 = QTableWidgetItem(f'target {i + 1}')
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

    def tableWidget_doubleClicked(self, event):
        self.select_target = self.tableWidget.currentIndex().row()
        self.update()

    def getImageLabel(self, image):
        imageLabel = QLabel()
        imageLabel.setScaledContents(True)
        height, width, channel = image.shape
        bytesPerLine = channel * width

        qImage = QImage(image.data.tobytes(), 100, 100, bytesPerLine, QImage.Format_RGB888)
        imageLabel.setPixmap(QPixmap.fromImage(qImage))

        return imageLabel

    def func(self, x, c1, c2, a):
        return c2 + (c1 - c2) * np.exp(-a * x)

    def chart_update(self):

        if self.chart_view is None:
            self.chart_view = self.chart_draw()

        if self.value_verticalLayout.count() == 0:
            self.chart_view = self.chart_draw()
            self.value_verticalLayout.addWidget(self.chart_view)
        else:
            new_chart_view = self.chart_draw()
            self.value_verticalLayout.removeWidget(self.chart_view)
            self.value_verticalLayout.addWidget(new_chart_view)
            self.value_verticalLayout.update()
            self.chart_view = new_chart_view

    def chart_draw(self):
        """세팅창 그래프 칸에 소산계수 차트를 그리는 함수"""

        try:
            self.x = np.linspace(self.distance[0], self.distance[-1], 100, endpoint=True)
            self.x.sort()

            hanhwa_opt_r, hanhwa_cov_r = curve_fit(self.func, self.distance, self.r_list, maxfev=5000)
            hanhwa_opt_g, hanhwa_cov_g = curve_fit(self.func, self.distance, self.g_list, maxfev=5000)
            hanhwa_opt_b, hanhwa_cov_b = curve_fit(self.func, self.distance, self.b_list, maxfev=5000)

            # chart object
            chart = QChart()
            font = QFont()
            font.setPixelSize(20)
            font.setBold(3)
            # palette = QPalette()
            # palette.setColor(QPalette.Window, QColor('red'))
            chart.setTitleFont(font)
            # chart.setPalette(palette)
            chart.setTitle('Extinction coefficient Graph')
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

            axis_x = QValueAxis()
            axis_x.setTickCount(7)
            axis_x.setLabelFormat('%i')
            axis_x.setTitleText('Distance(km)')
            axis_x.setRange(0, 6)
            chart.addAxis(axis_x, Qt.AlignBottom)

            axis_y = QValueAxis()
            axis_y.setTickCount(7)
            axis_y.setLabelFormat('%i')
            axis_y.setTitleText('Intensity')
            axis_y.setRange(0, 255)
            chart.addAxis(axis_y, Qt.AlignLeft)

            # Red Graph
            if self.red_checkBox.isChecked():
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

            # Green Graph
            if self.green_checkBox.isChecked():
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

            # Blue Graph
            if self.blue_checkBox.isChecked():
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
            chart_view.setMaximumSize(800, 500)

            return chart_view

        except TypeError as e:
            QMessageBox.about(self, 'Error', f'{e}')
            pass

    def camera_flip(self):
        if self.cam_flag:
            self.cam_flag = False
        else:
            self.cam_flag = True
        self.image_load()

    def btn_on(self, e):
        self.flip_button.setIcon(QIcon('resources/flip_on.png'))

    def btn_off(self, e):
        self.flip_button.setIcon(QIcon('resources/flip_off.png'))

    def image_load(self):
        self.left_range = None
        self.right_range = None

        if self.cam_flag:   # cam_flag is True = PNM_9031RV_rear
            src = JS08Settings.get('rear_camera_rtsp')
            self.current_camera = JS08Settings.get('rear_camera_name')
            self.target_setting_label.setText(f'  Rear Target Setting ({self.current_camera})')
            self.get_target(self.current_camera)

        else:   # cam_flag is False = PNM_9031RV_front
            src = JS08Settings.get('front_camera_rtsp')
            self.current_camera = JS08Settings.get('front_camera_name')
            self.target_setting_label.setText(f'  Front Target Setting ({self.current_camera})')
            self.get_target(self.current_camera)

        try:
            # print(f'Current camera - {self.current_camera.replace("_", " ")}')

            # os.makedirs(f'{JS08Settings.get("target_csv_path")}/{self.current_camera}', exist_ok=True)
            cap = cv2.VideoCapture(src)
            ret, cv_img = cap.read()
            cp_image = cv_img.copy()
            cap.release()

        except Exception as e:
            QMessageBox.about(self, 'Error', f'{e}')

        self.image_label.setPixmap(self.convert_cv_qt(cp_image))
        self.show_target_table()
        self.chart_update()

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
                                        Qt.KeepAspectRatio, Qt.SmoothTransformation)

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

    def lbl_paintEvent(self, event):
        painter = QPainter(self.image_label)

        back_ground_image = self.thumbnail(self.cp_image)
        bk_image = QPixmap.fromImage(back_ground_image)
        painter.drawPixmap(QRect(0, 0, self.image_label.width(),
                                 self.image_label.height()), bk_image)

        painter.setPen(QPen(Qt.white, 1, Qt.DotLine))

        painter.drawLine((self.image_label.width() * 0.125), 0,
                         (self.image_label.width() * 0.125), self.image_label.height())
        painter.drawLine((self.image_label.width() * 0.375), 0,
                         (self.image_label.width() * 0.375), self.image_label.height())
        painter.drawLine((self.image_label.width() * 0.625), 0,
                         (self.image_label.width() * 0.625), self.image_label.height())
        painter.drawLine((self.image_label.width() * 0.875), 0,
                         (self.image_label.width() * 0.875), self.image_label.height())

        if self.cam_flag:
            if time.strftime('%Y%m%d', time.localtime(time.time())):
                painter.setPen(QPen(Qt.black, 1, Qt.DotLine))
                painter.drawText(self.image_label.width() * 0.0625, 20, 'E')
                painter.drawText(self.image_label.width() * 0.25, 20, 'SE')
                painter.drawText(self.image_label.width() * 0.5, 20, 'S')
                painter.drawText(self.image_label.width() * 0.75, 20, 'SW')
                painter.drawText(self.image_label.width() * 0.9375, 20, 'W')
                painter.setPen(QPen(Qt.white, 1, Qt.DotLine))
        elif self.cam_flag is False:
            painter.drawText(self.image_label.width() * 0.0625, 20, 'W')
            painter.drawText(self.image_label.width() * 0.25, 20, 'NW')
            painter.drawText(self.image_label.width() * 0.5, 20, 'N')
            painter.drawText(self.image_label.width() * 0.75, 20, 'NE')
            painter.drawText(self.image_label.width() * 0.9375, 20, 'E')

        if self.left_range and self.right_range:
            for name, corner1, corner2, in zip(self.target_name, self.left_range, self.right_range):
                br = QBrush(QColor(100, 10, 10, 40))
                painter.setBrush(br)
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                corner1_1 = int(corner1[0] / self.video_width * self.image_label.width())
                corner1_2 = int(corner1[1] / self.video_height * self.image_label.height())
                corner2_1 = int((corner2[0] - corner1[0]) / self.video_width * self.image_label.width())
                corner2_2 = int((corner2[1] - corner1[1]) / self.video_height * self.image_label.height())
                painter.drawRect(QRect(corner1_1, corner1_2, corner2_1, corner2_2))
                painter.drawText(corner1_1 + corner2_1, corner1_2 - 5, f'{name[7:]}')

        # print(f'self.select_target: {self.select_target}')

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
            painter.eraseRect(QRect(self.end.x(), self.end.y(), 200, 200))
            self.end_drawing = False
            self.isDrawing = False
            painter.end()

    def lbl_mousePressEvent(self, event):
        """마우스 클릭시 발생하는 이벤트, QLabel method overriding"""

        # 좌 클릭시 실행
        if event.buttons() == Qt.LeftButton:
            self.isDrawing = True
            self.begin = event.pos()
            self.end = event.pos()
            self.upper_left = (int((self.begin.x() / self.image_label.width()) * self.video_width),
                               int((self.begin.y() / self.image_label.height()) * self.video_height))
            self.image_label.update()

            self.draw_flag = True

        # 우 클릭시 실행
        elif event.buttons() == Qt.RightButton:
            self.isDrawing = False

            text, ok = QInputDialog.getText(self, 'Delete target',
                                            'Input target number to delete')
            if ok:
                if text == '':
                    del self.target_name[-1]
                    del self.left_range[-1]
                    del self.right_range[-1]
                    del self.distance[-1]
                    del self.azimuth[-1]

                else:
                    if len(self.left_range) > 0:
                        text = int(text)
                        del self.target_name[text - 1]
                        del self.left_range[text - 1]
                        del self.right_range[text - 1]
                        del self.distance[text - 1]
                        del self.azimuth[text - 1]

            self.update()
            self.image_label.update()
            self.draw_flag = False

    def lbl_mouseMoveEvent(self, event):
        """마우스가 움직일 때 발생하는 이벤트, QLabel method overriding"""
        if event.buttons() == Qt.LeftButton:
            self.end = event.pos()
            self.image_label.update()
            self.isDrawing = True

    def lbl_mouseReleaseEvent(self, event):
        """마우스 클릭이 떼질 때 발생하는 이벤트, QLabel method overriding"""
        if self.draw_flag:
            if self.cam_flag:
                if 0 < self.upper_left[0] <= self.video_width * 0.125:
                    self.azimuth.append('E')
                elif self.video_width * 0.125 < self.upper_left[0] <= self.video_width * 0.375:
                    self.azimuth.append('SE')
                elif self.video_width * 0.375 < self.upper_left[0] <= self.video_width * 0.625:
                    self.azimuth.append('S')
                elif self.video_width * 0.625 < self.upper_left[0] <= self.video_width * 0.875:
                    self.azimuth.append('SW')
                elif self.video_width * 0.875 < self.upper_left[0] <= self.video_width:
                    self.azimuth.append('W')

            elif self.cam_flag is False:
                if 0 < self.upper_left[0] <= self.video_width * 0.125:
                    self.azimuth.append('W')
                elif self.video_width * 0.125 < self.upper_left[0] <= self.video_width * 0.375:
                    self.azimuth.append('NW')
                elif self.video_width * 0.375 < self.upper_left[0] <= self.video_width * 0.625:
                    self.azimuth.append('N')
                elif self.video_width * 0.625 < self.upper_left[0] <= self.video_width * 0.875:
                    self.azimuth.append('NE')
                elif self.video_width * 0.875 < self.upper_left[0] <= self.video_width:
                    self.azimuth.append('E')

            self.end = event.pos()
            self.image_label.update()
            self.lower_right = (int((self.end.x() / self.image_label.width()) * self.video_width),
                                int((self.end.y() / self.image_label.height()) * self.video_height))

            text, ok = QInputDialog.getText(self, '거리 입력', '거리(km)')

            if ok:
                self.left_range.append(self.upper_left)
                self.right_range.append(self.lower_right)
                self.distance.append(text)
                self.target_name.append('target_' + str(len(self.left_range)))

                # self.save_target(self.current_camera)
                self.isDrawing = False
                self.end_drawing = True
            else:
                self.isDrawing = False
                del self.azimuth[-1]

                self.image_label.update()

            self.show_target_table()

    def data_csv_path(self):
        fName = QFileDialog.getExistingDirectory(
            self, 'Select path to save data csv file', JS08Settings.get('data_csv_path'))
        if fName:
            self.data_csv_path_textBrowser.setPlainText(fName)
        else:
            pass

    def target_csv_path(self):
        fName = QFileDialog.getExistingDirectory(
            self, 'Select path to save target csv file', JS08Settings.get('target_csv_path'))
        if fName:
            self.target_csv_path_textBrowser.setPlainText(fName)
        else:
            pass

    def image_save_path(self):
        fName = QFileDialog.getExistingDirectory(
            self, 'Select path to save image file', JS08Settings.get('image_save_path'))
        if fName:
            self.image_save_path_textBrowser.setPlainText(fName)
        else:
            pass

    def afd_btn_click(self):
        dlg = FileAutoDelete()
        dlg.show()
        dlg.exec_()

    def save_vis(self):

        save_path_front = f'{JS08Settings.get("data_csv_path")}/{JS08Settings.get("front_camera_name")}/' \
                          f'{JS08Settings.get("front_camera_name")}.csv'

        print(save_path_front)

        col = ['datetime', 'camera_direction',
               'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW',
               'prevailing_visibility']
        result = pd.DataFrame(col)
        print(result)

        # result['datetime'] =
        # result['camera_direction'] =
        # result['N'] =
        # result['NE'] =
        # result['E'] =
        # result['SE'] =
        # result['S'] =
        # result['SW'] =
        # result['W'] =
        # result['NW'] =
        # result['prevailing_visibility'] =

        result.to_csv(f'{JS08Settings.get("data_csv_path")}/{self.current_camera}/{self.current_camera}.csv',
                      index=False)

    def save_target(self, camera: str):

        file = f'{JS08Settings.get("target_csv_path")}/{camera}/{camera}.csv'
        if self.left_range and os.path.isfile(file):
            col = ['target_name', 'left_range', 'right_range', 'distance', 'azimuth']
            result = pd.DataFrame(columns=col)
            result['target_name'] = self.target_name
            result['left_range'] = self.left_range
            result['right_range'] = self.right_range
            result['distance'] = self.distance
            result['azimuth'] = self.azimuth
            result.to_csv(file, mode='w', index=False)
            print(f'[{camera}.csv SAVED]')

    def get_target(self, camera: str):

        save_path = os.path.join(f'{JS08Settings.get("target_csv_path")}/{camera}')
        file = f'{save_path}/{camera}.csv'

        if os.path.isfile(f'{save_path}/{camera}.csv') is False:
            os.makedirs(f'{save_path}', exist_ok=True)
            makeFile = pd.DataFrame(columns=['target_name', 'left_range', 'right_range', 'distance', 'azimuth'])
            makeFile.to_csv(file, mode='w', index=False)

        target_df = pd.read_csv(f'{save_path}/{camera}.csv')
        self.target_name = target_df['target_name'].tolist()
        self.left_range = self.str_to_tuple(target_df['left_range'].tolist())
        self.right_range = self.str_to_tuple(target_df['right_range'].tolist())
        self.distance = target_df['distance'].tolist()
        self.azimuth = target_df['azimuth'].tolist()

    def accept_click(self):

        JS08Settings.set('data_csv_path', self.data_csv_path_textBrowser.toPlainText())
        JS08Settings.set('target_csv_path', self.target_csv_path_textBrowser.toPlainText())
        JS08Settings.set('image_save_path', self.image_save_path_textBrowser.toPlainText())
        JS08Settings.set('image_size', self.image_size_comboBox.currentIndex())
        JS08Settings.set('visibility_alert_limit', self.vis_limit_spinBox.value())
        JS08Settings.set('login_id', self.id_lineEdit.text())
        JS08Settings.set('login_pw', self.pw_lineEdit.text())

        self.save_target(self.current_camera)
        self.close()

    def reject_click(self):
        self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = JS08SettingWidget()
    ui.show()
    sys.exit(app.exec_())
