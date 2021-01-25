import sys
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.begin = QPoint()
        self.lastPoint = QPoint()
        self.image = QPixmap("image_path/v2.png")
        self.setGeometry(100, 100, 500, 500)
        self.resize(self.image.width(), self.image.height())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))
        painter.setBrush(br)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawPixmap(self.rect(), self.image)
        painter.drawRect(QRect(self.begin, self.lastPoint))


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.begin = event.pos()
            self.lastPoint = event.pos()
            print(self.begin)

    def mouseMoveEvent(self, event):
        if event.buttons() and self.drawing:
            # painter = QPainter(self.image)
            # painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            # painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
            self.lastPoint = event.pos()
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())