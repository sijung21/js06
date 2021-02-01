
import sys

import cv2

from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QPoint, QRect, Qt

from video_thread import VideoThread
from mainwindow import Ui_MainWindow
from mouse_drag_example4 import TestRect

class Js06MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.camera_name = ""
        self.video_thread = None
        self.ipcam_start()
        self.begin = QPoint()
        self.end = QPoint()
        self.qt_img = QPixmap()

    def setupUi(self, MainWindow: QMainWindow):
        super().setupUi(MainWindow)
        # self.centralwidget.paintEvent = self.paintEvent
        self.image_label.paintEvent = self.paintEvent
        self.image_label.mousePressEvent = self.mousePressEvent
        self.image_label.mouseMoveEvent = self.mouseMoveEvent
        self.image_label.mouseReleaseEvent = self.mouseReleaseEvent

    def ipcam_start(self):
        """Connect to webcam"""
        if self.video_thread is not None:
            self.video_thread.stop()

        self.camera_name = "PNM-9030V"
        # create the video capture thread
        self.video_thread = VideoThread('rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp')
        # self.video_thread = VideoThread()
        # connect its signal to the update_image slot
        self.video_thread.update_pixmap_signal.connect(self.update_image)
        # start the thread
        self.video_thread.start()

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.qt_img = self.convert_cv_qt(cv_img)
        print(type(self.qt_img))
        self.image_label.setPixmap(self.qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width, ch = rgb_image.shape
        # print(self.img_height, self.img_width)
        self.label_width = self.image_label.width()
        self.label_height = self.image_label.height()

        bytes_per_line = ch * self.img_width
        convert_to_Qt_format = QImage(rgb_image.data, self.img_width, self.img_height, bytes_per_line,
                                            QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
        return QPixmap.fromImage(p)

    def paintEvent(self, event):
        qp = QPainter(self.image_label)
        qp.drawPixmap(self.image_label.rect(), self.qt_img)
        br = QBrush(QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        """마우스 프레스 함수 오버라이드"""
        self.begin = event.pos()
        self.end = event.pos()
        print(self.begin)
        self.image_label.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.image_label.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.image_label.update()
        print(self.end.x(), self.end.y())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Js06MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())