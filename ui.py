#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    音乐播放器
"""

import sys
import os

from PyQt5 import QtWidgets, QtCore, QtMultimedia


class ShowFiles(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置一个Widget
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.resize(100, 300)
        # 设置垂直布局
        self.bodyLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.set_head()
        self.set_foot()
        self.bodyLayout.addLayout(self.headLayout)
        self.bodyLayout.addLayout(self.footLayout)
        self.setLayout(self.bodyLayout)

    def set_head(self):
        # 设置水平布局,左侧添加Label,右侧位输入框
        self.headLayout = QtWidgets.QHBoxLayout()
        self.headLabel = QtWidgets.QLabel('音乐目录:')
        self.headInput = QtWidgets.QLineEdit('/home/luxutao/Music/1998.mp3')
        self.headLayout.addWidget(self.headLabel)
        self.headLayout.addWidget(self.headInput)

    def set_foot(self):
        # 设置水平布局
        self.footLayout = QtWidgets.QHBoxLayout()
        self.footLabel = QtWidgets.QLabel('显示文件：')
        # 设置Label位置顶部
        self.footLabel.setAlignment(QtCore.Qt.AlignTop)
        # 创建一个带有滑动条的区域
        self.filesList = QtWidgets.QScrollArea()
        # 创建一个listWidget放置到滑动区域
        self.list = QtWidgets.QListWidget()
        self.filesList.setWidget(self.list)
        # 创建一个按钮
        self.submitLayout = QtWidgets.QPushButton('提交')
        # 设置按钮的点击事件
        self.submitLayout.clicked.connect(self.get_files)
        # 设置布局
        self.footLayout.addWidget(self.footLabel)
        self.footLayout.addWidget(self.filesList)
        self.footLayout.addWidget(self.submitLayout)

    def get_files(self):
        # 获得输入框内输入的值
        text = self.headInput.displayText()
        # 将list区域清空并且将路径的值插入进去,接受的是列表类型
        self.list.clear()
        if os.path.exists(text):
            player = QtMultimedia.QMediaPlayer(self)
            player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(text)))
            player.setVolume(100)
            player.play()
        else:
            # 添加警告框
            QtWidgets.QMessageBox.warning(self, "Warning", "当前输入路径<{path}>不存在!".format(
                path=text), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ShowFiles()
    main.show()
    sys.exit(app.exec_())
