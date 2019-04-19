#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    计划定时任务 针对selinium不能执行在Linux后台问题
"""


import datetime
import subprocess
import time

CRONpath = '/usr/bin/python3'
CRONlist = {'03:33': '/storage/Projects/slmulate/bilibili.py',
            '04:44': '/storage/Projects/slmulate/51cto.py',
            '03:55': '/storage/Projects/slmulate/jd.py'}

while True:
    NOWdate = datetime.datetime.now().strftime('%H:%M')
    if NOWdate in CRONlist.keys():
        subprocess.call("/usr/bin/python3 {0}".format(CRONlist[NOWdate]), shell=True)
    time.sleep(60)
