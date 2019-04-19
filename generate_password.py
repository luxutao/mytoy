#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    生成复杂性密码
"""


from itertools import product
import telnetlib
import random

word_low = 'abcdefghigklmnopqrstuvwxyz'
word_up = list(word_low.upper())
symbol = list('!@#$%^&*')
numbers = list('1234567890')
password = numbers + symbol + word_up + list(word_low)


def generate():
    return random.sample(password, 1)[0]


def main():
    while True:
        pwd = ''
        numbers = input('请输入要生成的密码位数(q or quit退出)： ')
        if numbers == 'q' or numbers == 'quit':
            break
        try:
            for _ in range(int(numbers)):
                pwd += generate()
            print("\033[32m" + pwd + "\033[0m")
        except ValueError:
            print("\033[31m输入错误，请重新输入！\033[0m")
            continue


if __name__ == '__main__':
    main()
