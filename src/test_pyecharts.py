# # coding=utf-8
# # from __future__ import unicode_literals
# from pyecharts import Bar, Pie, Gauge
#
# attr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
# v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
# bar = Bar("Bar Graph", "precipitation and evaporation one year")
# bar.add("precipitation", attr, v1, mark_line=["average"], mark_point=["max", "min"])
# bar.add("evaporation", attr, v2, mark_line=["average"], mark_point=["max", "min"])
# bar.height = 500
# bar.width = 800
# bar.render()
#
# gauge = Gauge("Gauge Graph")
# gauge.add("이용률", "가운데", 66.66)
#
# attr = ['A', 'B', 'C', 'D', 'E', 'F']
# v1 = [11, 12, 13, 10, 10, 10]
# v2 = [19, 21, 32, 20, 20, 33]
# pie = Pie('Pie Graph', title_pos='center', width=900)
# pie.add('A', attr, v1, center=[25,50], is_random=True, radius=[30, 75], rosetype='radius')
# pie.add('B', attr, v2, center=[75,50], is_random=True, radius=[30, 75], rosetype='area', is_legend_show=False,
#         is_label_show=True)
# pie.render()

# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# import sys
#
#
# class UI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.mainLayout()
#
#     def initUI(self):
#         self.setWindowTitle("TEST")
#
#     def mainLayout(self):
#         self.mainhboxLayout = QHBoxLayout(self)
#         self.frame = QFrame(self)
#         self.mainhboxLayout.addWidget(self.frame)
#         self.hboxLayout = QHBoxLayout(self.frame)
#
#         self.myHtml = QWebEngineView()
#         # url = "http://www.baidu.com"
#         self.myHtml.load(QUrl("render.html"))
#
#         self.hboxLayout.addWidget(self.myHtml)
#         self.setLayout(self.mainhboxLayout)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = UI()
#     ex.show()
#     sys.exit(app.exec_())

import plotly.express as px
df = px.data.wind()
fig = px.line_polar(df, r='frequency', theta='direction', color='strength', line_close=True,
                    color_discrete_sequence=px.colors.sequential.Plasma_r,
                    template='plotly_dark', )
fig.show()
# self.m_output.setHtml(fig.to_html(include_plotlyjs='cdn'))