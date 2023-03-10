import paramiko
import datetime

add_time = datetime.datetime.now()
com_time = str(add_time.strftime('%Y%m%d%H%M%S'))

# def upload():
#     # 连接虚拟机centos上的ip及端口，实例化一个transport对象
#     transport = paramiko.Transport(("192.168.92.128", 22))
#     transport.connect(username="zhangkui", password="ab2021cdzk")
#     # 将实例化的Transport作为参数传入SFTPClient中
#     sftp = paramiko.SFTPClient.from_transport(transport)
#     # 将“calculator.py”上传到filelist文件夹中
#     sftp.put('D:\work_down\zk.txt', '/home/zhangkui/zhangkui/bak/zk.txt')
#     # 将centos中的aaa.txt文件下载到桌面
#     # sftp.get('/filedir/aaa.txt', r'C:\Users\duany_000\Desktop\test_aaa.txt')
#     transport.close()
#
#


def sshzk():
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    # 即允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname="192.168.92.128", port=22, username="zhangkui", password="ab2021cdzk")
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(f'cd /home/zhangkui/zhangkui/bak; mkdir {com_time}')
    # 结果放到stdout中，如果有错误将放到stderr中
    result = stdout.read().decode()
    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    print("--------------Create Complete--------------")


if __name__ == '__main__':
    # upload()
    sshzk()
