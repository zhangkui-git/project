#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from sys import argv
# EPS：设定值，打印日志的频率
# sleep：间隔，控制真实的速率
EPS, sleep = 10000, 2  # 通过EPS和sleep控制真实的速率

# ip
host = "192.168.4.165"

# 日志目录
log_file = './V2R1_7.txt'

# 日志总量额定值
quota = 100*100000000  # 100亿

# 持续时间额定值，单位秒
# timing = int(argv[4]) * 3600 + 300  # 24小时
timing = 4 * 3600  # 24小时


if __name__ == '__main__':
    print(111)
