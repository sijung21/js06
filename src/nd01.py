
import datetime
import sys
import os
import time
import math

import cv2
import numpy as np
import pandas as pd
# import PyQt5
# print(PyQt5.__version__)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog, QListWidgetItem, QFileDialog, QDockWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QPoint, QRect, Qt, QRectF, QSize, QCoreApplication, pyqtSlot, QTimer, QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

from video_thread import VideoThread
from curved import CurvedThread
from mainwindow import Ui_MainWindow
from video_thread import Js06VideoWidget2

print(pd.__version__)

class ND01MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "mainwindow.ui")
        uic.loadUi(ui_path, self)

        self.camera_name = ""
        self.video_thread = None
        # self.ipcam_start()
        self.begin = QPoint()
        self.end = QPoint()
        self.qt_img = QPixmap()
        self.isDrawing = False
        self.curved_thread = None

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
        self.create_dir()        

        self.filepath = os.path.join(os.getcwd())
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)
        MainWindow.keyPressEvent = self.keyPressEvent
        # self.image_label.paintEvent = self.paintEvent

        # self.video_dock = QDockWidget("Video", self)
        # self.video_dock.setFeatures(
            # QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable)
        # self.video_widget = Js06VideoWidget2(self)
        # self.gridLayout.setWidget(self.video_widget)
        # self.setCentralWidget(self.video_widget)

        # 카메라 영상을 보여줄 QGraphicsView 생성
        self.scene = QGraphicsScene(self)
        self.video_graphicsview = QGraphicsView(self.scene)
        self.video_graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_item = QGraphicsVideoItem()
        self.scene.addItem(self.video_item)
        
        self.verticallayout.addWidget(self.video_graphicsview)

        # 영상을 재생시켜주는 QMediaPlayer 생성
        self._player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self._player.setVideoOutput(self.video_item)
        self._player.setPosition(0)
  
        VIDEO_SRC3 = "rtsp://admin:sijung5520@d617.asuscomm.com:3554/profile2/media.smp"
        
        CAM_NAME = "QNO-8080R"
        self.actionQNO_8080R.triggered.connect((lambda: self.onCameraChange(VIDEO_SRC3, CAM_NAME, "Video")))
        self.actionQNO_8080R.triggered.connect((lambda: self.test_settings("image")))
        self.actionTC5.triggered.connect((lambda: self.onCameraChange(VIDEO_SRC3, CAM_NAME, "Video")))
        self.actionTC5.triggered.connect((lambda: self.test_settings("TC5")))
        self.actionTC7.triggered.connect((lambda: self.onCameraChange(VIDEO_SRC3, CAM_NAME, "Video")))
        self.actionTC7.triggered.connect((lambda: self.test_settings("TC7")))
        self.actionImage.triggered.connect(self.read_image)
        self.actionPrint.triggered.connect(self.minprint)
        # 그림 그리는 Q레이블 생성
        self.blank_lbl = QLabel(self.video_graphicsview)
        self.blank_lbl.setGeometry(0, 0, 1919, 570)
        self.blank_lbl.paintEvent = self.lbl_paintEvent

        self.blank_lbl.mousePressEvent = self.lbl_mousePressEvent
        self.blank_lbl.mouseMoveEvent = self.lbl_mouseMoveEvent
        self.blank_lbl.mouseReleaseEvent = self.lbl_mouseReleaseEvent

        self.timer = QTimer(MainWindow)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout_run)

    @pyqtSlot(str)
    def onCameraChange(self, url, camera_name, src_type):
        self.camera_name = camera_name
        self._player.setMedia(QMediaContent(QUrl(url)))
        self.video_graphicsview.fitInView(self.video_item)
        self._player.play()

        self.get_target(self.camera_name)

        self.video_thread = VideoThread(url, src_type)
        self.video_thread.update_pixmap_signal.connect(self.convert_cv_qt)
        self.video_thread.start()

    def timeout_run(self):
        current_time = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))
        self.time_label_name.setText(current_time)
        self.video_graphicsview.fitInView(self.video_item)

    def convert_cv_qt(self, cv_img):
        self.epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        self.cp_image = cv_img.copy()
        self.cp_image = cv2.cvtColor(self.cp_image, cv2.COLOR_BGR2RGB)
        img_height, img_width, ch = cv_img.shape
        self.image_width = int(img_width)
        self.image_height = int(img_height)
        self.video_flag = True
        bytes_per_line = ch * img_width

        if self.epoch[-2:] == "00":
            self.minprint()
            if self.pm_25 is not None and self.g_ext is not None and self.test_name is not None:
                self.save_frame(cv_img, self.epoch, self.g_ext, self.pm_25)
                self.g_ext = None
                self.pm_25 = None
                return
        
        if self.camera_name == "Image":
            convert_to_Qt_format = QImage(cv_img.data, img_width, img_height, bytes_per_line,
                                            QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
            return QPixmap.fromImage(p)
    
    def save_frame(self, image: np.ndarray, epoch: str, g_ext, pm_25):
        # image_path = os.path.join(self.filepath, f"{self.test_name}", f"{self.camera_name}")
        image_path = os.path.join(self.filepath, f"{self.test_name}")
        file_name = f"{epoch}"
        if not os.path.isdir(image_path):
            os.makedirs(image_path)

        g_ext = round(g_ext / 1000, 4)

        if not os.path.isfile(f"{image_path}/{file_name}_{g_ext}_{pm_25}.jpg"):
            cv2.imwrite(f"{image_path}/{file_name}_{g_ext}_{pm_25}.jpg", image)
            del image
            del image_path
            cv2.destroyAllWindows()
            print(file_name , " 이미지가 저장되었습니다.")
            return

    def test_settings(self, test_name):

        if self.test_name is not None:
            self.test_name = None

        if self.test_name is None:
            self.test_name = test_name


    def lbl_paintEvent(self, event):
        self.horizontal_flag = True
        painter = QPainter(self.blank_lbl)

        if self.camera_name == "Image" and self.video_flag:
            back_ground_image =  self.thumbnail(self.cp_image)
            bk_image = QPixmap.fromImage(back_ground_image)
            painter.drawPixmap(QRect(0, 0, 1919, 570), bk_image)

        if self.horizontal_flag and self.video_flag:
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

        painter.end()

    def create_dir(self):
        """정보를 저장할 폴더(경로)들을 만든다."""
        folder_name = ["target", "image", "extinction", "rgb"]

        for f_name in folder_name:
            try:
                os.mkdir(f_name)
                print(f"{f_name} 폴더를 생성했습니다.")
            except Exception as e:
                pass

    def read_image(self):
        self.bgrfilter = True
        self.camera_name = "Image"
        print("read_Image 실행")
        self.get_target(self.camera_name)

        if self.video_thread is not None:
            self.video_thread.stop()

        imagePath, _ = QFileDialog.getOpenFileName(directory="D:/kriss/vis_20km/name_modify_vis20/p01")
        
        print(imagePath)
        if imagePath:
            self.video_thread = VideoThread(imagePath, "Image")
            self.video_thread.update_pixmap_signal.connect(self.update_image)
            self.video_thread.start()
        else:
            return



    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        
        self.qt_img = self.convert_cv_qt(cv_img)
        self.blank_lbl.setPixmap(self.qt_img)
        print("이미지 업데이트")

    # def convert_cv_qt(self, cv_img):
    #     """Convert from an opencv image to QPixmap"""
    #     if self.bgrfilter:
    #         rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    #         self.cp_image = rgb_image.copy()
    #     else:
    #         rgb_image = self.cp_image.copy()

    #     self.img_height, self.img_width, ch = rgb_image.shape
    #     self.label_width = self.image_label.width()
    #     self.label_height = self.image_label.height()
    #     bytes_per_line = ch * self.img_width

    #     rec_color = (139, 0, 255)
    #     tar_color = (0, 255, 0)

    #     for corner1, corner2 in zip(self.left_range, self.right_range):
    #         cv2.rectangle(rgb_image, corner1, corner2, rec_color, 6)
    #     if len(self.min_xy) > 0:
    #         cv2.rectangle(rgb_image, (self.min_xy[0]-10, self.min_xy[1]-10), (self.min_xy[0]+10, self.min_xy[1]+10), tar_color, 4)
    #     self.last_image = rgb_image.copy()

    #     convert_to_Qt_format = QImage(rgb_image.data, self.img_width, self.img_height, bytes_per_line,
    #                                         QImage.Format_RGB888)
    #     p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio,
    #                                     Qt.SmoothTransformation)
    #     self.bgrfilter = False

    #     return QPixmap.fromImage(p)

    # def paintEvent(self, event):
    #     """레이블 위에 그림을 그리는 함수, QLabel method overriding"""
    #     qp = QPainter(self.image_label)
    #     qp.drawPixmap(self.image_label.rect(), self.qt_img)

    #     if self.isDrawing:
    #         br = QBrush(QColor(100, 10, 10, 40))
    #         qp.setBrush(br)
    #         qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
    #         qp.drawRect(QRect(self.begin, self.end))
    #         # 썸네일 만들기
    #         th_x, th_y = self.thumbnail_pos(self.end)
    #         th_qimage = self.thumbnail(self.cp_image[th_y - 50 :th_y + 50, th_x - 50 :th_x + 50, :])
    #         thumbnail_image = QPixmap.fromImage(th_qimage)
    #         qp.drawPixmap(QRect(self.end.x(), self.end.y(), 200, 200), thumbnail_image)

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
            text, ok = QInputDialog.getText(self.centralwidget, '거리 입력', '거리(km)')
            if ok:
                self.left_range.append(self.upper_left)
                self.right_range.append(self.lower_right)
                self.distance.append(text)
                self.min_xy = self.minrgb(self.upper_left, self.lower_right)
                self.target_name.append("target_" + str(len(self.left_range)))
                self.save_target()
                self.isDrawing = False
                self.end_drawing = True
            else:
                self.isDrawing = False
                self.blank_lbl.update()
                # self.update_image(self.last_image)
                # self.minprint()

    #     if self.rightflag:
    #         self.update_image(self.last_image)

    #     self.isDrawing = False

    def keyPressEvent(self, e):
        """키 입력할 때 동작하는 함수 QMainwindow KeyPressEvent를 오버라이딩"""
        if e.key() == Qt.Key_Escape:
            sys.exit()

    

    def minprint(self):
        """지정한 구역들에서 소산계수 산출용 픽셀을 출력하는 함수"""

        epoch = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
        print("소산계수 좌표 출력")
        result = ()
        cnt = 1
        self.min_x = []
        self.min_y = []

        for upper_left, lower_right in zip(self.left_range, self.right_range):
            result = self.minrgb(upper_left, lower_right)
            print(f"target{cnt}의 소산계수 검출용 픽셀위치 =  ", result)
            self.min_x.append(result[0])
            self.min_y.append(result[1])
            cnt += 1

        self.get_rgb(epoch)

        self.curved_thread = CurvedThread(self.camera_name, epoch)
        self.curved_thread.update_extinc_signal.connect(self.extinc_print)
        self.curved_thread.run()

        self.list_test()

        graph_dir = os.path.join(f"extinction/{self.camera_name}")

        if os.path.isfile(f"{graph_dir}/{epoch}.png"):
            graph_image = cv2.imread(f"{graph_dir}/{epoch}.png")
            graph_image = cv2.cvtColor(graph_image, cv2.COLOR_BGR2RGB)

            img_height, img_width, ch = graph_image.shape
            bytes_per_line = ch * img_width

            convert_to_Qt_format = QImage(graph_image.data, img_width, img_height, bytes_per_line,
                                        QImage.Format_RGB888)

            p = convert_to_Qt_format.scaled(self.graph_label.width(), self.graph_label.height(), Qt.IgnoreAspectRatio,
                                            Qt.SmoothTransformation)

            self.graph_label.setPixmap(QPixmap.fromImage(p))
        
        # return g_ext, pm_25

    def minrgb(self, upper_left, lower_right):
        """드래그한 영역의 RGB 최솟값을 추출한다"""

        up_y = min(upper_left[1], lower_right[1])
        down_y = max(upper_left[1], lower_right[1])

        left_x = min(upper_left[0], lower_right[0])
        right_x = max(upper_left[0], lower_right[0])

        test = self.cp_image[up_y:down_y, left_x:right_x, :]

        # 드래그한 영역의 RGB 값을 각각 추출한다.
        r = test[:, :, 0]
        g = test[:, :, 1]
        b = test[:, :, 2]

        # RGB값을 각 위치별로 모두 더한다.
        # RGB 최댓값이 255로 정해져있어 값을 초과하면 0부터 시작된다. numpy의 clip 함수를 이용해 array의 최댓값을 수정한다.
        r = np.clip(r, 0, 765)
        sum_rgb = r + g + b

        # RGB 값을 합한 뒤 가장 최솟값의 index를 추출한다.
        t_idx = np.where(sum_rgb == np.min(sum_rgb))

        show_min_y = t_idx[0][0] + up_y
        show_min_x = t_idx[1][0] + left_x

        return (show_min_x, show_min_y)

    def get_rgb(self, epoch: str):
        r_list = []
        g_list = []
        b_list = []

        for x, y in zip(self.min_x, self.min_y):

            r_list.append(self.cp_image[y, x, 0])
            g_list.append(self.cp_image[y, x, 1])
            b_list.append(self.cp_image[y, x, 2])

        self.save_rgb(r_list, g_list, b_list, epoch)

    def save_rgb(self, r_list, g_list, b_list, epoch):
        """Save the rgb information for each target."""
        try:
            save_path = os.path.join(f"rgb/{self.camera_name}")
            os.mkdir(save_path)

        except Exception as e:
            pass

        if r_list:
            col = ["target_name", "r", "g", "b", "distance"]
            result = pd.DataFrame(columns=col)
            result["target_name"] = self.target_name
            result["r"] = r_list
            result["g"] = g_list
            result["b"] = b_list
            result["distance"] = self.distance
            result.to_csv(f"{save_path}/{epoch}.csv", mode="w", index=False)

    def extinc_print(self, c1_list: list = [0, 0, 0], c2_list: list = [0, 0, 0], alp_list: list = [0, 0, 0]):

        self.r_c1_textbox.setPlainText(f"{c1_list[0]:.4f}")
        self.g_c1_textbox.setPlainText(f"{c1_list[1]:.4f}")
        self.b_c1_textbox.setPlainText(f"{c1_list[2]:.4f}")

        self.r_c2_textbox.setPlainText(f"{c2_list[0]:.4f}")
        self.g_c2_textbox.setPlainText(f"{c2_list[1]:.4f}")
        self.b_c2_textbox.setPlainText(f"{c2_list[2]:.4f}")

        self.r_alpha_textbox.setPlainText(f"{alp_list[0]:.6f}")
        self.g_alpha_textbox.setPlainText(f"{alp_list[1]:.6f}")
        self.b_alpha_textbox.setPlainText(f"{alp_list[2]:.6f}")
        self.g_ext = round(alp_list[1], 1)
        self.visibility_print(alp_list[1])
        self.pm_print(alp_list)

    def visibility_print(self, ext_g: float = 0.0):
        vis_value = 0

        vis_value = (3.912/ext_g)
        
        vis_value_str = f"{vis_value:.2f}" + " km"
        self.visibility_value.setText(vis_value_str)

    def pm_print(self, ext_list: list):

        r_ext_pm = ext_list[0]*1000/4/2.5
        g_ext_pm = ext_list[1]*1000/4/2.5
        b_ext_pm = ext_list[2]*1000/4/2.5
        

        pm_value = b_ext_pm/(1+5.67*((85/100)**5.8))
        pm_value_str = f"{pm_value:.2f}" + r" ug/m^3"
        self.pm_25 = round(pm_value, 2)
        self.pm25_value.setText(pm_value_str)



    def save_target(self):
        """Save the target information for each camera."""
        try:
            save_path = os.path.join(f"target/{self.camera_name}")
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
            result.to_csv(f"{save_path}/{self.camera_name}.csv", mode="w", index=False)

    def get_target(self, camera_name: str):
        """특정 카메라의 타겟 정보들을 불러온다."""

        save_path = os.path.join(f"target/{self.camera_name}")
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

    def list_test(self):
        """소산계수 검출용 이미지들을 리스트뷰에 보여주는 함수"""
        self.imagelist.clear()
        cnt = 0
        for x, y in zip(self.min_x, self.min_y):

            image = self.cp_image[y-50:y+50, x-50:x+50, :].copy()
            cv2.rectangle(image, (40, 40), (60, 60), (255, 0, 0), 2)

            image = self.cvt_cv_qpixamp(image)
            icon_image = QIcon(image)
            item_image = QListWidgetItem(icon_image, "target")
            item_image.setSizeHint(QSize(200, 110))
            item_image.setTextAlignment(Qt.AlignTop)

            self.imagelist.addItem(item_image)
            # self.imagelist.setItem(1, cnt, item_image)
            cnt += 1

    def cvt_cv_qpixamp(self, image: np.ndarray):
        """cv 이미지를 qpixmap으로 변환하는 함수"""
        img_height, img_width, ch = image.shape
        bytes_per_line = ch * img_width

        convert_to_Qt_format = QImage(image.data.tobytes(), img_width, img_height,
                                    QImage.Format_RGB888)

        p = convert_to_Qt_format.scaled(self.cp_image.shape[1], self.cp_image.shape[0], Qt.IgnoreAspectRatio,
                                        Qt.SmoothTransformation)

        return QPixmap.fromImage(p)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ND01MainWindow()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
