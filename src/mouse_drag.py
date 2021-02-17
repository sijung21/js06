
import sys
import os

import cv2
import numpy as np
import pandas as pd

from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog
from PyQt5.QtCore import QPoint, QRect, Qt, QRectF

from video_thread import VideoThread
from curved import CurvedThread
from mainwindow import Ui_MainWindow

class Js06MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
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

        self.capture_start()

    def setupUi(self, MainWindow: QMainWindow):
        super().setupUi(MainWindow)
        self.image_label.paintEvent = self.paintEvent
        self.image_label.mousePressEvent = self.mousePressEvent
        self.image_label.mouseMoveEvent = self.mouseMoveEvent
        self.image_label.mouseReleaseEvent = self.mouseReleaseEvent

        self.actionstart.triggered.connect(self.capture_start)
        self.actionprint.triggered.connect(self.minprint)

    def ipcam_start(self):
        """Connect to webcam"""
        if self.video_thread is not None:
            self.video_thread.stop()
        #test
        # self.video_thread = VideoThread('rtsp://admin:sijung5520@192.168.100.253/profile2/media.smp')
        self.camera_name = "PNM-9030V"
        # create the video capture thread
        self.video_thread = VideoThread('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
        # webcam version
        # self.video_thread = VideoThread()
        # connect its signal to the update_image slot
        self.video_thread.update_pixmap_signal.connect(self.update_image)
        # start the thread
        self.video_thread.start()

    def capture_start(self):
        if self.video_thread is not None:
            self.video_thread.stop()

        self.bgrfilter = True
        self.camera_name = "PNM-9030V"
        self.get_target(self.camera_name)
        # create the video capture thread
        self.video_thread = VideoThread('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
        self.video_thread.update_pixmap_signal.connect(self.update_image)
        # start the thread
        self.video_thread.start()

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(self.qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        if self.bgrfilter:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            self.cp_image = rgb_image.copy()
        else:
            rgb_image = self.cp_image.copy()

        self.img_height, self.img_width, ch = rgb_image.shape
        self.label_width = self.image_label.width()
        self.label_height = self.image_label.height()
        bytes_per_line = ch * self.img_width

        rec_color = (139, 0, 255)
        tar_color = (0, 255, 0)

        for corner1, corner2 in zip(self.left_range, self.right_range):
            cv2.rectangle(rgb_image, corner1, corner2, rec_color, 6)
        if len(self.min_xy) > 0:
            cv2.rectangle(rgb_image, (self.min_xy[0]-10, self.min_xy[1]-10), (self.min_xy[0]+10, self.min_xy[1]+10), tar_color, 4)

        self.last_image = rgb_image.copy()

        convert_to_Qt_format = QImage(rgb_image.data, self.img_width, self.img_height, bytes_per_line,
                                            QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
        self.bgrfilter = False

        return QPixmap.fromImage(p)

    def paintEvent(self, event):
        """레이블 위에 그림을 그리는 함수, QLabel method overriding"""
        qp = QPainter(self.image_label)
        qp.drawPixmap(self.image_label.rect(), self.qt_img)

        if self.isDrawing:
            br = QBrush(QColor(100, 10, 10, 40))
            qp.setBrush(br)
            qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            qp.drawRect(QRect(self.begin, self.end))
            # test = QPixmap.fromImage(self.cp_image)
            th_x, th_y = self.tumbnailed_pos(self.end)
            test = self.tumbnailed(self.cp_image[th_y - 50 :th_y + 50, th_x - 50 :th_x + 50, :])
            qp.drawPixmap(QRectF(0, 0, 70, 40), test, QRectF(0, 0, 70, 40))

    def tumbnailed_pos(self, end_pos):
        x = int((end_pos.x()/self.label_width)*self.img_width)
        y = int((end_pos.y()/self.label_height)*self.img_height)
        print(x, y)
        return x, y

    def tumbnailed(self, image):
        print(image.shape)
        height, width, channel = image.shape
        bytesPerLine = channel * width
        qImg = QImage(image.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg

    def mousePressEvent(self, event):
        """마우스 클릭시 발생하는 이벤트, QLabel method overriding"""
        if event.buttons() == Qt.LeftButton:
            self.isDrawing = True
            self.begin = event.pos()
            self.end = event.pos()
            self.upper_left = (int((self.begin.x()/self.label_width)*self.img_width),
                               int((self.begin.y()/self.label_height)*self.img_height))
            self.image_label.update()

            self.leftflag = True
            self.rightflag = False

        elif event.buttons() == Qt.RightButton:
            self.isDrawing = False
            if len(self.left_range) > 0:
                del self.distance[-1]
                del self.target_name[-1]
                del self.left_range[-1]
                del self.right_range[-1]
                self.rightflag = True
            self.leftflag = False

    def mouseMoveEvent(self, event):
        """마우스가 움직일 때 발생하는 이벤트, QLabel method overriding"""
        if event.buttons() == Qt.LeftButton:
            self.end = event.pos()
            self.image_label.update()
            self.isDrawing = True

    def mouseReleaseEvent(self, event):
        """마우스 클릭이 떼질 때 발생하는 이벤트, QLabel method overriding"""
        if self.leftflag == True:
            self.end = event.pos()
            self.image_label.update()
            self.lower_right = (int((self.end.x()/self.label_width)*self.img_width),
                                int((self.end.y()/self.label_height)*self.img_height))
            self.left_range.append(self.upper_left)
            self.right_range.append(self.lower_right)
            text, ok = QInputDialog.getText(self.centralwidget, '거리 입력', '거리(km)')
            if ok:
                self.distance.append(text)
                self.min_xy = self.minrgb(self.upper_left, self.lower_right)
                self.target_name.append("target_" + str(len(self.left_range)))
                self.save_target()
                self.update_image(self.last_image)

        if self.rightflag:
            self.update_image(self.last_image)

        self.isDrawing = False

    ## Key 입력이 안되네 메서드 오버라이딩도 안된다.. 왜이럴까???
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            print("sdsds")
            self.back_capture()

    def back_capture(self):
        """소산계수를 구한 시점의 영상을 캡쳐해 레이블에 출력하는 함수"""

        img_height, img_width, ch = self.cp_image.shape
        bytes_per_line = ch * img_width

        convert_to_Qt_format = QImage(self.cp_image.data, img_width, img_height, bytes_per_line,
                                    QImage.Format_RGB888)

        p = convert_to_Qt_format.scaled(self.capture_label.width(), self.capture_label.height(), Qt.IgnoreAspectRatio,
                                        Qt.SmoothTransformation)
        self.capture_label.setPixmap(QPixmap.fromImage(p))
        print("전체 캡쳐")

    def minprint(self):
        """지정한 구역들에서 소산계수 산출용 픽셀을 출력하는 함수"""

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

        self.get_rgb()

        self.curved_thread = CurvedThread(self.camera_name)
        self.curved_thread.update_alpha_signal.connect(self.what)
        self.curved_thread.run()

        graph_image = cv2.imread("test.png")

        img_height, img_width, ch = graph_image.shape
        bytes_per_line = ch * img_width

        convert_to_Qt_format = QImage(graph_image.data, img_width, img_height, bytes_per_line,
                                    QImage.Format_RGB888)

        p = convert_to_Qt_format.scaled(self.graph_label.width(), self.graph_label.height(), Qt.IgnoreAspectRatio,
                                        Qt.SmoothTransformation)
        self.graph_label.setPixmap(QPixmap.fromImage(p))

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

    def get_rgb(self):
        r_list = []
        g_list = []
        b_list = []

        for x, y in zip(self.min_x, self.min_y):

            r_list.append(self.cp_image[y, x, 0])
            g_list.append(self.cp_image[y, x, 1])
            b_list.append(self.cp_image[y, x, 2])

        self.save_rgb(r_list, g_list, b_list)

    def save_rgb(self, r_list, g_list, b_list):
        """Save the rgb information for each target."""
        if r_list:
            col = ["target_name", "r", "g", "b", "distance"]
            result = pd.DataFrame(columns=col)
            result["target_name"] = self.target_name
            result["r"] = r_list
            result["g"] = g_list
            result["b"] = b_list
            result["distance"] = self.distance
            result.to_csv(f"{self.camera_name}_rgb.csv", mode="w", index=False)

    def what(self, alpha1: float = 0.0, alpha2: float = 0.0):
        print(alpha1, alpha2)

    def save_target(self):
        """Save the target information for each camera."""
        if self.left_range:
            col = ["target_name", "left_range", "right_range", "distance"]
            result = pd.DataFrame(columns=col)
            result["target_name"] = self.target_name
            result["left_range"] = self.left_range
            result["right_range"] = self.right_range
            result["distance"] = self.distance
            result.to_csv(f"{self.camera_name}.csv", mode="w", index=False)

    def get_target(self, camera_name: str):
        """특정 카메라의 타겟 정보들을 불러온다."""
        if os.path.isfile(f"{camera_name}.csv"):
            target_df = pd.read_csv(f"{camera_name}.csv")
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
    ui = Js06MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())