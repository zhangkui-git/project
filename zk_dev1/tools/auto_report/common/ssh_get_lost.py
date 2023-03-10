import paramiko
from select_es import *

pwd = select_ssh_pwd


def ssh_cen():
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    # 即允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=f"{host}", port=22, username="root", password=f"{pwd}")
    # ssh.connect(hostname="192.168.4.165", port=22, username="root", password=f"{pwd}")
    # 执行命令1
    stdin, stdout, stderr = ssh.exec_command("cd /root/logs/processor; cat info.log | grep -w es_sink_lost | awk '{print $8}' | tail -n  1")
    # 结果放到stdout中，如果有错误将放到stderr中
    result = stdout.read().decode()
    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    if result != '':
        return int(result)
    else:
        return 0


# if __name__ == '__main__':
#     ssh_cen()
