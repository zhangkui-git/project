from scapy.all import *

packet = rdpcap("1.pcap")  #读取pcap文件

New_Packet = []    #创建一个新的对象
ii = 0
for pkt in packet:

    if pkt['IP'].src == "10.250.73.13":
        # pkt['IP'].src = "70.0.0.1"
        # pkt['IP'].dst = "163.1.1.1"
        pkt['port'].src = 34926
        # pkt['Ether'].src = "20:47:47:95:93:90"
        # pkt['Ether'].dst = "d0:c5:d3:ed:62:15"
    # else:
    #     pkt['IP'].dst = "70.0.0.1"
    #     pkt['IP'].src = "163.1.1.1"
    #     pkt['Ether'].src = "d0:c5:d3:ed:62:15"
    #     pkt['Ether'].dst = "20:47:47:95:93:90"
    # if ii == 28:         #针对第28条数据流进行flags的替换，0x18十六进制转换成十进制是24
    #     pkt['TCP'].flags = 0x18
    #
    # pkt['IP'].chksum = None         #检验和会自动进行校验
    # pkt['TCP'].chksum = None
    #print("new chksum:" + str(ch1))
    if ii<=32:           #只保留32条流
        New_Packet.append(pkt)
    ii += 1


wrpcap("1_new.pcap", New_Packet)    #生成新的pcap
