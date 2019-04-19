#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import re

if (len(sys.argv) != 4):
    print('参数错误')
    sys.exit(1)

name = sys.argv[1]
season = sys.argv[2]
dirpath = sys.argv[3]

files = os.listdir(dirpath)
for i in files:
    print(i)
    # s = input('请输入第几集：')
    s = re.findall(r'.+?第(.+?)话.+?', i)[0]
    os.rename(dirpath + '/' + i, dirpath + '/%s.S%02d.E%02d.mp4' % (name, int(season), int(s)))
