'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/23 11:41
software: PyCharm
'''
import socket

IP = "192.168.4.56"
# IP = "192.168.100.159"
host = f"https://{IP}:8440"
es_host = "http://{}:9200".format(IP)

# linux 配置
linux_port = '22'
linux_user = 'root'
linux_pass = 'Wnt.1@3456'

# 发送邮件配置

# SMTP服务器,这里使用qq邮箱
# mail_host = "smtp.qq.com"  #qq
mail_host = "smtp.qiye.163.com"
port = 465
# port = 933
# 发件人邮箱
# mail_sender = "847251287@qq.com"
# mail_sender = "yumeng.tian@winicssec.com"
# 邮箱授权码,注意这里不是邮箱密码
# mail_license = "ebfwzymgmjinbcij"  # qq邮箱
mail_license = "ZYmfvVAu3Ew6Z5dT"  # 企业邮箱
# 收件人邮箱，可以为多个收件人
mail_receivers = ["yumeng.tian@winicssec.com", 'yanting.chen@winicssec.com', 'gaibei.liu@winicssec.com',
                  'lili.shi@winicssec.com', 'yunteng.wei@winicssec.com',
                  'lemin.zheng@winicssec.com', 'hlyu@winicssec.com',
                  'myzhang@winicssec.com', 'xubo.mu@winicssec.com', 'kui.zhang@winicssec.com']


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
