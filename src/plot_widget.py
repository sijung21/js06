from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *

import pyqtgraph as pg

import time


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time(초)', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        """
        override 하여, tick 옆에 써지는 문자를 원하는대로 수정함.
        values --> x축 값들   ; 숫자로 이루어진 Itarable data --> ex) List[int]
        """
        return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]


class PlotWidget(QGraphicsView):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.resize(1200, 100)

        self.pw = pg.PlotWidget(
            labels={'left': 'Visibility'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )

        hbox = QHBoxLayout()
        hbox.addWidget(self.pw)
        self.setLayout(hbox)

        # self.pw.setYRange(0, 30, padding=0)
        self.pw.setYRange(0, 30)

        time_data = int(time.time())
        self.pw.setXRange(time_data - 10, time_data + 1)  # 생략 가능.

        self.pw.showGrid(x=True, y=True)
        # self.pw.enableAutoRange()

        self.pdi = self.pw.plot(pen='y')   # PlotDataItem obj 반환.

        self.plotData = {'x': [], 'y': []}

    def update_plot(self, new_time_data: int):
        data_sec = time.strftime("%S", time.localtime(new_time_data))
        # self.plotData['y'].append(int(data_sec))
        self.plotData['y'].append(10)
        self.plotData['x'].append(new_time_data)

        self.pw.setXRange(new_time_data - 3600 * 3, new_time_data, padding=0)   # 항상 x축 시간을 최근 범위만 보여줌.
        print(new_time_data)

        self.pdi.setData(self.plotData['x'], self.plotData['y'])
