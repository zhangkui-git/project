import time
import pysyslogclient

# 通过UDP协议发送syslog日志
client = pysyslogclient.SyslogClientRFC5424('192.168.4.60', 514, proto="UDP")
# client = pysyslogclient.SyslogClientRFC5424('192.168.10.101', 514, proto="TCP")
# 通过TCP协议发送syslog日志
# mip = [f"192.{f}.11.{i}" for i in range(1, 250) for f in range(1, 16)]
# mip = [f"152.{f}.55.{i}" for i in range(1, 250) for f in range(1, 20)]
# print(mip, "\n", len(mip))

file = 'network_info.txt'


def put_1():
    for line in open(file, encoding='utf-8'):
        if not line.startswith("#"):  # 过滤
            data = line.rstrip('\n')
            data1 = bytes(data, "UTF-8")
            client.send(data1)


def put_2():
    for ip in mip:
        str2 = f"12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.11.124|^Probe201229008|^2021-06-03 16:28:37|^17|^{ip}|^|^64766|^224.0.11.252|^|^5355|^d0:37:45:1e:8e:90|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^"
        data1 = bytes(str2, "UTF-8")
        client.send(data1)
        # print(x)
        time.sleep(0.005)


if __name__ == '__main__':
    mip = [f'10.{ip1}.54.{ip}' for ip in range(50) for ip1 in range(10)]
    # mip = [f'10.251.251.{ip}' for ip in range(1, 50)]
    print(len(mip))
    # put_1()
    put_2()
















# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# message = "10|^null|^|^2|^1|^0|^|^|^2021-06-03 14:54:28|^2021-06-03 14:54:28|^WIN-93J8ESTPGGR-威努特|^192.168.40.177|^192.168.40.178|^1|^c:\software\abc\1.txt|^1|^EA14A453WIN-93J8ESTPGGR-威努特|^null|^null|^vulnerability|^文件保护，修改|^|^c:\windows\system32\notepad.exe|^0|^null|^1|^3|^"
# data = bytes(message, 'UTF-8')
# s.sendto(data, ("192.168.4.165", 514))
# s.close()




