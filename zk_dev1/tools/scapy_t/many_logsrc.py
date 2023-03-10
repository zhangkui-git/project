from scapy.all import *
from scapy.layers.inet import *
import time
from log2file import *
import threading
mip1 = [f"192.168.51.{i}" for i in range(1, 201)]
mip2 = [f"192.168.52.{i}" for i in range(1, 201)]
mip3 = [f"192.168.53.{i}" for i in range(1, 201)]
mip4 = [f"192.168.54.{i}" for i in range(1, 201)]
mip5 = [f"192.168.55.{i}" for i in range(1, 201)]
mip = mip1 + mip2 + mip3 + mip4 + mip5


def send_msg(ip, item):
    paket = IP(src=ip, dst='192.168.4.165') / UDP(sport=random.randint(100, 20000), dport=514) / item
    sendp(paket, verbose=False)


def put_udp(ip):
    for item in open("./V2R1_7.txt",  encoding='utf-8'):
        start_time = time.time()
        send_msg(ip, item)
        end_time = time.time()
        sleep1 = end_time - start_time
        if sleep1 < 1:
            sleep2 = 1 - sleep1
            time.sleep(sleep2)
            # print(f"等待时长为{sleep2}")
            logging.info(f"等待时长为{sleep2}")
        else:
            sleep2 = 1 - sleep1
            logging.info(f"等待时长为{sleep2}")


if __name__ == '__main__':
    num = 1
    sum1 = 10
    while num < sum1:
        put_udp()
        num += 1

