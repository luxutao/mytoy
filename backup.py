#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    本地电脑备份到其他的目录，工作电脑备份到smb服务器
"""


import tarfile, getpass
import datetime
import os, time, glob
import sys, shutil
import re
from smb.SMBConnection import SMBConnection

Start = time.time()
username = getpass.getuser()  # 获得当前用户
Home_path = '/storage/Backups/'
Time = datetime.datetime.now().strftime('%Y-%m-%d')  # 日期
Excludes_path = ['/home/xxx/.cache', '/home/xxx/.local/share/Steam/steamapps/common']


# 定义Samba类，进行连接、上传、删除等操作
class Samba():
    # 参数为用户、密码、本地计算机名、Samba计算机名、Samba地址、Samba端口
    def __init__(self, user, passwd, localhost, remotehost, address, port):
        self.conn = SMBConnection(user, passwd, localhost, remotehost)
        self.status = self.conn.connect(address, port)

    def Time_Remove(self):
        if self.status:
            for file in self.conn.listPath('samba', 'backup')[2:]:
                if round((time.time() - file.create_time) / 3600 / 24) > 30:
                    self.conn.deleteFiles('samba', 'backup/{0}'.format(file.filename))
        shutil.rmtree(Home_path)

    # 上传文件到backup目录下
    def upload(self, localfile):
        with open(localfile[0], 'rb') as up:
            self.conn.storeFile('samba', 'backup/{0}'.format(os.path.basename(localfile[0])), up)

    def close(self):
        self.conn.close()
        print('上传到Samba服务器成功，请登录查看。')


# 如果不存在路径则创建
def Create(path):
    if not os.path.exists(path):
        os.mkdir(path)


# 移除60天以前的的文件
def Remove(path):
    for file in glob.glob('{0}*.tar.gz'.format(path)):
        if round((time.time() - os.path.getmtime(file)) / 3600 / 24) > 60:
            os.remove(file)


# def Exclude_filter(tarinfo):
#     if tarinfo.name in [path[1:] for path in Excludes_path]:
#         return None
#     else:
#         return tarinfo


# 排除函数，返回True的代表排除
def Exclude(name=''):
    if name in Excludes_path:
        return True
    else:
        return False


# 开始创建一个tar文件，并使用exclude参数进行筛选排除，如果出现权限拒绝，则将该目录或文件添加到Excludes_path列表中，并且重新开始执行
def Begin(path, tt, user):
    try:
        with tarfile.open('{2}{1}_HOME_BACKUP_{0}.tar.gz'.format(tt, user, path), 'w:gz') as tar:
            # tar.add('/home/{0}'.format(user),filter=Exclude_filter)
            tar.add('/home/{0}'.format(user), exclude=Exclude)
            # tar.add('/home/{0}'.format(user))
    except PermissionError as error:
        print('raise PermissionError {0}(已跳过)'.format(str(error)))
        os.remove('{2}{1}_HOME_BACKUP_{0}.tar.gz'.format(tt, user, path))
        PATH = re.match(r'.*\'(.+?)\'.*', str(error))
        Excludes_path.append(PATH.group(1))
        Begin(path, Time, username)
    return True


# 计算耗费时间
def Count(start, path):
    if Begin(path, Time, username):
        end = time.time()
        print('{0}备份成功，耗时约{1:.2f}s'.format(Time, (end - start)))


if __name__ == '__main__':
    if sys.argv[1] == 'work':
        Create(Home_path)
        Count(Start, Home_path)
        smb = Samba('用户名', '密码', 'ThinkPad-E450c', 'FTP_SERVER', '地址', 139)
        smb.upload(glob.glob('{0}*'.format(Home_path)))
        smb.Time_Remove()
        smb.close()
    elif sys.argv[1] == 'home':
        Create(Home_path)
        Count(Start, Home_path), Remove(Home_path)
    else:
        print('请输入正确的参数，‘work’ or ‘home’')
        sys.exit(1)
