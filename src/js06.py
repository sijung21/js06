Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@chaezz 
SteveChae17
/
js06-rpi
Private
2
22
Code
Issues
67
Pull requests
5
Actions
Projects
5
Security
Insights
js06-rpi/src/js06.py /
@Oh-JongJin
Oh-JongJin Add random value in Polar plot
Latest commit e6752db 21 hours ago
 History
 3 contributors
@Oh-JongJin@chaezz@ruddyscent
372 lines (317 sloc)  14.8 KB
  
# !/usr/bin/env python3
#
# Copyright 2020-21 Sijung Co., Ltd.
# Authors:
#     ruddyscent@gmail.com (Kyungwon Chun)
#     5jx2oh@gmail.com (Jongjin Oh)

import os
import pandas as pd

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QActionGroup, QMessageBox, QInputDialog, QLabel, QTabBar
from PyQt5 import uic

# js06 modules
import resources

from video_widget_2 import Js06VideoWidget2
from target_plot_widget_2 import Js06TargetPlotWidget
from time_series_plot_widget import Js06TimeSeriesPlotWidget
from video_thread import VideoThread
from tflite_thread import TfliteThread
from settings import Js06Settings
from save_db import SaveDB


class Js06MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "designer/js06_form.ui")
        uic.loadUi(ui_path, self)

        app_icon = QIcon(":icon/logo.png")
        self.setWindowIcon(app_icon)
        self.setGeometry(400, 50, 1500, 1000)
        # self.showFullScreen()
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)

        # Initialize variable
        self.horizontal_y1 = None
        self.horizontal_y2 = None
        self.horizontal_y3 = None
        self.horizontal_flag = False
        self.tflite_thread = None
        self.target = None
        self.target_x = None
        self.target_y = None
        self.prime_x = None
        self.prime_y = None
        self.distance = None
        self.oxlist = None
        self.target_process = False

        self.filepath = os.path.join(os.getcwd(), "target")
        try:
            os.makedirs(self.filepath, exist_ok=True)
        except OSError:
            pass

        # Check the last shutdown status
        shutdown_status = Js06Settings.get('normal_shutdown')
        if not shutdown_status:
            response = QMessageBox.question(
                self,
                'JS-06 Restore to defaults',
                'The last exit status of JS-06 was recorded as abnormal. '
                'Do you want to restore to the factory default?',
            )
            if response == QMessageBox.Yes:
                Js06Settings.restore_defaults()
        Js06Settings.set('normal_shutdown', False)

        # video dock
        self.video_dock = QDockWidget("Video", self)
        self.video_dock.setFeatures(
            QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable)
        self.video_widget = Js06VideoWidget2(self)
        self.video_dock.setWidget(self.video_widget)
        self.setCentralWidget(self.video_dock)

        # To drawing target box in blank label
        self.blank_lbl = QLabel(self.video_widget)
        self.blank_lbl.mousePressEvent = self.lbl_mousePressEvent
        self.blank_lbl.mouseMoveEvent = self.lbl_mouseMoveEvent
        self.blank_lbl.paintEvent = self.lbl_paintEvent

        VIDEO_SRC1 = "rtsp://admin:sijung5520@d617.asuscomm.com:2554/profile2/media.smp"
        VIDEO_SRC2 = "rtsp://admin:sijung5520@d617.asuscomm.com:1554/profile2/media.smp"
        VIDEO_SRC3 = "rtsp://admin:sijung5520@d617.asuscomm.com:3554/profile2/media.smp"

        self.actionCamera_1.triggered.connect(lambda: self.video_widget.onCameraChange(VIDEO_SRC1))
        self.actionCamera_1.triggered.connect(lambda: Js06Settings.set('camera', 1))
        self.actionCamera_2.triggered.connect(lambda: self.video_widget.onCameraChange(VIDEO_SRC2))
        self.actionCamera_2.triggered.connect(lambda: Js06Settings.set('camera', 2))
        self.actionCamera_3.triggered.connect(lambda: self.video_widget.onCameraChange(VIDEO_SRC3))
        self.actionCamera_3.triggered.connect(lambda: Js06Settings.set('camera', 3))

        self.actionEdit_target.triggered.connect(self.target_mode)
        self.actionOpen_with_RTSP.triggered.connect(self.open_with_rtsp)
        self.actionHorizontal.triggered.connect(self.replace_horizontal)

        action_group = QActionGroup(self)
        action_group.addAction(self.actionCamera_1)
        action_group.addAction(self.actionCamera_2)
        action_group.addAction(self.actionCamera_3)

        camera_choice = Js06Settings.get('camera')
        if camera_choice == 1:
            self.video_widget.camera_name = "QND-8020R"
            self.camera_name = "QND-8020R"
            self.actionCamera_1.triggered.emit()
            self.actionCamera_1.setChecked(True)
        elif camera_choice == 2:
            self.video_widget.camera_name = "PNM-9030V"
            self.camera_name = "PNM-9030V"
            self.actionCamera_2.triggered.emit()
            self.actionCamera_2.setChecked(True)
        elif camera_choice == 3:
            self.video_widget.camera_name = "XNO-8080R"
            self.camera_name = "XNO-8080R"
            self.actionCamera_3.triggered.emit()
            self.actionCamera_3.setChecked(True)

        # target plot dock
        self.target_plot_dock = QDockWidget("Target plot", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.target_plot_dock)
        self.target_plot_dock.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.target_plot_widget = Js06TargetPlotWidget(self)
        self.target_plot_dock.setWidget(self.target_plot_widget)

        # grafana dock 1
        self.web_dock_1 = QDockWidget("Grafana plot 1", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.target_plot_dock)
        self.web_dock_1.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.web_view_1 = Js06TimeSeriesPlotWidget()
        self.web_dock_1.setWidget(self.web_view_1)

        self.tabifyDockWidget(self.target_plot_dock, self.web_dock_1)
        tabbar = self.findChild(QTabBar, "")
        tabbar.tabBarClicked.connect(self.current_dock)

        self.qtimer = QTimer()
        self.qtimer.setInterval(2000)
        self.qtimer.timeout.connect(self.inference)
        self.qtimer.start()
    # end of __init__

    def closeEvent(self, event):
        Js06Settings.set('normal_shutdown', True)
        event.accept()
    # end of closeEvent

    def current_dock(self, index):
        tabbar = self.sender()
        print(f"You clicked {tabbar.tabText(index)}.")

    def inference(self):
        self.video_widget.graphicView.fitInView(self.video_widget.video_item)
        self.blank_lbl.setGeometry(self.video_widget.graphicView.geometry())

        if self.horizontal_y1 is None:
            self.horizontal_y1 = self.blank_lbl.height() * (1 / 4)
            self.horizontal_y2 = self.blank_lbl.height() * (1 / 2)
            self.horizontal_y3 = self.blank_lbl.height() * (3 / 4)

        if self.actionInference.isChecked():
            self.actionEdit_target.setChecked(False)
            if self.tflite_thread is None:
                if not self.prime_x:
                    print("There is nothing to Inference.")
                    return
                print("Start Inference.")

                # self.tflite_thread = TfliteThread(self.crop_imagelist100)
                # self.tflite_thread.run_flag = True
                # self.tflite_thread.update_oxlist_signal.connect(self.get_visibility)
                # self.tflite_thread.start()
        else:
            if self.tflite_thread is None:
                return
            if self.tflite_thread.run_flag:
                print("Stop Inference.")
    # end of inference

    def target_mode(self):
        """Set target image modification mode"""
        self.save_target()
        if self.target_process:
            self.target_process = False
            self.save_target()
        else:
            self.target_process = True
            self.actionInference.setChecked(False)
            if self.tflite_thread is not None:
                self.tflite_thread.stop()
                self.tflite_thread = False
            print("Target edit mode.")
            self.save_target()
    # end of target_mode


    def get_target(self):
        if os.path.isfile(f"target/{self.camera_name}.csv"):
            print(self.camera_name)
            result = pd.read_csv(f"target/{self.camera_name}.csv")
            self.target = result.target.tolist()
            self.prime_x = result.x.tolist()
            self.prime_y = result.y.tolist()
            self.label_x = result.label_x.tolist()
            self.label_y = result.label_y.tolist()
            self.distance = result.distance.tolist()
            self.oxlist = [0 for i in range(len(self.prime_x))]
            print("Load csv file.")

        elif os.path.isfile(f"target/{self.camera_name}.csv") is False:
            print("No csv file.")
        else:
            print("Unable to load csv file.")
    # end of get_target

    def save_target(self):
        if self.prime_x:
            col = ["target", "x", "y", "label_x", "label_y", "distance", "discernment"]
            self.result = pd.DataFrame(columns=col)
            self.result["target"] = self.target
            self.result["x"] = self.prime_x
            self.result["y"] = self.prime_y
            self.result["label_x"] = [round(x * self.video_widget.graphicView.geometry().width() /
                                            self.video_widget.video_item.nativeSize().width(), 3) for x in self.target_x]
            self.result["label_y"] = [round(y * self.video_widget.graphicView.geometry().height() /
                                            self.video_widget.video_item.nativeSize().height(), 3) for y in self.target_y]
            self.result["distance"] = self.distance
            self.result["discernment"] = self.oxlist
            self.result.to_csv(f"{self.filepath}/{self.camera_name}.csv", mode="w", index=False)
    # end of save_target

    def coordinator(self):
        self.prime_x = [y / self.video_widget.video_item.nativeSize().height() for y in self.target_y]
        self.prime_x = [2 * x / self.video_widget.video_item.nativeSize.width() - 1 for x in self.target_x]
    # end of coordinator

    def restoration(self):
        self.target_x = [self.f2i((x + 1) * self.video_widget.video_item.nativeSize().width() / 2) for x in self.prime_x]
        self.target_y = [self.f2i(y * self.video_widget.video_item.nativeSize().height()) for y in self.prime_y]
    # end of restoration

    @staticmethod
    def f2i(num: float):
        return int(num + 0.5)
    # end of f2i

    def lbl_mousePressEvent(self, event):
        y = int(event.pos().y() / self.video_widget.graphicView.geometry().height() *
                self.video_widget.video_item.nativeSize().height())
        x = int(event.pos().x() / self.video_widget.graphicView.geometry().width() *
                self.video_widget.video_item.nativeSize().width())
        if self.actionEdit_target.isChecked():
            print(x, y)

        if self.target:
            for i in range(len(self.target)):
                self.target[i] = i + 1

        if not self.target_process:
            return

        if event.buttons() == Qt.LeftButton:
            text, ok = QInputDialog.getText(self.centralWidget(), "Add Target", "Distance (km)")
            if ok:
                self.target_x.append(x)
                self.target_y.append(y)
                self.distance.append(float(text))
                self.target.append(str(len(self.target_x)))
                self.oxlist.append(0)
                print(f"Target position: {self.target_x[-1]}, {self.target_y[-1]}")
                self.coordinator()
                self.save_target()
                self.get_target()

        if event.buttons() == Qt.RightButton:
            text, ok = QInputDialog.getText(self.centralWidget(), "Remove Target", "Enter target number to remove")
            text = int(text)
            if ok:
                if len(self.prime_x) >= 1:
                    del self.target[text - 1]
                    del self.prime_x[text - 1]
                    del self.prime_y[text - 1]
                    del self.label_x[text - 1]
                    del self.label_y[text - 1]
                    del self.distance[text - 1]
                    del self.oxlist[text - 1]
                    print(f"[Target {text}] remove.")
                    self.save_target()

                else:
                    print("There are no targets to remove.")
    # end of lbl_mousePressEvent

    def lbl_mouseMoveEvent(self, event):
        if Qt.LeftButton and self.horizontal_flag:
            if self.horizontal_y1 - 5 < event.pos().y() < self.horizontal_y1 + 5:
                self.horizontal_y1 = event.pos().y()
                self.setCursor(QCursor(Qt.ClosedHandCursor))

            if self.horizontal_y2 - 5 < event.pos().y() < self.horizontal_y2 + 5:
                self.horizontal_y2 = event.pos().y()
                self.setCursor(QCursor(Qt.ClosedHandCursor))

            if self.horizontal_y3 - 5 < event.pos().y() < self.horizontal_y3 + 5:
                self.horizontal_y3 = event.pos().y()
                self.setCursor(QCursor(Qt.ClosedHandCursor))
    # end of lbl_mouseMoveEvent

    def lbl_mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
    # end of lbl_mouseReleaseEvent

    def lbl_paintEvent(self, event):
        painter = QPainter(self.blank_lbl)
        if self.horizontal_flag:
            painter.setPen(QPen(Qt.black, 2, Qt.DotLine))
            x1 = painter.drawLine(self.blank_lbl.width() * (1 / 4), 0,
                                  self.blank_lbl.width() * (1 / 4), self.blank_lbl.height())
            x2 = painter.drawLine(self.blank_lbl.width() * (1 / 2), 0,
                                  self.blank_lbl.width() * (1 / 2), self.blank_lbl.height())
            x3 = painter.drawLine(self.blank_lbl.width() * (3 / 4), 0,
                                  self.blank_lbl.width() * (3 / 4), self.blank_lbl.height())

            y1 = painter.drawLine(0, self.horizontal_y1, self.blank_lbl.width(), self.horizontal_y1)
            y2 = painter.drawLine(0, self.horizontal_y2, self.blank_lbl.width(), self.horizontal_y2)
            y3 = painter.drawLine(0, self.horizontal_y3, self.blank_lbl.width(), self.horizontal_y3)
        else:
            x1 = None
            x2 = None
            x3 = None
            y1 = None
            y2 = None
            y3 = None
        painter.end()
    # end of lbl_paintEvent

    def replace_horizontal(self):
        if self.actionHorizontal.isChecked():
            self.horizontal_flag = True
        else:
            self.horizontal_flag = False
    # end of replace_horizontal

    def open_with_rtsp(self):
        text, ok = QInputDialog.getText(self, "Input RTSP", "Only Hanwha Camera")
        if ok:
            print(text)
    # end of open_with_rtsp

# end of Js06MainWindow


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = Js06MainWindow()
    window.show()
    sys.exit(app.exec_())
# end of js06.py
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Loading complete{"mode":"full","isActive":false}