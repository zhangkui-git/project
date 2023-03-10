#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import socket
import time
import sys
from datamodel import *


class SyslogSend:
    count = 0

    def __init__(self):
        self.log_file = log_file
        self.host = host

    # UDP协议
    @staticmethod
    def UDPsyslog(message, host):
        data = bytes(message, 'UTF-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(data, (host, 514))
        s.close()

    # TCP协议
    @staticmethod
    def TCPsyslog(message, host):
        data = bytes(message, 'UTF-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 515))
        s.sendall(data)
        s.close()

    # 主函数
    def test(self):
        for line in open(self.log_file, encoding = 'utf-8'):
            if not line.startswith("#"):  # 过滤
                log = line.rstrip('\n')
                self.UDPsyslog(log, host = self.host)

                SyslogSend.count += 1
                # 速率
                if self.count % EPS == 0:
                    time.sleep(sleep)
                    now_time = time.time()
                    print("%s/%s" % (self.count, round(now_time - start_time, 3)), "速率:",
                          round(self.count / (now_time - start_time)))
                # 定额
                if self.count >= quota:
                    sys.exit(0)
                # 定时
                if time.time() - start_time >= timing:
                    sys.exit(0)


print("=" * 8, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "=" * 8)
start_time = time.time()
while True:  # todo 循环次数
    try:
        SyslogSend().test()
    except KeyboardInterrupt:
        stop_time = time.time()
        print("手动结束！")
        print("=" * 8, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "=" * 8)
        print("日志总量：", SyslogSend.count)
        print("持续时间：", round(stop_time - start_time, 3))
        print("平均速率：", round(SyslogSend.count / (stop_time - start_time)), "EPS")
        break
    except SystemExit:
        stop_time = time.time()
        print("自动结束！")
        print("=" * 8, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "=" * 8)
        print("日志总量：", SyslogSend.count)
        print("持续时间：", round(stop_time - start_time, 3))
        print("平均速率：", round(SyslogSend.count / (stop_time - start_time)), "EPS")
        break
    except Exception as e:
        print(e)
        break
