#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import logging
import time
from datamodel import *
from log2file import *
import pysyslogclient
import sys


class SyslogSend:
    count = 0

    # UDP协议
    @staticmethod
    def UDPsyslog(message):
        data = bytes(message, 'UTF-8')
        client.send(data)

    # 主函数
    def test():
        for line in open(log_file, encoding='utf-8'):
            if not line.startswith("#"):  # 过滤
                log = line.rstrip('\n')
                SyslogSend.UDPsyslog(log)

                SyslogSend.count += 1
                # 速率
                if SyslogSend.count % EPS == 0:
                    now_time = time.time()
                    log_info = f'日志总量： {SyslogSend.count},  用时： {round(now_time - start_time, 3)}, 速率:  {round(SyslogSend.count / (now_time - start_time))}'
                    # print(log_info)
                    logging.info(log_info)
                    time.sleep(sleep)
                # 定额
                if SyslogSend.count >= quota:
                    sys.exit(0)
                # 定时
                if time.time() - start_time >= timing:
                    sys.exit(0)


log_start_info = "=" * 8 + "start:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
logging.info(log_start_info)
start_time = time.time()


def put_udp():
    try:
        while True:  # todo 循环次数
                SyslogSend.test()
    except KeyboardInterrupt:
        stop_time = time.time()
        logging.info("手动结束！")
        log_end_info = "=" * 8 + "stop:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
        log_sum = f"日志总量： {SyslogSend.count}"
        log_sum_time = f"持续时间： {round(stop_time - start_time, 3)}"
        log_avg = f"平均速率： {round(SyslogSend.count / (stop_time - start_time))} EPS"
        logging.info(log_end_info + "\n" + log_sum + "\n" + log_sum_time + "\n" + log_avg)
        sys.exit(0)
    except SystemExit:
        stop_time = time.time()
        logging.info("自动结束！")
        log_end_info = "=" * 8 + "stop:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
        log_sum = f"日志总量： {SyslogSend.count}"
        log_sum_time = f"持续时间： {round(stop_time - start_time, 3)}"
        log_avg = f"平均速率： {round(SyslogSend.count / (stop_time - start_time))} EPS"
        logging.info(log_end_info + "\n" + log_sum + "\n" + log_sum_time + "\n" + log_avg)
        sys.exit(0)
    except Exception as e:
        logging.info(e)
        sys.exit(0)


if __name__ == '__main__':
    # 可手动修改端口和协议
    client = pysyslogclient.SyslogClientRFC5424(host, 514, proto="UDP")
    if sys.argv[1] == "config":
        put_udp()
    else:
        EPS = int(sys.argv[2])
        sleep = float(sys.argv[3])
        host = sys.argv[1]
        timing = int(sys.argv[4])
        quota = int(sys.argv[5])
        put_udp()

