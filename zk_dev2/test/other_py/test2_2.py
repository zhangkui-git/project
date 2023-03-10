from scapy.all import *
from scapy.layers.inet import *

data = "3|^A5A07D79508B40038CB5671A00762ADA|^xx|^3|^1|^1|^无意见|^2019-10-19 15:16:05.0|^2019-10-19 15:16:05.0|^2019-10-19 15:16:05.0|^终端名称|^192.168.1.1|^128.0.5.87|^129.0.5.165|^100|^xxx|^2|^audit|^A5A07D79508B40038CB5671A00762ADA|^1|^A5A07D79508B40038CB5671A00762ADA|^"
send(IP(src='192.168.14.164', dst='192.168.4.155')/UDP(sport=random.randint(100, 20000), dport=514)/data, verbose=False)
# for line in open(file, encoding='utf-8'):
#     if not line.startswith("#"):  # 过滤
#         ip = line.rstrip('\n')
#         send(IP(src=ip, dst='192.168.4.165')/UDP(sport=random.randint(100, 20000), dport=514)/data)

print("====完成====")


# # data = "10|2|1|0|2021-06-03 14:54:28"
# cnt = 1
# num = 40
# while cnt <= num:
#     send(IP(src='19.13.11.2', dst='192.168.4.154')/UDP(sport=7371, dport=514)/data)
#     cnt += 1





