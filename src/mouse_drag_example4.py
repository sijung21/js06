import sys

from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QPoint, QRect, Qt

import cv2


class TestRect(QLabel):
    def __init__(self):
        super().__init__()
        self.begin = QPoint()
        self.end = QPoint()

    def paintEvent(self, event):
        super().paintEvent(event)
        qp = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        # self.begin = event.pos()
        self.end = event.pos()
        self.update()
        print(self.end.x(), self.end.y())

    def get_px(self, pos):
        return pos


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image = None
        win_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        win_rectangle.moveCenter(center_point)
        self.move(win_rectangle.topLeft())
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.test_image()
        self.show()

    def test_image(self):
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        label = TestRect()
        self.main_layout.addWidget(label)
        image = cv2.imread('image_path/v2.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = 700, 700
        image = cv2.resize(image, (height, width))
        self.current_image = QImage(image, height, width, QImage.Format_RGB888)
        label.setPixmap(QPixmap(self.current_image))
        print(label.end)

    def target(self, x):
        print(x)

if __name__ == '__main__':
    test = QApplication(sys.argv)
    test_window = TestWindow()
    sys.exit(test.exec_())
