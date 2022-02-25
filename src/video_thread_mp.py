
#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np

import cv2
from multiprocessing import Process, Queue
import multiprocessing as mp
import datetime
import time

from PyQt5 import QtWidgets, QtGui, QtCore

import target_info


def producer(q):
    proc = mp.current_process()    
    
    while True:
        epoch = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        
        # 2초에 한번
        # if int(epoch[-2:]) % 2 == 00:
        
        # 1분에 한번
        if epoch[-2:] == "00":
            print(epoch)
            try:
                target_name, left_range, right_range, distance = target_info.get_target("PNM_9030V")
                
                if len(left_range) < 4:
                    continue
                else:
                    pass
                
                cap = cv2.VideoCapture("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")
                ret, cv_img = cap.read()
                
                if ret:
                    visibility = target_info.minprint(epoch[:-2], left_range, right_range, distance, cv_img)
                    visibility = visibility
                    cap.release()
                    
                    q.put(visibility)
                    time.sleep(1)
            except Exception as e:
                print(e)
                cap.release()
                cap = cv2.VideoCapture("rtsp://admin:sijung5520@192.168.100.100/profile2/media.smp")
                continue

class CurveThread(QtCore.QThread):
    update_visibility_signal = QtCore.pyqtSignal(str)

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
            print("Start curve thread")
            while self._run_flag:
                if not self.q.empty():
                    visibility = self.q.get()
                    print("visibility: ", visibility)
                    self.update_visibility_signal.emit(visibility)
            # shut down capture system

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.quit()
        self.wait()


        
