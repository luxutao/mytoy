#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    创建三个目录，然后将1920和1366的图片进行拼接，变成3286的图片，适合用于双显示器
"""


from PIL import Image
import glob, os, random, time, subprocess, getpass

user = getpass.getuser()
P1920 = '/home/%s/Pictures/P1920/' % user
P1366 = '/home/%s/Pictures/P1366/' % user
P3286 = '/home/%s/Pictures/P3286/' % user


def convert(width, height, list, path, delete=True):
    for name in list:
        Image.open(name).resize((width, height), Image.ANTIALIAS).save(path + '1_{0}'.format(os.path.basename(name)))
        if delete:
            os.remove(name)


def joint(small_list, big_list):
    if len(small_list) == len(big_list):
        print('请稍等~')
        for i_file in small_list:
            width = 3286
            height = 1080
            image = Image.new('RGB', (width, height), (255, 255, 255))
            im1 = Image.open(i_file)
            im1w, im1h = im1.size
            im2 = Image.open(P1920 + '%s' % os.path.basename(i_file)[2:])
            im2w, im2h = im2.size
            try:
                cro1 = im1.crop((0, 0, im1w, im1h))  # 裁剪第一张图片,（left,up,right,down）
                cro2 = im2.crop((0, 0, im2w, im2h))
                image.paste(cro1, (0, 0, im1w, im1h))  # 粘贴到左到右1366，上到下768
                image.paste(cro2, (im1w, 0, width, height))  # 粘贴到左开始1366，右到3286，上到下1080
                image.save(P3286 + '%s' % os.path.basename(i_file))
                time.sleep(random.random() * 3)
            except:
                pass
    else:
        print('两个目录下的文件数量不同，已经退出~')
        exit(1)


if __name__ == '__main__':
    for path in [P1366, P1920, P3286]:
        if not os.path.exists(path):
            subprocess.call('mkdir -p {0}'.format(path), shell=True)
    convert(1920, 1080, glob.glob(P1920 + '*.jpg'), P1920)
    convert(1366, 768, glob.glob(P1920 + '*.jpg'), P1366, delete=False)
    joint(glob.glob(P1366 + '*.jpg'), glob.glob(P1920 + '*.jpg'))
