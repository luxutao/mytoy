#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 17-7-2 下午1:12
@__Description__ = "制作动图格式，会根据x轴长度进行推进操作"
"""

import random
import matplotlib.pyplot as plt

plt.xlim(0, 20)
plt.ylim(0, 100)
plt.ion()
i = 0
f = []
q = []
while True:
    temp = random.choice(list(range(100)))
    f.append(temp)
    i += 1
    q.append(i)
    # 重点，每次超过刻度则重新设置刻度，实现动作
    if i > 20:
        plt.xlim(i - 20, i)
    plt.plot(q, f, 'b')
    # 刷新时间
    plt.pause(0.1)
