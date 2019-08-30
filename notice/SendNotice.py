#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import datetime


import imagehash
import requests
from PIL import ImageGrab, Image


def screenshot():
    x = 1130
    y = 730
    m = 1220
    n = 768
    files = []
    for i in range(3):
        files.append(ImageGrab.grab((x, y, m, n)))
        time.sleep(0.5)    
    return files


def is_same(images):
##        width,height = image1.size
##        for x in range(1,width):
##            for y in range(1,height):
##                if (image1.getpixel((x,y)) != image2.getpixel((x,y))) or (image1.getpixel((x,y)) != image3.getpixel((x,y))) or (image2.getpixel((x,y)) != image3.getpixel((x,y))):
##                    return False
    hash_1 = imagehash.average_hash(images[0])
    hash_2 = imagehash.average_hash(images[1])
    hash_3 = imagehash.average_hash(images[2])
    if (hash_1 != hash_2) or (hash_1 != hash_3) or (hash_2 != hash_3):
        return False
    return True


def send(message):
    data = requests.get("http://10.0.2.2:9999/?message=%s" % message).json()
    print(data)


def main():
    images = screenshot()
    same = is_same(images)
    send(same)

    
if __name__ == "__main__":
    while True:
        main()
        time.sleep(3)
