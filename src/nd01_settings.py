#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import os
import cv2
import pandas as pd

from PyQt5.QtGui import (QPixmap, QPainter, QBrush,
                         QColor, QPen, QImage,
                         QIcon)
from PyQt5.QtWidgets import (QApplication, QLabel, QInputDialog,
                             QDialog, QAbstractItemView, QVBoxLayout,
                             QGridLayout, QPushButton, QMessageBox)
from PyQt5.QtCore import (QPoint, QRect, Qt)

from PyQt5 import uic


class ND01SettingWidget(QDialog):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/settings.ui")
        uic.loadUi(ui_path, self)
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.begin = QPoint()
        self.end = QPoint()
        self.upper_left = ()
        self.lower_right = ()
        self.left_range = []
        self.right_range = []
        self.distance = []
        self.target_name = []
        self.min_xy = ()

        self.isDrawing = False
        self.draw_flag = False
        self.cam_flag = False

        self.video_width = 0
        self.video_height = 0

        self.cp_image = None
        self.end_drawing = None

        self.current_camera = ""

        self.image_load()

        # 그림 그리는 삐뮤디 생성
        # self.blank_lbl = QLabel(self.target_setting_image_label)
        # # self.blank_lbl.setGeometry(0, 0, 1200, 500)
        # self.blank_lbl.paintEvent = self.lbl_paintEvent
        #
        # self.blank_lbl.mousePressEvent = self.lbl_mousePressEvent
        # self.blank_lbl.mouseMoveEvent = self.lbl_mouseMoveEvent
        # self.blank_lbl.mouseReleaseEvent = self.lbl_mouseReleaseEvent

        self.flip_button.clicked.connect(self.camera_flip)
        self.flip_button.enterEvent = self.btn_on
        self.flip_button.leaveEvent = self.btn_off

        self.target_setting_image_label.paintEvent = self.lbl_paintEvent
        self.target_setting_image_label.mousePressEvent = self.lbl_mousePressEvent
        self.target_setting_image_label.mouseMoveEvent = self.lbl_mouseMoveEvent
        self.target_setting_image_label.mouseReleaseEvent = self.lbl_mouseReleaseEvent

        self.get_target("PNM_9022V")

    def camera_flip(self):
        if self.cam_flag:
            self.cam_flag = False
        else:
            self.cam_flag = True
        self.image_load()

    def btn_on(self, e):
        self.flip_button.setIcon(QIcon('ui/resources/icon/flip_on.png'))

    def btn_off(self, e):
        self.flip_button.setIcon(QIcon('ui/resources/icon/flip_off.png'))

    def image_load(self):
        self.target_setting_image_label.setStyleSheet('background-image:')
        if self.cam_flag:
            src = "rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp"
            self.target_setting_label.setText('  Rear Target Setting')
        else:
            src = "rtsp://admin:sijung5520@192.168.100.101/profile2/media.smp"
            self.target_setting_label.setText('  Front Target Setting')

        try:
            cap = cv2.VideoCapture(src)
            ret, cv_img = cap.read()
            cp_image = cv_img.copy()
            cap.release()
        except Exception as e:
            QMessageBox.about(self, 'Error', f'{e}')

        self.target_setting_image_label.setPixmap(self.convert_cv_qt(cp_image))

    def convert_cv_qt(self, cv_img):
        """Convert CV image to QImage."""
        cv_img = cv_img.copy()
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        self.cp_image = cv_img.copy()

        self.video_height, self.video_width, ch = cv_img.shape

        bytes_per_line = ch * self.video_width
        convert_to_Qt_format = QImage(cv_img.data, self.video_width, self.video_height,
                                      bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.target_setting_image_label.width(),
                                        self.target_setting_image_label.height(),
                                        Qt.KeepAspectRatio, Qt.SmoothTransformation)

        return QPixmap.fromImage(p)

    def lbl_paintEvent(self, event):
        painter = QPainter(self.target_setting_image_label)

        back_ground_image = self.thumbnail(self.cp_image)
        bk_image = QPixmap.fromImage(back_ground_image)
        painter.drawPixmap(QRect(0, 0, self.target_setting_image_label.width(),
                                 self.target_setting_image_label.height()), bk_image)

        for corner1, corner2, in zip(self.left_range, self.right_range):
            br = QBrush(QColor(100, 10, 10, 40))
            painter.setBrush(br)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            corner1_1 = int(corner1[0] / self.video_width * self.target_setting_image_label.width())
            corner1_2 = int(corner1[1] / self.video_height * self.target_setting_image_label.height())
            corner2_1 = int((corner2[0] - corner1[0]) / self.video_width * self.target_setting_image_label.width())
            corner2_2 = int((corner2[1] - corner1[1]) / self.video_height * self.target_setting_image_label.height())
            painter.drawRect(QRect(corner1_1, corner1_2, corner2_1, corner2_2))

        if self.isDrawing:
            br = QBrush(QColor(100, 10, 10, 40))
            painter.setBrush(br)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(QRect(self.begin, self.end))
            th_x, th_y = self.thumbnail_pos(self.end)
            th_qimage = self.thumbnail(self.cp_image[th_y - 50:th_y + 50, th_x - 50:th_x + 50, :])
            thumbnail_image = QPixmap.fromImage(th_qimage)
            painter.drawPixmap(QRect(self.end.x(), self.end.y(), 200, 200), thumbnail_image)

        if self.end_drawing:
            painter.eraseRect(QRect(self.begin, self.end))
            painter.eraseRect(QRect(self.end.x(), self.end.y(), 200, 200))
            self.end_drawing = False
            self.isDrawing = False
            painter.end()

    def get_target(self, camera_name: str):
        """특정 카메라의 타겟 정보들을 불러온다."""

        save_path = os.path.join(f"target/{camera_name}")
        print("타겟을 불러옵니다.")
        if os.path.isfile(f"{save_path}/{camera_name}.csv"):
            target_df = pd.read_csv(f"{save_path}/{camera_name}.csv")
            self.target_name = target_df["target_name"].tolist()
            self.left_range = target_df["left_range"].tolist()
            self.left_range = self.str_to_tuple(self.left_range)
            self.right_range = target_df["right_range"].tolist()
            self.right_range = self.str_to_tuple(self.right_range)
            self.distance = target_df["distance"].tolist()

    def save_target(self, camera_name: str):
        print(f'타겟을 저장합니다 - {camera_name}')

    def str_to_tuple(self, before_list):
        """저장된 타겟들의 위치정보인 튜플 리스트가 문자열로 바뀌어 다시 튜플형태로 변환하는 함수"""
        tuple_list = [i.split(',') for i in before_list]
        tuple_list = [(int(i[0][1:]), int(i[1][:-1])) for i in tuple_list]
        return tuple_list

    # 타겟 조정 및 썸네일 관련 함수 시작
    def thumbnail_pos(self, end_pos):
        x = int((end_pos.x() / self.target_setting_image_label.width()) * self.video_width)
        y = int((end_pos.y() / self.target_setting_image_label.height()) * self.video_height)
        return x, y

    def thumbnail(self, image):
        height, width, channel = image.shape
        bytesPerLine = channel * width
        qImg = QImage(image.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg

    def lbl_mousePressEvent(self, event):
        """마우스 클릭시 발생하는 이벤트, QLabel method overriding"""

        # 좌 클릭시 실행
        if event.buttons() == Qt.LeftButton:
            self.isDrawing = True
            self.begin = event.pos()
            self.end = event.pos()
            self.upper_left = (int((self.begin.x() / self.target_setting_image_label.width()) * self.video_width),
                               int((self.begin.y() / self.target_setting_image_label.height()) * self.video_height))
            self.target_setting_image_label.update()

            self.draw_flag = True

        # 우 클릭시 실행
        elif event.buttons() == Qt.RightButton:
            self.isDrawing = False
            if len(self.left_range) > 0:
                del self.distance[-1]
                del self.target_name[-1]
                del self.left_range[-1]
                del self.right_range[-1]
                self.save_target(self.current_camera)
            self.draw_flag = False
            self.target_setting_image_label.update()

    def lbl_mouseMoveEvent(self, event):
        """마우스가 움직일 때 발생하는 이벤트, QLabel method overriding"""
        if event.buttons() == Qt.LeftButton:
            self.end = event.pos()
            self.target_setting_image_label.update()
            self.isDrawing = True

    def lbl_mouseReleaseEvent(self, event):
        """마우스 클릭이 떼질 때 발생하는 이벤트, QLabel method overriding"""
        if self.draw_flag:
            self.end = event.pos()
            self.target_setting_image_label.update()
            self.lower_right = (int((self.end.x() / self.target_setting_image_label.width()) * self.video_width),
                                int((self.end.y() / self.target_setting_image_label.height()) * self.video_height))
            text, ok = QInputDialog.getText(self, '거리 입력', '거리(km)')
            if ok:
                self.left_range.append(self.upper_left)
                self.right_range.append(self.lower_right)
                self.distance.append(text)
                # self.min_xy = self.minrgb(self.upper_left, self.lower_right)
                self.target_name.append("target_" + str(len(self.left_range)))
                # self.save_target()
                self.isDrawing = False
                self.end_drawing = True

                print(f'{text} km')
            else:
                self.isDrawing = False
                self.target_setting_image_label.update()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = ND01SettingWidget()
    ui.show()
    sys.exit(app.exec_())
