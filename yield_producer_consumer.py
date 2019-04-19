#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    
"""

def consumer():
    last = ''
    while True:
        receival = yield last
        if receival is not None:
            print('Consume %s' % receival)
            last = receival


def producer(gen, n):
    """发送一个none进行初始化，执行到达last停止，然后发送x到receival变量，然后继续执行下面，再次执行到last返回"""
    gen.send(None)
    x = 0
    while x < n:
        x += 1
        print('Produce %s' % x)
        last = gen.send(x)
    gen.close()


gen = consumer()
producer(gen, 5)
