#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import time
import pysyslogclient
import sys
import os


class SyslogSend:
    count = 0
    sleep = 0
    tmp_time = 0
    # UDP协议
    @staticmethod
    def UDPsyslog(message):
        data = bytes(message, 'UTF-8')
        client.send(data)

    # 主函数
    def test():
        for line in open(log_file, encoding='utf-8'):
            print(22222)
            if not line.startswith("#"):  # 过滤
                log = line.rstrip('\n')
                if SyslogSend.count == 0:
                    SyslogSend.tmp_time = time.time()
                SyslogSend.UDPsyslog(log)
                SyslogSend.count += 1
                if SyslogSend.count % 300 == 0:
                    time.sleep(0.01)
                print(33333)
                print(38888883333)
                print(SyslogSend.count)
                # 速率
                # 理论上不加sleep 速率一定大于输入的值，跟机器性能有关系，问题暂时保留
                if SyslogSend.count % speed == 0:
                    print(66666)
                    now_time = time.time()
                    sum_time = now_time - start_time
                    if SyslogSend.count == speed and sum_time == 0.0:
                        sum_time = 0.001
                    else:
                        sum_time = sum_time
                    v = round(SyslogSend.count / sum_time)
                    if v > speed + 100:
                        SyslogSend.sleep = round(1 - (now_time - SyslogSend.tmp_time), 5)
                        time.sleep(SyslogSend.sleep)
                        SyslogSend.tmp_time = time.time()
                    elif v < speed:
                        SyslogSend.sleep = SyslogSend.sleep - 0.01
                        time.sleep(SyslogSend.sleep)
                        SyslogSend.tmp_time = time.time()
                    else:
                        time.sleep(SyslogSend.sleep)
                        SyslogSend.tmp_time = time.time()
                    log_info = f'日志总量： {SyslogSend.count},  用时： {round(now_time - start_time, 3)}, 速率:  {v}, 此时的间隔为: {SyslogSend.sleep}'
                    print(log_info)
                print(444444)
                # 定额
                if SyslogSend.count >= quota:
                    print(777777)
                    sys.exit(0)
                # 定时
                if time.time() - start_time >= timing:
                    print(8888888888)
                    sys.exit(0)


def put_udp():
    try:
        while True:  # todo 循环次数
                SyslogSend.test()
                print(55555)
    except KeyboardInterrupt:
        stop_time = time.time()
        print("手动结束！")
        log_end_info = "=" * 8 + "stop:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
        log_sum = f"日志总量： {SyslogSend.count}"
        log_sum_time = f"持续时间： {round(stop_time - start_time, 3)}"
        log_avg = f"平均速率： {round(SyslogSend.count / (stop_time - start_time))} EPS"
        print(log_end_info + "\n" + log_sum + "\n" + log_sum_time + "\n" + log_avg)
        sys.exit(0)
    except SystemExit:
        stop_time = time.time()
        print("自动结束！")
        log_end_info = "=" * 8 + "stop:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
        log_sum = f"日志总量： {SyslogSend.count}"
        log_sum_time = f"持续时间： {round(stop_time - start_time, 3)}"
        log_avg = f"平均速率： {round(SyslogSend.count / (stop_time - start_time))} EPS"
        print(log_end_info + "\n" + log_sum + "\n" + log_sum_time + "\n" + log_avg)
        sys.exit(0)
    except Exception as e:
        sys.exit(0)


if __name__ == '__main__':
    local_file_dir = os.getcwd()
    log_file = './no_network_V2R1_7.txt'
    host = '192.168.4.164'
    speed = '10000'
    timing = 60
    quota = 1000000000
    client = pysyslogclient.SyslogClientRFC5424(host, 514, proto="UDP")
    log_start_info = "=" * 8 + "start:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
    print(log_start_info)
    start_time = time.time()
    print(111111)
    put_udp()

