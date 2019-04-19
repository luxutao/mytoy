#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    模拟按键
"""

import virtkey
import time


v = virtkey.virtkey()
v.press_keysym(65507) #Ctrl键位
v.press_unicode(ord('v')) #模拟字母V
v.release_unicode(ord('v'))
v.release_keysym(65507)
time.sleep(5)
v.press_keysym(65421) #Enter
v.release_keysym(65421)