import time
import pysyslogclient

# 通过UDP协议发送syslog日志
client = pysyslogclient.SyslogClientRFC5424('192.168.100.63', 514, proto="UDP")
# data = '111111111'
# data1 = bytes(data, "UTF-8")
# client.send(data1)
# client = pysyslogclient.SyslogClientRFC5424('192.168.10.101', 514, proto="TCP")
# 通过TCP协议发送syslog日志
# mip = [f"192.{f}.11.{i}" for i in range(1, 250) for f in range(1, 16)]
# mip = [f"192.{f}.55.{i}" for i in range(1, 250) for f in range(1, 250)]
# mip = [f"192.1{i}.11.1" for i in range(1, 60)]
# print(mip, "\n", len(mip))

# file = 'network_info.txt'


def put_1():
    for line in open(file, encoding='utf-8'):
        if not line.startswith("#"):  # 过滤
            data = line.rstrip('\n')
            data1 = bytes(data, "UTF-8")
            client.send(data1)


file = open('no_ok_asset.txt', 'a')


def put_2():
    for ip in mip:
        str2 = f"12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{ip}|^Probe201229008|^2021-06-03 16:28:37|^17|^{ip}|^|^64766|^{ip}|^|^5355|^d0:37:45:1e:8e:90|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^\n"
        data1 = bytes(str2, "UTF-8")
        file.write(str2)
        # client.send(data1)
        # print(data1)
        # time.sleep(0.1)


if __name__ == '__main__':
    mip = [f'40.{ip1}.51.{ip}' for ip in range(250) for ip1 in range(250)]
    # mip = [f'41.{ip1}.51.51' for ip1 in range(61, 195)]
    print(f"开始写入未确认资产{len(mip)}个", mip)
    # put_1()
    put_2()
    print(f"写入未确认资产{len(mip)}个 已完成")























