#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 2017/7/3 09:46
@__Description__ = " 官方实例"
"""

import matplotlib.pyplot as plt
import matplotlib,os

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
pie = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
# 设置饼状图中文显示
# 原文解释链接https://my.oschina.net/Kanonpy/blog/617535?p=1
for font in pie[1]:
        font.set_fontproperties(matplotlib.font_manager.FontProperties(
                fname=os.path.dirname(__file__) + '/static/fonts/weiruanyahei.ttf'))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()