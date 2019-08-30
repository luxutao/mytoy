#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import subprocess

from flask import Flask
from flask import request,jsonify
app = Flask(__name__)

@app.route('/')
def notice():
    message_status = request.args.get('message')
    stop_command = "ps -ef | grep '/home/luxutao/Projects/notice/NoticeTray.py' | grep -v 'grep' | grep -v '/bin/sh' | awk '{print $2}'"
    start_command = "/usr/bin/python3 /home/luxutao/Projects/notice/NoticeTray.py"
    stdout = subprocess.Popen(stop_command, stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    if message_status == 'True':
        # 解析相同，没有消息
        if stdout:
            subprocess.Popen("kill %s" % stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        if not stdout:   
            subprocess.Popen(start_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return jsonify({"code":200,"msg":"success"})

@app.route('/changeWorkSpace')
def changeWorkSpace():
    subprocess.Popen("qdbus org.kde.KWin /KWin setCurrentDesktop 1", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    return jsonify({"code":200,"msg":"success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
