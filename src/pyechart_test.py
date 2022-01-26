from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import sys
import os

app = QApplication(sys.argv)

browser = QtWebEngineWidgets.QWebEngineView()
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "render.html"))
local_url = QUrl.fromLocalFile(file_path)
browser.load(local_url)

browser.show()

app.exec_()