#!/usr/bin/env python3
#
# Copyright 2020-2021 Sijung Co., Ltd.
# Authors: 
#     ruddyscent@gmail.com (Kyungwon Chun)
#     5jx2oh@gmail.com (Jongjin Oh)

import time
import os
import cv2
import numpy as np
from video_thread import VideoThread

from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

# VIDEO_SRC1 = "rtsp://admin:sijung5520@d617.asuscomm.com:2554/profile2/media.smp"
VIDEO_SRC2 = "rtsp://admin:sijung5520@d617.asuscomm.com:1554/profile2/media.smp"
VIDEO_SRC3 = "rtsp://admin:sijung5520@192.168.100.20/profile2/media.smp"
# VIDEO_SRC3 = "rtsp://admin:sijung5520@d617.asuscomm.com:3554/profile2/media.smp"


class Js06VideoWidget2(QWidget):
    def __init__(self, parent=None):
        super(Js06VideoWidget2, self).__init__(parent)

        self.scene = QGraphicsScene(self)
        self.graphicView = QGraphicsView(self.scene)
        self.graphicView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_item = QGraphicsVideoItem()
        self.scene.addItem(self.video_item)

        self._player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self._player.setVideoOutput(self.video_item)
        self._player.setPosition(0)

        layout = QVBoxLayout(self)
        # layout.resize(500, 1920)
        layout.addWidget(self.graphicView)
        self.camera_name = None

        self.filepath = os.path.join(os.getcwd(), "target")
        try:
            os.makedirs(self.filepath, exist_ok=True)
        except OSError:
            pass
        print("비디오 위젯 클래스 시작")
    # end of __init__

    @pyqtSlot(QMediaPlayer.State)
    def on_stateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.view.fitInView(self.video_item, Qt.KeepAspectRatio)
    # end of on_stateChanged

    @pyqtSlot(str)
    def onCameraChange(self, url):
        print("비디오 실행")
        self._player.setMedia(QMediaContent(QUrl(url)))
        self.graphicView.fitInView(self.video_item)
        self._player.play()

        self.video_thread = VideoThread(url)
        self.video_thread.update_pixmap_signal.connect(self.convert_cv_qt)
        self.video_thread.start()
    # end of onCameraChange

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        self.epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        if self.epoch[-2:] == "00":
            self.save_frame(cv_img, self.epoch)
    # end of conver_cv_qt

    def save_frame(self, image: np.ndarray, epoch: str):
        image_path = os.path.join(self.filepath, "image", f"{self.camera_name}", f"{epoch[2:6]}")
        file_name = f"{epoch}"
        if not os.path.isdir(image_path):
            os.makedirs(image_path)
        if not os.path.isfile(f"{image_path}/{file_name}.jpg"):
            cv2.imwrite(f"{image_path}/{file_name}.jpg", image)
        del image
        del image_path
        cv2.destroyAllWindows()
    # end of save_frame

# end of VideoWidget2


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QMenuBar, QAction, qApp

    app = QApplication(sys.argv)

    def exit():
        sys.exit()

    window = Js06VideoWidget2()
    menubar = QMenuBar(window)
    exitMenu = menubar.addMenu("File")
    exitAction = QAction("Exit", window)
    exitAction.setShortcut("Ctrl+W")
    actionCamera_2 = QAction("PNM-9030V", window)
    actionCamera_3 = QAction("XNO-8080R", window)
    exitAction.triggered.connect(exit)
    exitMenu.addAction(actionCamera_2)
    exitMenu.addAction(actionCamera_3)
    exitMenu.addAction(exitAction)

    actionCamera_2.triggered.connect(lambda: window.onCameraChange(VIDEO_SRC2))
    actionCamera_3.triggered.connect(lambda: window.onCameraChange(VIDEO_SRC3))
    actionCamera_3.triggered.emit()

    window.resize(600, 600)
    window.show()
    sys.exit(app.exec_())