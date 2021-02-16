
import sys

import cv2
import numpy as np
import pandas as pd

from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QInputDialog
from PyQt5.QtCore import QPoint, QRect, Qt

from video_thread import VideoThread
from mainwindow import Ui_MainWindow

class Js06MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.camera_name = ""
        self.video_thread = None
        self.ipcam_start()
        self.begin = QPoint()
        self.end = QPoint()
        self.qt_img = QPixmap()
        self.isDrawing = True

        self.upper_left = ()
        self.lower_right = ()
        self.left_range = []
        self.right_range = []
        self.distance = []
        self.target_name = []
        self.min_x = 0
        self.min_y = 0
        self.min_xy = ()
        self.leftflag = False

    def setupUi(self, MainWindow: QMainWindow):
        super().setupUi(MainWindow)
        self.image_label.paintEvent = self.paintEvent
        self.image_label.mousePressEvent = self.mousePressEvent
        self.image_label.mouseMoveEvent = self.mouseMoveEvent
        self.image_label.mouseReleaseEvent = self.mouseReleaseEvent

        self.actionstart.triggered.connect(self.back_capture)
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

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(self.qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        self.cp_image = rgb_image.copy()
        self.img_height, self.img_width, ch = rgb_image.shape
        self.label_width = self.image_label.width()
        self.label_height = self.image_label.height()
        bytes_per_line = ch * self.img_width

        rec_color = (139, 0, 255)
        tar_color = (0, 255, 0)

        if len(self.min_xy) > 0:
            for corner1, corner2 in zip(self.left_range, self.right_range):
                cv2.rectangle(rgb_image, corner1, corner2, rec_color, 6)

            cv2.rectangle(rgb_image, (self.min_xy[0]-10, self.min_xy[1]-10), (self.min_xy[0]+10, self.min_xy[1]+10), tar_color, 4)

        convert_to_Qt_format = QImage(rgb_image.data, self.img_width, self.img_height, bytes_per_line,
                                            QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
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

        elif event.buttons() == Qt.RightButton:
            self.isDrawing = False
            if len(self.left_range) > 0:
                del self.distance[-1]
                del self.target_name[-1]
                del self.left_range[-1]
                del self.right_range[-1]
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

        for upper_left, lower_right in zip(self.left_range, self.right_range):
            result = self.minrgb(upper_left, lower_right)
            print(f"target{cnt}의 소산계수 검출용 픽셀위치 =  ", result)
            cnt += 1

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

        min_y = t_idx[0][0] + up_y
        min_x = t_idx[1][0] + left_x

        return (min_x, min_y)

    def save_target(self):
        """Save the target information for each camera."""
        if self.left_range:
            col = ["target_name", "left_range", "right_range", "distance"]
            result = pd.DataFrame(columns=col)
            result["target_name"] = self.target_name
            result["left_range"] = self.left_range
            result["right_range"] = self.right_range
            result["distance"] = self.distance
            result.to_csv("target_df.csv", mode="w", index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Js06MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
