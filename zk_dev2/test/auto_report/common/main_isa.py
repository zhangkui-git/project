#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import logging
import time
from log2file import *
import pysyslogclient
from select_es import *
from send_mail import sendmail
from ssh_get_lost import ssh_cen


class SyslogSend:
    count = 0
    tmp_time = 0
    sleep = 0
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
                if SyslogSend.count == 0:
                    SyslogSend.tmp_time = time.time()
                    # print("11-------", tmp_time)
                SyslogSend.UDPsyslog(log)
                SyslogSend.count += 1
                if SyslogSend.count % 300 == 0:
                    time.sleep(0.01)
                # 速率
                # 理论上不加sleep 速率一定大于输入的值，跟机器性能有关系，问题暂时保留
                if SyslogSend.count % speed == 0:
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
                    logging.info(log_info)
                    # print(log_info)

                # 定额
                if SyslogSend.count >= quota:
                    sys.exit(0)
                # 定时
                if time.time() - start_time >= timing:
                    sys.exit(0)


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
        avg = round(SyslogSend.count / (stop_time - start_time), 3)
        log_avg = f"平均速率： {avg} EPS"
        logging.info(log_end_info + "\n" + log_sum + "\n" + log_sum_time + "\n" + log_avg)
        # 增加延迟时间，因为速率较高可能会有一点积压，消费完在查es
        time.sleep(60)
        end_sum_es = select_es2()
        # 增加延迟时间，es数据量较大可能查询较慢
        time.sleep(20)
        sys_sum = end_sum_es - begin_sum_es
        end_es_lost_sum = ssh_cen()
        time.sleep(20)
        es_lost_sum = end_es_lost_sum - begin_es_lost_sum
        end_num = f"{host}的es写入的数据-----{sys_sum}，系统es_lost丢失的数据---{es_lost_sum}"
        logging.info(end_num)
        sendmail(product, version, host, mem, time1, speed, SyslogSend.count, sys_sum, es_lost_sum, avg)
        sys.exit(0)
    except SystemExit:
        stop_time = time.time()
        logging.info("自动结束！")
        log_end_info = "=" * 8 + "stop:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
        log_sum = f"日志总量： {SyslogSend.count}"
        log_sum_time = f"持续时间： {round(stop_time - start_time, 3)}"
        avg = round(SyslogSend.count / (stop_time - start_time), 3)
        log_avg = f"平均速率： {avg} EPS"
        logging.info(log_end_info + "\n" + log_sum + "\n" + log_sum_time + "\n" + log_avg)
        # 增加延迟时间，因为速率较高可能会有一点积压，消费完在查es
        time.sleep(60)
        end_sum_es = select_es2()
        # 增加延迟时间，es数据量较大可能查询较慢
        time.sleep(20)
        sys_sum = end_sum_es - begin_sum_es
        end_es_lost_sum = ssh_cen()
        time.sleep(20)
        es_lost_sum = end_es_lost_sum - begin_es_lost_sum
        end_num = f"{host}的es写入的数据-----{sys_sum}，系统es_lost丢失的数据---{es_lost_sum}"
        logging.info(end_num)
        sendmail(product, version, host, mem, time1, speed, SyslogSend.count, sys_sum, es_lost_sum, avg)
        sys.exit(0)
    except Exception as e:
        logging.info(e)
        sys.exit(0)


if __name__ == '__main__':
    local_file_dir = os.getcwd()
    log_file = 'new_V2R1_7.txt'
    log_start_info = "=" * 8 + "start:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=" * 8
    logging.info(log_start_info)
    timing = time1 * 3600
    quota = 10000000 * 5000
    # 可手动修改端口和协议
    client = pysyslogclient.SyslogClientRFC5424(host, 514, proto="UDP")
    begin_sum_es = select_es2()
    time.sleep(10)
    begin_es_lost_sum = ssh_cen()
    time.sleep(10)
    start_num = f"{host}的es开始的数据-----{begin_sum_es}, es_lost开始的数据-----{begin_es_lost_sum}"
    logging.info(start_num)
    start_time = time.time()
    put_udp()

