#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)


import os

import cv2
import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import (QPoint, QRect, Qt,
                          QPointF)
from PyQt5.QtGui import (QPixmap, QPainter, QBrush,
                         QColor, QPen, QImage,
                         QIcon)
from PyQt5.QtWidgets import (QApplication, QLabel, QInputDialog,
                             QDialog, QAbstractItemView, QVBoxLayout,
                             QGridLayout, QPushButton, QMessageBox,
                             QFileDialog, QWidget)
from PyQt5.QtChart import (QChartView, QLegend, QLineSeries,
                           QPolarChart, QScatterSeries, QValueAxis,
                           QChart)
from model import JS06Settings


class EfficiencyChart(QChartView):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setMaximumSize(600, 400)

        series = QLineSeries()

        load = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
        eff = [0, 0.5726, 0.7321, 0.7978, 0.8398, 0.8616, 0.8798,
               0.8903, 0.9002, 0.9062, 0.9127, 0.9267, 0.9379, 0.9430, 0.9448]

        for i, e in zip(load, eff):
            series.append(QPointF(float(i), float(e) * 100))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Efficiency vs. Load')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(0, 30)
        axisX.setLabelFormat("%.1f")
        axisX.setTickCount(7)

        axisY = QValueAxis()
        axisY.setRange(0, 100)
        axisY.setLabelFormat("%d")
        axisY.setMinorTickCount(5)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        series.attachAxis(axisX)
        series.attachAxis(axisY)

        chart.legend().setVisible(False)