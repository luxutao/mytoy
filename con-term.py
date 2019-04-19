#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    telnet 连接设备管理，支持添加设备、删除设备及设备列表
"""

import pexpect
import sys
import re
import os
import pickle
import operator
import random

try:
    ip = sys.argv[1]
except:
    ip = None

pwd = os.path.abspath(__file__)
filepath = os.path.dirname(pwd) + '/devices.pickle'
def color(str):
    n = random.randint(0, 7)
    return n, '\033[0;3%s;4%sm%s\033[0m' % (n, n, str)

def get_devices():
    """获得设备的排序及设备字典"""
    with open(filepath, 'rb') as f:
        devices = pickle.load(f)
    sort_devices = sorted(devices.items(), key=lambda e: e[0])
    return sort_devices, devices


def write_device(ip, username=None, password=None, add=None, delete=None):
    """序列化新设备字典"""
    _, devices = get_devices()
    if add:
        devices[ip] = {'username': username, 'password': password}
    elif delete:
        devices.pop(ip)
    with open(filepath, 'wb') as f:
        pickle.dump(devices, f)


def index_devices():
    """返回索引及IP对应字典，{0:'x.x.x.x'}"""
    sort_devices, devices = get_devices()
    serial = {}
    for i, device in zip(range(len(sort_devices)), sort_devices):
        print('%s.  %10s' % (i, device[0]))
        serial[i] = device
    return serial


def connect(ip, username, password):
    """开始连接，判断超时或者账号密码错误导致的连接失败"""
    try:
        child = pexpect.spawn(command='telnet %s' % ip, timeout=3)
        child.expect('Username:')
        child.sendline(username)
        child.expect('Password:')
        child.sendline(password)
    except pexpect.exceptions.TIMEOUT:
        print('连接超时。')
        exit(1)
    try:
        index = child.expect(pattern=['Error'], timeout=1)
        if index == 0:
            print('登录失败')
            exit(1)
    except pexpect.exceptions.TIMEOUT:
        child.interact()
        # 关闭pexpect
        child.close()


def msg():
    """提示信息"""
    print('1. 添加设备')
    print('2. 删除设备')
    print('3. 设备列表')
    print('4. 退出')


def connect_ip(ip):
    _, devices = get_devices()
    try:
        username = devices.get(ip).get('username')
        password = devices.get(ip).get('password')
        connect(ip, username, password)
    except AttributeError as e:
        print('IP地址不存在，请先添加设备。')
        exit(1)


if __name__ == '__main__':
    if not os.path.exists(filepath):
        with open(filepath,'wb') as f:
            pickle.dump({}, f)
    # 如果存在参数则直接连接
    if ip:
        if len(re.findall(r'[0-9]+', ip)) == 4:
            connect_ip(ip)
        else:
            print('请输入IP地址或进行以下选择。')
    # 如果不存在参数操作选项
    while True:
        msg()
        try:
            choice = input('请输入选项： ')
        except KeyboardInterrupt:
            print('退出')
            exit(0)
        if choice == '1':
            ip = input('请输入IP： ')
            if len(re.findall(r'[0-9]+', ip)) != 4:
                print('请输入正确的IP地址。')
                continue
            username = input('请输入用户名： ')
            password = input('请输入密码： ')
            write_device(ip=ip, username=username, password=password, add=True)
            continue
        elif choice == '2':
            serial = index_devices()
            index_or_ip = input('请输入要删除的设备编号或IP地址： ')
            if len(re.findall(r'[0-9]+', index_or_ip)) == 4:
                ip = index_or_ip
            elif len(re.findall(r'[0-9]+', index_or_ip)) == 1:
                ip = serial.get(int(index_or_ip))[0]
            else:
                print('请输入一个正确的选项。')
                continue
            write_device(ip=ip, delete=True)
            print('删除成功。')
            continue
        elif choice == '3':
            serial = index_devices()
            index_or_ip = input('请输入要连接的设备编号或IP地址： ')
            if len(re.findall(r'[0-9]+', index_or_ip)) == 4:
                connect_ip(index_or_ip)
            elif len(re.findall(r'[0-9]+', index_or_ip)) == 1:
                try:
                    device = serial.get(int(index_or_ip))
                    username = device[1].get('username')
                    password = device[1].get('password')
                except TypeError:
                    print('该编号不存在。')
                    continue
                connect(device[0], username, password)
            else:
                print('请输入一个正确的选项。')
                continue
        elif choice == '4':
            break
        elif re.findall(r'^[a-zA-Z].+?[a-zA-Z]$',choice):
            columns, lines = os.get_terminal_size()
            blocks = 0
            for s in range(columns * lines):
                n, col = color(' ')
                if n == 0:
                    blocks += 1
                print(col,sep='',end='')
            print('\n',sep='',end='')
            while True:
                try:
                    block_count = input('请输入有多少块黑色的(手动滑稽)：')
                    if int(block_count) == blocks:
                        print('666')
                        break
                    else:
                        print('好笨哦。手动再见~')
                        exit(1)
                except KeyboardInterrupt:
                    print('居然使用Ctrl+c😒。')
                    continue
                except EOFError:
                    print('居然使用Ctrl+d😒。')
                    continue
                except ValueError:
                    print('请问你输入的是数字吗？')
                    continue
        else:
            print('输入错误，请重新输入')
            continue
