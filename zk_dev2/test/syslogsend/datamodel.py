#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# EPS：设定值，打印日志的频率
# sleep：间隔，控制真实的速率
EPS, sleep = 210, 1  # 通过EPS和sleep控制真实的速率

# ip
host = '192.168.100.149'

# 日志目录
log_file = './syslog_txt/V2R1(性能测试使用数据).txt'

# 日志总量额定值
quota = 10*100000000  # 10亿

# 持续时间额定值，单位秒
timing = 300  # 24小时


if __name__ == '__main__':
    print("修改完参数之后请运行本目录下的main.py")
