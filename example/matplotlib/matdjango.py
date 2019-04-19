#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 17-7-2 下午1:15
@__Description__ = " 实现将图片生成的二进制直接插入到django中"
"""

# models.py
from django.db import models


# Create your models here.
class CPUmonitoring(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    # 获取数据的时间
    time = models.DateTimeField(null=False)
    # 获取到的oid的值
    value = models.CharField(max_length=16, null=False)

    def __repr__(self):
        return '<CPU {0}>'.format(self.value)


# graph.py
import matplotlib, os

# 不显示图片直接保存
matplotlib.use('Agg')
import matplotlib.dates as mdate
from matplotlib.backends.backend_agg import FigureCanvas
from webmonit import models
import numpy as np
from django.http import HttpResponse
import matplotlib.pyplot as plt


def makechart():
    d = models.CPUmonitoring.objects.all()
    if len(d) > 11:
        # 创建一个绘图对象，并且使它成为当前的绘图对象
        fig = plt.figure()
        # 添加一个子图，参数为大小
        axex1 = fig.add_subplot(111)
        # 设置字体，让mat支持中文
        myfont = matplotlib.font_manager.FontProperties(
            fname=os.path.dirname(__file__) + '/static/fonts/weiruanyahei.ttf')
        plt.rcParams['axes.unicode_minus'] = False
        split = len(d) - 1
        # 设置子图的x轴时间的显示格式
        axex1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
        # 设置x轴刻度
        plt.xticks(mdate.date2num([n.time for n in d[split - 11: split]]))
        # 设置x轴的起始限制
        plt.xlim(mdate.date2num(d[split - 10: split][0].time), mdate.date2num(d[split - 1].time))
        # 设置x轴中文名称
        plt.xlabel('time',fontproperties=myfont)
        plt.ylim(0, 100)
        plt.ylabel('value',fontproperties=myfont)
        times = [n.time for n in d[split - 10: split]]
        values = [n.value for n in d[split - 10: split]]
        plt.plot_date(times, values, 'b')
        # 返回图像对象，或者直接返回一个response进行调用（不推荐），如果直接返回一个response对象，则无法将图片数据插入到一个网页的某个部分，
        # 所以，返回一个图像的对象，在django中的views视图进行调整，输出到模板的img中
        canvas = FigureCanvas(fig)
        return canvas
        # response = HttpResponse(content_type='image/png')
        # canvas.print_png(response)
        # return response


# views.py
import io, base64
from django.shortcuts import render


def cpu_monitor(request):
    graphic = io.BytesIO()
    line_graph = makechart()
    if line_graph:
        line_graph.print_png(graphic)
        return render(request, 'cpu_monitor.html', {'graphic': base64.encodebytes(graphic.getvalue())})

# cpu_monitor.html
# 设置HTML模板中的图片显示格式为base64
# <img src="data:image/jpeg;base64,{{ graphic }}" />
