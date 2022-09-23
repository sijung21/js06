#!/usr/bin/env python3
#
# Copyright 2021-2022 Sijung Co., Ltd.
#
# Authors:
#     cotjdals5450@gmail.com (Seong Min Chae)
#     5jx2oh@gmail.com (Jongjin Oh)

import time
import numpy as np
import random

from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtCharts import (QChartView, QLegend, QLineSeries,
                              QPolarChart, QValueAxis, QChart,
                              QAreaSeries, QCategoryAxis)
from model import JS08Settings


class DiscernmentView(QChartView):

    def __init__(self, parent: QWidget):

        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(600, 400)

        # chart = QPolarChart(title='Discernment Visibility')
        chart = QPolarChart()
        # chart.legend().setAlignment(Qt.AlignRight)
        chart.legend().setVisible(False)
        # chart.legend().setMarkerShape(QLegend.MarkerShapeCircle)
        self.setChart(chart)
        self.chart().setTheme(QChart.ChartThemeDark)
        self.chart().setBackgroundBrush(QBrush(QColor('#16202a')))

        # pen = QPen()
        # pen.setWidth(3)
        # pen.setColor('green')
        # self.series = QLineSeries()
        # self.series.setName('Visibility')
        # self.series.setColor(QColor('green'))
        # self.series.setPen(pen)
        # chart.addSeries(self.series)

        self.axis_x = QValueAxis()
        self.axis_x.setTickCount(9)
        self.axis_x.setRange(0, 360)
        self.axis_x.setLabelFormat('%d \xc2\xb0')
        # self.axis_x.setLabelFormat('%d')
        # axis_x.setTitleText('Azimuth (deg)')
        # axis_x.setTitleVisible(False)
        # chart.setAxisX(self.axis_x, self.series)

        self.axis_distance = QCategoryAxis()
        self.axis_distance.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        self.axis_distance.setRange(0, 360)
        self.axis_distance.setLabelsFont(QFont('Noto Sans', 15))

        data = np.arange(22.5, 360, 45)
        dataName = ['NE', 'EN', 'ES', 'SE', 'SW', 'WS', 'WN', 'NW']
        # self.dataDist = ['']

        for name, dt in zip(dataName, data):
            self.axis_distance.append(f'{name}', dt)
        self.axis_distance.setGridLineVisible(False)
        self.axis_distance.setLineVisible(False)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, 20)
        self.axis_y.setMax(20)
        self.axis_y.setLabelFormat('%d km')
        # axis_y.setTitleText('Distance (km)')
        # axis_y.setTitleVisible(False)
        # chart.setAxisY(self.axis_y, self.series)

        self.lowerLine = QLineSeries()
        self.upperLine = QLineSeries()
        # self.upperLine.attachAxis(self.axis_x)
        # self.upperLine.attachAxis(self.axis_y)

        for i in range(0, 46):
            self.upperLine.append(i, 0)
        for i in range(45, 91):
            self.upperLine.append(i, 0)
        for i in range(90, 136):
            self.upperLine.append(i, 0)
        for i in range(135, 181):
            self.upperLine.append(i, 0)
        for i in range(180, 226):
            self.upperLine.append(i, 0)
        for i in range(226, 271):
            self.upperLine.append(i, 0)
        for i in range(270, 316):
            self.upperLine.append(i, 0)
        for i in range(315, 361):
            self.upperLine.append(i, 0)

        self.area = QAreaSeries()
        self.area.setLowerSeries(self.lowerLine)
        self.area.setUpperSeries(self.upperLine)
        self.area.setOpacity(0.7)

        chart.addSeries(self.area)
        # chart.addAxis(self.axis_x, QPolarChart.PolarOrientationAngular)
        chart.addAxis(self.axis_distance, QPolarChart.PolarOrientationAngular)
        # chart.addAxis(self.axis_y, QPolarChart.PolarOrientationRadial)
        chart.setAxisX(self.axis_x, self.area)
        chart.setAxisY(self.axis_y, self.area)

    def refresh_stats(self, data: dict):

        self.upperLine.clear()

        # self.dataDist = [data.get('NE'), data.get('EN'), data.get('ES'), data.get('SE'),
        #                  data.get('SW'), data.get('WS'), data.get('WN'), data.get('NW')]

        dataName = ['NE', 'EN', 'ES', 'SE', 'SW', 'WS', 'WN', 'NW']

        # for dn, dd, d in zip(dataName, self.dataDist, np.arange(22.5, 360, 45)):
            # self.axis_distance.append(f'{dn} - {dd}', d)

        for i in range(0, 46):
            self.upperLine.append(i, data.get('NE'))
        for i in range(45, 91):
            self.upperLine.append(i, data.get('EN'))
        for i in range(90, 136):
            self.upperLine.append(i, data.get('ES'))
        for i in range(135, 181):
            self.upperLine.append(i, data.get('SE'))
        for i in range(180, 226):
            self.upperLine.append(i, data.get('SW'))
        for i in range(226, 271):
            self.upperLine.append(i, data.get('WS'))
        for i in range(270, 316):
            self.upperLine.append(i, data.get('WN'))
        for i in range(315, 361):
            self.upperLine.append(i, data.get('NW'))

        # self.series.append([
        #     QPointF(360, float(data.get('front_N')))
        # ])
        #
        # self.series.replace([
        #     QPointF(0, float(data.get('front_N'))), QPointF(45, float(data.get('front_NE'))),
        #     QPointF(90, float(data.get('front_E'))), QPointF(135, float(data.get('rear_SE'))),
        #     QPointF(180, float(data.get('rear_S'))), QPointF(225, float(data.get('rear_SW'))),
        #     QPointF(270, float(data.get('rear_W'))), QPointF(315, float(data.get('front_NW'))),
        #     QPointF(360, float(data.get('front_N')))
        # ])

    def mousePressEvent(self, event):

        # JS08Settings.set('maxfev_count', JS08Settings.get('maxfev_count') + 1)
        # self.maxfev_time.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # JS08Settings.set('maxfev_time', self.maxfev_time)
        # print(self.maxfev_time)

        print(f'flag: {JS08Settings.get("maxfev_flag")}, count: {JS08Settings.get("maxfev_count")}')
        # JS08Settings.add_maxfev_time(self.maxfev_time)
        # print()
        # print(f'time: {JS08Settings.get("maxfev_time")}')

        data = {'NE': round(random.uniform(10, 20), 3), 'EN': round(random.uniform(10, 20), 3),
                  'ES': round(random.uniform(10, 20), 3), 'SE': round(random.uniform(10, 20), 3),
                  'SW': round(random.uniform(10, 20), 3), 'WS': round(random.uniform(10, 20), 3),
                  'WN': round(random.uniform(10, 20), 3), 'NW': round(random.uniform(10, 20), 3)}
        # self.refresh_stats(data)

        # self.axis_distance.replaceLabel('NE - 20.0', 'Hi')


if __name__ == '__main__':

    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    visibility = {'visibility_front': 18.829, 'visibility_rear': 5.192,
                  'NE': 20.000, 'EN': 7.208,
                  'ES': 20.000, 'SE': 5.015,
                  'SW': 2.613, 'WS': 20.000,
                  'WN': 20.000, 'NW': 20.000}

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.resize(600, 400)
    discernment_view = DiscernmentView(window)
    discernment_view.refresh_stats(visibility)
    window.setCentralWidget(discernment_view)
    window.show()
    sys.exit(app.exec())
