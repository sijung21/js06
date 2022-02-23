
import datetime
from nd01_settings import ND01_Setting_Widget
import sys
import os
import time
import math

import cv2
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue
import multiprocessing as mp

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


from video_thread_mp import CurveThread
import video_thread_mp
import save_db

from nd01_settings import ND01_Setting_Widget

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
        self.radio_checked = None
        self.visibility_copy = 0
        self.running_ave_checked = None
        self.q_list = []
        self.q_list_scale = 300

        self.filepath = os.path.join(os.getcwd())
    #     # self.image_label.paintEvent = self.paintEvent

        # Create a QGraphicsView to show the camera image
        self.scene = QGraphicsScene(self)
        self.video_graphicsview = QGraphicsView(self.scene)
        self.video_graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_item = QGraphicsVideoItem()
        self.scene.addItem(self.video_item)
        
        self.verticallayout.addWidget(self.video_graphicsview)

        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.setUrl(QUrl("http://localhost:3000/d/GXA3xPS7z/new-dashboard-copy?orgId=1&kiosk&from=now-1h&to=now"))
        # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.ShowScrollBars(False))
        self.webview.setZoomFactor(1)
        self.web_verticalLayout.addWidget(self.webview)

        # Create QMediaPlayer that plays video
        self._player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self._player.setVideoOutput(self.video_item)
        self._player.setPosition(0)
  
        VIDEO_SRC3 = "rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp"
        
        CAM_NAME = "PNM_9030V"
        self.onCameraChange(VIDEO_SRC3, CAM_NAME, "Video")
        
        self.settings_button.clicked.connect(self.btn_test)
        
        self.video_thread = CurveThread(VIDEO_SRC3, "Video", q)
        self.video_thread.update_visibility_signal.connect(self.print_data)
        self.video_thread.start()

        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout_run)
    
    @pyqtSlot()
    def btn_test(self):
        self._player.stop()
        # app = QApplication(sys.argv)
        if self.radio_checked == None:
            dlg = ND01_Setting_Widget("Km")
        else:
            dlg = ND01_Setting_Widget(self.radio_checked)
        dlg.show()
        # sys.exit(app.exec_())
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
        
        self.radio_checked = dlg.radio_flag
        print(self.radio_checked, "변환 완료")
        
        self.running_ave_checked = dlg.running_ave_checked
        print(self.running_ave_checked, "변환 완료")
        
        if self.running_ave_checked == "One":
            self.q_list_scale = 30
        elif self.running_ave_checked == "Five":
            self.q_list_scale = 150
        elif self.running_ave_checked == "Ten":
            self.q_list_scale = 300
            
        self._player.play()
        self._player.play()
                
    @pyqtSlot(str)
    def print_data(self, visibility):
        print(visibility)
        visibility_float = round(float(visibility), 3)
        
        if len(self.q_list) == 0 or self.q_list_scale != len(self.q_list):
            self.q_list = []
            for i in range(self.q_list_scale):
                self.q_list.append(visibility_float)
                
            print("q 리스트 길이", len(self.q_list))
            result_vis = np.mean(self.q_list)
        else:
            print("q 리스트 길이2", len(self.q_list))
            self.q_list.pop(0)
            self.q_list.append(visibility_float)
            result_vis = np.mean(self.q_list)            
        
        self.visibility_copy = round(float(result_vis), 3)
        
        if self.radio_checked == None or self.radio_checked == "Km":
            visibility_text = str(self.visibility_copy) + " km"
            print(visibility_text)
        elif self.radio_checked == "Mile":
            visibility_mile = round(self.visibility_copy / 1.609, 1)
            print(visibility_mile)
            visibility_text = str(visibility_mile) + " mi"
        
        self.c_vis_label.setText(visibility_text)
        
        ext = 3.912 / self.visibility_copy
        hd = 89
        pm_value = round((ext*1000/4/2.5)/(1+5.67*((hd/100)**5.8)),2)
        pm_text = str(pm_value) + " ㎍/㎥"
        self.c_pm_label.setText(pm_text)
        
        self.data_storage(self.visibility_copy)
        # self.statusBar().showMessage(data)
        
    @pyqtSlot(str)
    def onCameraChange(self, url, camera_name, src_type):
        """Connect the IP camera and run the video thread."""
        self.camera_name = camera_name
        self._player.setMedia(QMediaContent(QUrl(url)))
        # self.video_graphicsview.fitInView(self.video_item)
        self._player.play()

        # self.get_target(self.camera_name)

    def timeout_run(self):
        """Print the current time."""
        current_time = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))
        self.real_time_label.setText(current_time)
        self.video_graphicsview.fitInView(self.video_item)

    def convert_cv_qt(self, cv_img):
        """Convert CV image to QImage."""
        # self.epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        self.cp_image = cv_img.copy()
        self.cp_image = cv2.cvtColor(self.cp_image, cv2.COLOR_BGR2RGB)
        # img_height, img_width, ch = cv_img.shape
        # self.image_width = int(img_width)
        # self.image_height = int(img_height)
        # self.video_flag = True
        # bytes_per_line = ch * img_width

        # if self.epoch[-2:] == "00":
        # if self.pm_25 is not None and self.g_ext is not None and self.test_name is not None:
        #     self.save_frame(cv_img, self.epoch, self.g_ext, self.pm_25)
        #     self.g_ext = None
        #     self.pm_25 = None
            # return
        
        print("비디오 끝")
        # return
    
    def save_frame(self, image: np.ndarray, epoch: str, g_ext, pm_25):
        """Save the image of the calculation time."""
        print("save_frame 시작")
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
            print(file_name , "The image has been saved.")
            return

    def keyPressEvent(self, e):
        """Override function QMainwindow KeyPressEvent that works when key is pressed"""
        if e.key() == Qt.Key_Escape:
            sys.exit()
        if e.key() == Qt.Key_F:
            self.showFullScreen()
        
    def data_storage(self, vis_data):
        """Store visibility and fine dust values ​​in the database."""

        save_db.SaveDB(vis_data)
        print("data storage!")

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

if __name__ == '__main__':
    mp.freeze_support()
    q = Queue()
    p = Process(name="producer", target=video_thread_mp.producer, args=(q, ), daemon=True)
    p.start()
    
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ND01MainWindow()
    # ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
