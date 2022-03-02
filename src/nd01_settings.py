
import datetime
import sys
import os
import time
import math
from tkinter.messagebox import RETRY

import cv2
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import curve_fit
# import PyQt5
# print(PyQt5.__version__)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog, QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QPoint, QRect, Qt, QRectF, QSize, QCoreApplication, pyqtSlot, QTimer, QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem


from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis

import target_info

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
        self.r_list = []
        self.g_list = []
        self.b_list = []
        self.x = None
        self.chart_view = None
        
        self.running_ave_checked = None
        
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
        
        self.target_name, self.left_range, self.right_range, self.distance = target_info.get_target("PNM_9030V")
    
        self.ten_radio_btn.setChecked(True)
        self.red_checkBox.setChecked(True)
        self.green_checkBox.setChecked(True)
        self.blue_checkBox.setChecked(True)
        
        if len(self.left_range) > 0:
            self.show_target_table()
        else:
            pass
        
        if len(self.left_range) > 4:
            self.chart_update()
        else:
            pass
        
        ## 라디오 버튼, 체크박스 이벤트시 함수와 연동 설정
        
        self.km_radio_btn.clicked.connect(self.radio_function)
        self.mile_radio_btn.clicked.connect(self.radio_function)  
        
        self.red_checkBox.clicked.connect(self.chart_update)
        self.green_checkBox.clicked.connect(self.chart_update)
        self.blue_checkBox.clicked.connect(self.chart_update)

        
        self.one_radio_btn.clicked.connect(self.running_avr_time_settings_function)
        self.five_radio_btn.clicked.connect(self.running_avr_time_settings_function)
        self.ten_radio_btn.clicked.connect(self.running_avr_time_settings_function)
    
    def func(self, x, c1, c2, a):
        return c2 + (c1 - c2) * np.exp(-a * x)
    
    def chart_update(self):
        """세팅창 그래프를 업데이트 하는 함수"""
        if self.html_verticalLayout.count() == 0:
            self.chart_view = self.chart_draw()
            self.html_verticalLayout.addWidget(self.chart_view)        
        else:
            new_chart_view = self.chart_draw()
            self.html_verticalLayout.removeWidget(self.chart_view)
            self.html_verticalLayout.addWidget(new_chart_view)            
            self.html_verticalLayout.update()
            self.chart_view = new_chart_view
            
        print("update chart!")
        
    def chart_draw(self):
        """세팅창 그래프 칸에 소산계수 차트를 그리는 함수"""
        # data
        global x   
        
        # if self.x is None:
        print("distance 리스트", self.distance)
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
        chart.setTitleFont(font)
        
        chart.setTitle('Extinction coefficient Graph')
        
        # chart.createDefaultAxes()
        axis_x = QValueAxis()
        axis_x.setTickCount(7)
        axis_x.setLabelFormat("%i")
        axis_x.setTitleText("Distance(km)")
        axis_x.setRange(0,20)        
        chart.addAxis(axis_x, Qt.AlignBottom)        
        
        axis_y = QValueAxis()
        axis_y.setTickCount(7)
        axis_y.setLabelFormat("%i")
        axis_y.setTitleText("Intensity")
        axis_y.setRange(0, 255)                
        chart.addAxis(axis_y, Qt.AlignLeft)
        
        # Red Graph
        if self.red_checkBox.isChecked():
        
            series1 = QLineSeries()
            series1.setName("Red")
            pen = QPen()
            pen.setWidth(2)
            series1.setPen(pen)
            series1.setColor(QColor("Red"))
            
            for dis in self.x:
                series1.append(*(dis, self.func(dis, *hanhwa_opt_r)))
            chart.addSeries(series1) # data feeding  
            series1.attachAxis(axis_x)
            series1.attachAxis(axis_y)
        
        # Green Graph
        if self.green_checkBox.isChecked():
        
            series2 = QLineSeries()
            series2.setName("Green")
            pen = QPen()
            pen.setWidth(2)
            series2.setPen(pen)   
            series2.setColor(QColor("Green")) 
            for dis in self.x:
                series2.append(*(dis, self.func(dis, *hanhwa_opt_g)))
            chart.addSeries(series2)  # data feeding
            
            series2.attachAxis(axis_x)
            series2.attachAxis(axis_y)  
            

        # Blue Graph
        if self.blue_checkBox.isChecked():
            series3 = QLineSeries()
            series3.setName("Blue")  
            pen = QPen()
            pen.setWidth(2)
            series3.setPen(pen)   
            series3.setColor(QColor("Blue"))
            for dis in self.x:
                series3.append(*(dis, self.func(dis, *hanhwa_opt_b)))
            chart.addSeries(series3)  # data feeding
            
            series3.attachAxis(axis_x)
            series3.attachAxis(axis_y)  

        chart.legend().setAlignment(Qt.AlignRight)
        
        # displaying chart
        chart.setBackgroundBrush(QBrush(QColor(22,32,42)))
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        return chart_view
    
    def running_avr_time_settings_function(self):
        """radio button 설정에 따라 Running Average 단위를 변경해서 설정하는 함수"""
        if self.one_radio_btn.isChecked():
            self.running_ave_checked = "One"
            
        elif self.five_radio_btn.isChecked():
            self.running_ave_checked = "Five"
            
        elif self.ten_radio_btn.isChecked():
            self.running_ave_checked = "Ten"

    def radio_function(self):
        """radio button 설정에 따라 시정 단위를 변경해서 출력하는 함수"""
        if self.km_radio_btn.isChecked():
            self.radio_flag = "Km"
            # print(self.radio_flag)
        elif self.mile_radio_btn.isChecked():
            self.radio_flag = "Mile"
            # print(self.radio_flag)
        
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
            # print("썸네일 삭제")
            painter.eraseRect(QRect(self.begin, self.end))
            painter.eraseRect(QRect(self.end.x(), self.end.y(), 200, 200))
            self.end_drawing = False
            self.isDrawing = False
            self.blank_lbl.update()
        painter.end()
            
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
                self.distance.append(float(text))
                self.target_name.append("target_" + str(len(self.left_range)))
                self.save_target()
                self.isDrawing = False
                self.end_drawing = True
                self.show_target_table()
            else:
                self.isDrawing = False
                self.blank_lbl.update()
            
            if len(self.left_range) > 4:
                self.chart_update()
    
    def save_target(self):
        """Save the target information for each camera."""
        try:
            save_path = os.path.join(f"target/PNM_9030V")
            os.mkdir(save_path)

        except Exception as e:
            pass
        
        
        print("target name 갯수 : ", len(self.target_name))
        print("left 좌표 갯수 : ", len(self.left_range))
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
        self.r_list = []
        self.g_list = []
        self.b_list = []
        
        
        copy_image = self.cp_image.copy()
        row_count = len(self.distance)
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        
        
        for upper_left, lower_right in zip(self.left_range, self.right_range):
            result = target_info.minrgb(upper_left, lower_right, copy_image)
            min_x.append(result[0])
            min_y.append(result[1])
            
            self.r_list.append(copy_image[result[1],result[0],0])
            self.g_list.append(copy_image[result[1],result[0],1])
            self.b_list.append(copy_image[result[1],result[0],2])
            
        for i in range(0, row_count):
            
            # 이미지 넣기            
            crop_image = copy_image[min_y[i] - 50: min_y[i] + 50, min_x[i] - 50: min_x[i] + 50, :].copy()
            cv2.rectangle(crop_image, (40, 40), (60, 60), (127, 0, 255), 2)
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
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    ui = ND01_Setting_Widget()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())

