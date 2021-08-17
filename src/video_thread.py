#!/usr/bin/env python3

import numpy as np

import cv2

from PyQt5 import QtWidgets, QtGui, QtCore


class VideoThread(QtCore.QThread):
    update_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, src: str = "", file_type: str = "None"):
        super().__init__()
        self._run_flag = False
        self.src = src
        self.file_type = file_type
        self.img_width = 0
        self.img_height = 0

    def run(self):
        self._run_flag = True
        ## 영상 입력이 카메라일 때
        if self.file_type == "Video":
            print("비디오 쓰레드 시작")

            if self.src == "":
                cap = cv2.VideoCapture(0)
            # cap = ""
            else:
                cap = cv2.VideoCapture(self.src)
            

            while self._run_flag:
                ret, cv_img = cap.read()
            #  cv_img = cv2.imread('image_path/v2.png')
                # self.update_pixmap_signal.emit(cv_img)
                if ret:
                    self.update_pixmap_signal.emit(cv_img)
            # shut down capture system
            cap.release()

        elif self.file_type == "Image":
            print("이미지 전송")
            cv_img = cv2.imread(self.src, cv2.IMREAD_COLOR)
            self.update_pixmap_signal.emit(cv_img)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
