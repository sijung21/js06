
import datetime
import sys
import os
import time
import math
from tkinter.messagebox import RETRY

import cv2
import numpy as np
import pandas as pd
# import PyQt5
# print(PyQt5.__version__)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog, QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QPoint, QRect, Qt, QRectF, QSize, QCoreApplication, pyqtSlot, QTimer, QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem



class ND01_Setting_Widget(QDialog):

    def __init__(self, radio_flag=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/test.ui")
        uic.loadUi(ui_path, self)
        
        self.begin = QPoint()
        self.end = QPoint()
        self.qt_img = QPixmap()
        self.isDrawing = False
        self.upper_left = ()
        self.lower_right = ()
        self.left_range = []
        self.right_range = []
        self.distance = []
        self.target_name = []
        self.min_x = []
        self.min_y = []
        self.min_xy = ()
        self.leftflag = False
        self.rightflag = False
        self.image_width = None
        self.image_height = None
        self.video_flag = False
        self.cp_image = None
        self.g_ext = None
        self.pm_25 = None
        self.test_name = None
        self.end_drawing = None
        self.cp_image = None
        
        self.radio_flag = radio_flag
        
        self.image_load()
        
        # 그림 그리는 Q레이블 생성
        self.blank_lbl = QLabel(self.target_setting_image_label)
        self.blank_lbl.setGeometry(0, 0, 1200, 500)
        self.blank_lbl.paintEvent = self.lbl_paintEvent

        self.blank_lbl.mousePressEvent = self.lbl_mousePressEvent
        self.blank_lbl.mouseMoveEvent = self.lbl_mouseMoveEvent
        self.blank_lbl.mouseReleaseEvent = self.lbl_mouseReleaseEvent
        
        if self.radio_flag == None or self.radio_flag == "Km":
            self.km_radio_btn.setChecked(True)
        elif self.radio_flag == "Mile":
            self.mile_radio_btn.setChecked(True)
        
        self.km_radio_btn.clicked.connect(self.radio_function)
        self.mile_radio_btn.clicked.connect(self.radio_function)
        
        self.get_target("PNM_9030V")
        
        self.show_target_table()

    def radio_function(self):
        """radio button 설정에 따라 시정 단위를 변경해서 출력하는 함수"""
        if self.km_radio_btn.isChecked():
            self.radio_flag = "Km"
            print(self.radio_flag)
        elif self.mile_radio_btn.isChecked():
            self.radio_flag = "Mile"
            print(self.radio_flag)
        
    def image_load(self):
        
        src = "rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp"
        try:
            cap = cv2.VideoCapture(src)
            ret, cv_img = cap.read()
            cp_image = cv_img.copy()
            cap.release()
        except Exception as e:
            print(e)
            self.image_load()
            
        self.target_setting_image_label.setPixmap(self.convert_cv_qt(cp_image))
        
    def convert_cv_qt(self, cv_img):
        """Convert CV image to QImage."""
        # self.epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        cv_img = cv_img.copy()
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        self.cp_image = cv_img.copy()
        img_height, img_width, ch = cv_img.shape
        self.image_width = int(img_width)
        self.image_height = int(img_height)
        # self.video_flag = True
        bytes_per_line = ch * img_width
        print(img_width, img_height)
        convert_to_Qt_format = QImage(cv_img.data, img_width, img_height, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(1200, 500, Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        print(self.target_setting_image_label.width(), self.target_setting_image_label.height())
        return QPixmap.fromImage(p)
    
    
    def lbl_paintEvent(self, event):
        self.horizontal_flag = True
        painter = QPainter(self.blank_lbl)

        # if self.camera_name == "Image" and self.video_flag:
        back_ground_image =  self.thumbnail(self.cp_image)
        bk_image = QPixmap.fromImage(back_ground_image)
        painter.drawPixmap(QRect(0, 0, 1200, 500), bk_image)

        # if self.horizontal_flag and self.video_flag:
        for corner1, corner2, in zip(self.left_range, self.right_range):
            br = QBrush(QColor(100, 10, 10, 40))
            painter.setBrush(br)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            corner1_1 = int(corner1[0]/self.image_width*self.blank_lbl.width())
            corner1_2 = int(corner1[1]/self.image_height*self.blank_lbl.height())
            corner2_1 = int((corner2[0]-corner1[0])/self.image_width*self.blank_lbl.width())
            corner2_2 = int((corner2[1]-corner1[1])/self.image_height*self.blank_lbl.height())
            painter.drawRect(QRect(corner1_1, corner1_2, corner2_1, corner2_2))
        
        if self.isDrawing:
            br = QBrush(QColor(100, 10, 10, 40))
            painter.setBrush(br)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(QRect(self.begin, self.end))
            # 썸네일 만들기
            th_x, th_y = self.thumbnail_pos(self.end)
            th_qimage = self.thumbnail(self.cp_image[th_y - 50 :th_y + 50, th_x - 50 :th_x + 50, :])
            thumbnail_image = QPixmap.fromImage(th_qimage)
            painter.drawPixmap(QRect(self.end.x(), self.end.y(), 200, 200), thumbnail_image)

        if self.end_drawing:
            print("썸네일 삭제")
            painter.eraseRect(QRect(self.begin, self.end))
            painter.eraseRect(QRect(self.end.x(), self.end.y(), 200, 200))
            self.end_drawing = False
            self.isDrawing = False
            self.blank_lbl.update()
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
            
    def str_to_tuple(self, before_list):
        """저장된 타겟들의 위치정보인 튜플 리스트가 문자열로 바뀌어 다시 튜플형태로 변환하는 함수"""
        tuple_list = [i.split(',') for i in before_list]
        tuple_list = [(int(i[0][1:]), int(i[1][:-1])) for i in tuple_list]
        return tuple_list
    
    # 타겟 조정 및 썸네일 관련 함수 시작
    def thumbnail_pos(self, end_pos):
        x = int((end_pos.x()/self.blank_lbl.width())*self.image_width)
        y = int((end_pos.y()/self.blank_lbl.height())*self.image_height)
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
            self.upper_left = (int((self.begin.x()/self.blank_lbl.width())*self.image_width),
                               int((self.begin.y()/self.blank_lbl.height())*self.image_height))
            self.blank_lbl.update()

            self.leftflag = True
            self.rightflag = False

        # 우 클릭시 실행
        elif event.buttons() == Qt.RightButton:
            self.isDrawing = False
            if len(self.left_range) > 0:
                del self.distance[-1]
                del self.target_name[-1]
                del self.left_range[-1]
                del self.right_range[-1]
                self.save_target()
                self.rightflag = True
            self.leftflag = False
            self.blank_lbl.update()
            self.show_target_table()

    def lbl_mouseMoveEvent(self, event):
        """마우스가 움직일 때 발생하는 이벤트, QLabel method overriding"""
        if event.buttons() == Qt.LeftButton:
            self.end = event.pos()
            self.blank_lbl.update()
            self.isDrawing = True

    def lbl_mouseReleaseEvent(self, event):
        """마우스 클릭이 떼질 때 발생하는 이벤트, QLabel method overriding"""
        if self.leftflag == True:
            self.end = event.pos()
            self.blank_lbl.update()
            self.lower_right = (int((self.end.x()/self.blank_lbl.width())*self.image_width),
                                int((self.end.y()/self.blank_lbl.height())*self.image_height))
            text, ok = QInputDialog.getText(self, '거리 입력', '거리(km)')
            if ok:
                self.left_range.append(self.upper_left)
                self.right_range.append(self.lower_right)
                self.distance.append(text)
                self.target_name.append("target_" + str(len(self.left_range)))
                self.save_target()
                self.isDrawing = False
                self.end_drawing = True
                self.show_target_table()
            else:
                self.isDrawing = False
                self.blank_lbl.update()
    
    def save_target(self):
        """Save the target information for each camera."""
        try:
            save_path = os.path.join(f"target/PNM_9030V")
            os.mkdir(save_path)

        except Exception as e:
            pass

        if self.left_range:
            col = ["target_name", "left_range", "right_range", "distance"]
            result = pd.DataFrame(columns=col)
            result["target_name"] = self.target_name
            result["left_range"] = self.left_range
            result["right_range"] = self.right_range
            result["distance"] = self.distance
            result.to_csv(f"{save_path}/PNM_9030V.csv", mode="w", index=False)
    
    def show_target_table(self):
        """ Target의 정보들을 테이블로 보여준다 """
        min_x = []
        min_y = []
        
        copy_image = self.cp_image.copy()
        row_count = len(self.distance)
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        
        
        for upper_left, lower_right in zip(self.left_range, self.right_range):
            result = self.minrgb(upper_left, lower_right, copy_image)
            min_x.append(result[0])
            min_y.append(result[1])
            
        for i in range(0, row_count):
            
            # 이미지 넣기            
            crop_image = copy_image[min_y[i] - 50: min_y[i] + 50, min_x[i] - 50: min_x[i] + 50, :].copy()
            cv2.rectangle(crop_image, (40, 40), (60, 60), (255, 0, 0), 2)
            item1 = self.getImagelabel(crop_image)
            self.tableWidget.setCellWidget(i, 0, item1)

            # target 번호 넣기
            item2 = QTableWidgetItem(f"Target_{i+1}")
            item2.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            item2.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget.setItem(i, 1, item2)
            
            # target 거리 넣기            
            item3 = QTableWidgetItem(f"{self.distance[i]}km")
            item3.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            item3.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget.setItem(i, 2, item3)
            
        
        self.tableWidget.verticalHeader().setDefaultSectionSize(90)
    
    def getImagelabel(self, image):
        """tableWidget의 셀 안에 넣을 이미지 레이블을 만드는 함수"""
        imageLabel_1 = QLabel()
        imageLabel_1.setScaledContents(True)
        height, width, channel = image.shape
        bytesPerLine = channel * width
        
        # 레이블에 이미지를 넣는다    
        qImg = QImage(image.data.tobytes(), 100, 100, bytesPerLine, QImage.Format_RGB888)
        # pixmap = QPixmap()
        
        imageLabel_1.setPixmap(QPixmap.fromImage(qImg))
        return imageLabel_1
            
    def minrgb(self, upper_left, lower_right, cp_image):
        """Extracts the minimum RGB value of the dragged area"""

        up_y = min(upper_left[1], lower_right[1])
        down_y = max(upper_left[1], lower_right[1])

        left_x = min(upper_left[0], lower_right[0])
        right_x = max(upper_left[0], lower_right[0])

        test = cp_image[up_y:down_y, left_x:right_x, :]

        r = test[:, :, 0]
        g = test[:, :, 1]
        b = test[:, :, 2]

        r = np.clip(r, 0, 765)
        sum_rgb = r + g + b

        t_idx = np.where(sum_rgb == np.min(sum_rgb))
        
        show_min_y = t_idx[0][0] + up_y
        show_min_x = t_idx[1][0] + left_x

        return (show_min_x, show_min_y)        
        # return
        
                
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    ui = ND01_Setting_Widget()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())

