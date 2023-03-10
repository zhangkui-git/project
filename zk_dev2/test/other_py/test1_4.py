from scapy.all import *
from scapy.layers.inet import *
import threading
# a = ['192.168.13.11', '192.168.13.12', '192.168.13.13', '192.168.13.14']
file = r'./data.txt'
host = "10.1.198.83"

def put_udp():
    data = "3|^A5A07D79508B40038CB5671A00762ADA|^xx|^3|^1|^1|^无意见|^2019-10-19 15:16:05.0|^2019-10-19 15:16:05.0|^2019-10-19 15:16:05.0|^终端名称|^192.168.1.1|^128.0.5.87|^129.0.5.165|^100|^xxx|^2|^audit|^A5A07D79508B40038CB5671A00762ADA|^1|^A5A07D79508B40038CB5671A00762ADA|^"
    for line in open(file, encoding='utf-8'):
        if not line.startswith("#"):  # 过滤
            ip = line.rstrip('\n')
            send(IP(src=ip, dst='192.168.4.165')/UDP(sport=random.randint(100, 20000), dport=514)/data)

    print("====完成====")


# def self_run():
#     t1 = threading.Thread(target=put_udp, args=(1,))
#     t2 = threading.Thread(target=put_udp, args=(2,))
#     t1.start()
#     time.sleep(1)
#     t2.start()


if __name__ == '__main__':
    # self_run()
    while True:
        put_udp()
        time.sleep(1)


