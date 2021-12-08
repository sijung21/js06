
#!/usr/bin/env python3

import numpy as np

import cv2
from multiprocessing import Process, Queue
import multiprocessing as mp
import datetime
import time

from PyQt5 import QtWidgets, QtGui, QtCore


def producer(q):
    proc = mp.current_process()
    print(proc.name)

    cap = cv2.VideoCapture("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")
    while True:
        epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        if epoch[-2:] == "00":
            ret, cv_img = cap.read()        
            q.put(cv_img)
        time.sleep(30)       
    cap.release()
        
        
class VideoThread(QtCore.QThread):
    update_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, src: str = "", file_type: str = "None", q: Queue = None):
        super().__init__()
        self._run_flag = False
        self.src = src
        self.file_type = file_type
        self.q = q


    def run(self):
        self._run_flag = True
        ## 영상 입력이 카메라일 때
        if self.file_type == "Video":
            print("비디오 쓰레드 시작") 
            while self._run_flag:
                if not self.q.empty():
                    cv_img = self.q.get()
                    self.update_pixmap_signal.emit(cv_img)
            # shut down capture system

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.quit()
        self.wait()


        
