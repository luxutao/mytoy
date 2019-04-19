#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    
"""

import os, re
import xlrd
import xlwt
import time

row = 0
path = '/home/luxutao/Desktop/未命名文件夹/'


# 读取excel表，存入到temp.txt中，格式为列表形式
def WriteTemp(file):
    data = xlrd.open_workbook(file).sheet_by_index(0)
    num = data.nrows
    for n in range(num):
        dd = [data.row(n)[i].value for i in range(data.ncols)]
        if isinstance(dd[0], float):
            ltime = xlrd.xldate_as_tuple(dd[0], data)
            dd[0] = time.strftime("%Y/%m/%d", ltime)
        with open(path + 'temp.txt', 'a') as ff:
            print(dd, file=ff)
    return num


# 写入数据
def WriteXlsx(rowsl):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    with open(path + 'temp.txt') as qq:
        for col, line in zip(qq, range(rowsl)):
            search = re.findall(r"\[(.+?)\]", col)
            listdata = search[0].split(',')
            replist = [m.strip().replace('\'', '') for m in listdata]
            for n in range(len(replist)):
                if replist[n]:
                    sheet1.write(line, n, replist[n])
    f.save(path + '合并数据.xlsx')
    # os.remove(path + 'temp.txt')


if __name__ == '__main__':
    # 循环目录下所有文件
    filelist = os.listdir(path)
    for filename in filelist:
        rows = WriteTemp(path + filename)
        row += rows
    WriteXlsx(row)
