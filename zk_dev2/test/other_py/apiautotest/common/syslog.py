'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2021/11/3 9:36
software: PyCharm
'''
import socket

from zk_dev2.test.other_py.apiautotest.config.config import IP
from zk_dev2.test.other_py.apiautotest.setting import ABS_PATH, DIR_NAME


def syslog(data):
    """
    Send syslog UDP packet to given host and port.
    """
    host = IP
    port = 514
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data.encode(), (host, port))
    sock.close()


def run(path):
    with open(DIR_NAME + path, "r", encoding="utf-8") as pf:
        alllines = pf.readlines()
        for line in alllines:
            data = r'' + line.strip("\n")  # windows解码的换行符是CR，LF，Linux的是
            # print(data)
            # print("%s" % (data))
            syslog(data)

if __name__ == '__main__':
    # print(DIR_NAME + r'\data\USM_V2R1_syslog_OnlySecurityLog.txt')
    syslog('100103|^Firewall210127007|^192.168.100.164|^|^低|^202004|^未知|^|^WOS|^0|^无|^2022-03-15 17:22:06.0|^默认区域|^2|^')