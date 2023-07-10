'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/23 11:41
software: PyCharm
'''
import socket

IP = "192.168.5.163"  # 服务器ip

host = f"https://{IP}:8440"
password = 'wnt8000LLy&y'  # 堡垒机密码
# password = 'wnt8000LLy&y'

# linux 配置
linux_port = '22'
linux_user = 'root'
linux_pass = 'Wnt.1@3456'

# rdp配置
rdp_ip = '192.168.4.119'  # 远程桌面ip
rdpPassword = 'Admin@123'  # 远程桌面密码
# name_list = ['op1']  # 堡垒机用户名
# name_list = ['op1', 'op2', 'op3', 'op4', 'op5', 'op6', 'op7', 'op8', 'op9', 'op10']   # 堡垒机用户名
name_list = ['op1']   # 堡垒机用户名

# ssh配置
ssh_ip = '192.168.5.163'


# 获取本机ip
def get_local_host(prefix):
    host_ip = ''
    # 单ip获取
    local_host = socket.gethostbyname(socket.gethostname())
    if '192.168.4' in local_host:
        host_ip = local_host
    else:  # 多ip指定获取
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip.startswith(prefix):
                host_ip = ip
    return host_ip


local_ip = get_local_host('192.168.4')
print(local_ip)
