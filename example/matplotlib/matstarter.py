#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 17-7-2 下午1:10
@__Description__ = "简易版制作折线图"
"""

import matplotlib.pyplot as plt
import numpy as np

d = [1, 2, 3, 4, 5]
q = [5, 6, 7, 8, 9]
# 简单理解，大框套小框
fig = plt.figure()
axex1 = fig.add_subplot(111)
# xy轴的开始与结束刻度及名称
plt.xlim(0, 10)
plt.xlabel('time')
plt.ylim(0, 10)
plt.ylabel('value')
# 显示图片，第三个参数为显示的颜色等设置，具体请查看文档。比如'b'\'g^'
plt.plot(np.array(d), np.array(q))
plt.show()
