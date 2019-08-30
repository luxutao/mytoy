#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import os
import subprocess

import requests
from PyQt5 import QtWidgets, QtCore


class BackWorkSpace(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置一个Widget
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.resize(100, 300)
        # 设置垂直布局
        self.bodyLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.set_foot()
        self.bodyLayout.addLayout(self.footLayout)
        self.setLayout(self.bodyLayout)

    def set_foot(self):
        # 设置水平布局
        self.footLayout = QtWidgets.QHBoxLayout()
        # 创建一个按钮
        self.backLayout = QtWidgets.QPushButton('返回')
        self.exitLayout = QtWidgets.QPushButton('退出')
        # 设置按钮的点击事件
        self.backLayout.clicked.connect(self.send)
        self.exitLayout.clicked.connect(self.exit)
        # 设置布局
        self.footLayout.addWidget(self.backLayout)
        self.footLayout.addWidget(self.exitLayout)

    def back(self):
        subprocess.Popen("qdbus org.kde.KWin /KWin setCurrentDesktop 1", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    def exit(self):
        sys.exit()

    def send(message):
        data = requests.get("http://192.168.2.12:9999/changeWorkSpace").json()
        print(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = BackWorkSpace()
    main.show()
    sys.exit(app.exec_())

