#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Description:
    The command line version of the youdao dictionary
"""


import sys
import os
import requests


def request_youdao(s):
    """
    向有道词典web版发起翻译请求
    :param s: string
    :return: data
    :type: dict
    """
    assert s
    data = {'type': 'AUTO',
            'i': s,
            'doctype': 'json',
            '&xmlVersion': '1.8',
            'keyfrom': 'fanyi.web',
            'ue': 'UTF-8',
            'action': 'FY_BY_CLICKBUTTON',
            'typoResul': 'true'
            }
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc'
    req = requests.post(url, data=data)
    if req.json()['errorCode'] == 0:
        return req.json()
    return None


def parse_data(data):
    """
    解析返回的数据
    :param data: dict list str tuple
    :return: None
    """
    if isinstance(data, dict):
        for k, v in data.items():
            print(k + ': ')
            parse_data(v)
    elif isinstance(data, (list, tuple)):
        for i in data:
            parse_data(i)
    else:
        print(data)


def printer(data):
    """
    用特定的格式在屏幕上打印返回的数据
    :param data: from request_youdao function
    :return: None
    """
    color = lambda n, s: '\033[3%dm%s\033[0m' % (n, s)
    src = ''
    tgt = ''
    if data:
        for li in data['translateResult']:
            src += li[0]['src'] + '\n'
            tgt += li[0]['tgt'] + '\n'
        print(color(1, u'[In]:\n{spec}{s}'.format(spec=' ' * 4, s=src)))
        print(color(5, u'[Out]:\n{spec}{s}'.format(spec=' ' * 4, s=tgt)))
    try:
        for i in data['smartResult']['entries'][1:]:
            print(color(3, ' ' * 4 + i))
    except KeyError:
        pass
    except TypeError:
        pass


def main():
    """
    Main function
    :return: None
    """
    input_s = ''
    if not sys.stdin.isatty():
        input_s = sys.stdin.read(5120)
        if not input_s.strip():
            exit(1)
    else:
        try:
            input_s = sys.argv[1]
        except IndexError:
            pass
    if not input_s.strip():
        columns,lines = os.get_terminal_size()
        while 1:
            try:
                print('╱{strnums} Input {strnums}╲'.format(strnums='-' * int(((columns - 9) / 2))))
                input_s = sys.stdin.read()
            except EOFError:
                if input_s:
                    break
            except KeyboardInterrupt:
                exit(0)
            print('╲{strnums} End {strnums}╱'.format(strnums='-' * int(((columns - 7) / 2))))
            data = request_youdao(s=input_s)
            printer(data)
    data = request_youdao(s=input_s)
    printer(data)


if __name__ == '__main__':
    main()
