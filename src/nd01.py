
import datetime
from nd01_settings import ND01_Setting_Widget
import sys
import os
import time
import math

import cv2
import numpy as np
import pandas as pd

# print(PyQt5.__version__)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog, QListWidgetItem, QFileDialog, QDockWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QPoint, QRect, Qt, QRectF, QSize, QCoreApplication, pyqtSlot, QTimer, QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings


from video_thread import VideoThread
from curved import CurvedThread
from ui.widget import Ui_js06_1920

import save_db

print(pd.__version__)

class ND01MainWindow(QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "ui/js06_1920.ui")
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
        # self.create_dir()        

        self.filepath = os.path.join(os.getcwd())
    #     # self.image_label.paintEvent = self.paintEvent

        # 카메라 영상을 보여줄 QGraphicsView 생성
        self.scene = QGraphicsScene(self)
        self.video_graphicsview = QGraphicsView(self.scene)
        self.video_graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_item = QGraphicsVideoItem()
        self.scene.addItem(self.video_item)
        
        self.verticallayout.addWidget(self.video_graphicsview)

        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.setUrl(QUrl("http://localhost:3000/d/GXA3xPS7z/new-dashboard-copy?orgId=1&refresh=30s&from=now-30m&to=now&kiosk"))
        # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.ShowScrollBars(False))
        self.webview.setZoomFactor(1)
        self.web_verticalLayout.addWidget(self.webview)

        # 영상을 재생시켜주는 QMediaPlayer 생성
        self._player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self._player.setVideoOutput(self.video_item)
        self._player.setPosition(0)
  
        VIDEO_SRC3 = "rtsp://admin:sijung5520@d617.asuscomm.com:1554/profile2/media.smp"
        
        CAM_NAME = "QNO-8080R"
        self.onCameraChange(VIDEO_SRC3, CAM_NAME, "Video")


        self.timer = QTimer()
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
        self.real_time_label.setText(current_time)
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
            return
    
    def save_frame(self, image: np.ndarray, epoch: str, g_ext, pm_25):
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

    def keyPressEvent(self, e):
        """키 입력할 때 동작하는 함수 QMainwindow KeyPressEvent를 오버라이딩"""
        if e.key() == Qt.Key_Escape:
            sys.exit()
        if e.key() == Qt.Key_F:
            self.showFullScreen()    

    def minprint(self):
        """지정한 구역들에서 소산계수 산출용 픽셀을 출력하는 함수"""

        epoch = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
        result = ()
        cnt = 1
        self.min_x = []
        self.min_y = []

        for upper_left, lower_right in zip(self.left_range, self.right_range):
            result = self.minrgb(upper_left, lower_right)
            self.min_x.append(result[0])
            self.min_y.append(result[1])
            cnt += 1

        self.get_rgb(epoch)

        self.curved_thread = CurvedThread(self.camera_name, epoch)
        self.curved_thread.update_extinc_signal.connect(self.extinc_print)
        self.curved_thread.run()

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

    def extinc_print(self, c1_list: list = [0, 0, 0], c2_list: list = [0, 0, 0], alp_list: list = [0, 0, 0], select_color: str = ""):

        self.g_ext = round(alp_list[1], 1)

        if select_color == "red" : 
            self.visibility_print(alp_list[0])
        elif select_color == "green" : 
            self.visibility_print(alp_list[1])
        else:
            self.visibility_print(alp_list[2])
        # self.pm_print(alp_list)

        

    def visibility_print(self, ext_g: float = 0.0):
        vis_value = 0

        vis_value = (3.912/ext_g)
        if vis_value > 20:
            vis_value = 20
        elif vis_value < 0.01:
            vis_value = 0.01

        self.data_save(vis_value)
        vis_value_str = f"{vis_value:.2f}" + " km"
        self.c_vis_label.setText(vis_value_str)
        

    def data_save(self, vis_data):
        """Database에 시정과 미세먼지 값을 저장한다."""

        save_db.SaveDB(vis_data)
        print("Data Save!")



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
        """Retrieves target information of a specific camera."""

        save_path = os.path.join(f"target/{self.camera_name}")
        print("Get target information")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ND01MainWindow()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
