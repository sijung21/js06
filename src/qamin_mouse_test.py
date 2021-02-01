from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.setWindowTitle('mouse')
        self.resize(320, 240)
        self.show()


    def mousePressEvent(self, event):  #event : QMouseEvent

        if event.buttons() & Qt.LeftButton:
            print('BUTTON PRESS - LEFT')
        if event.buttons() & Qt.MidButton:
            print('BUTTON PRESS - MIDDLE')
        if event.buttons() & Qt.RightButton:
            print('BUTTON PRESS - RIGHT')


    def mouseReleaseEvent(self, event):  # event : QMouseEvent
        print('BUTTON RELEASE')

    def wheelEvent(self, event):  # event QWheelEvent
        print('wheel')
        print('(%d %d)' % (event.angleDelta().x(), event.angleDelta().y()))

    def mouseMoveEvent(self, event):  # event QMouseEvent
        print('(%d %d)' % (event.x(), event.y()))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())