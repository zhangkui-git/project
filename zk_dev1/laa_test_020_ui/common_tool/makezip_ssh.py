import os
import paramiko
import datetime
import zipfile

add_time = datetime.datetime.now()
com_time = str(add_time.strftime('%Y%m%d%H%M%S'))
dsc_path = '/home/zhangkui/zhangkui/allure/apache-tomcat-8.5.81/allure/report'
src_path = rf'D:\work_soft\python\project\zk_dev1\laa_test_020_ui\report\result{com_time}\html'
src_path_new = rf'D:\work_soft\python\project\zk_dev1\laa_test_020_ui\report\result{com_time}\html.zip'
get_url = f'http://192.168.4.165:8780/report/{com_time}/html/index.html'

source_dir = src_path
output_filename = src_path_new


# 压缩
def make_zip():
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            print(filename)
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    print("压缩完成-------：", output_filename)

def sshzk():
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    # 即允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname="192.168.4.165", port=22, username="zhangkui", password="ab2021cdzk")
    # 执行命令1
    stdin, stdout, stderr = ssh.exec_command(f'cd {dsc_path}; mkdir {com_time}')
    # 结果放到stdout中，如果有错误将放到stderr中
    result = stdout.read().decode()
    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 连接虚拟机centos上的ip及端口，实例化一个transport对象
    transport = paramiko.Transport(("192.168.4.165", 22))
    transport.connect(username="zhangkui", password="ab2021cdzk")
    # 将实例化的Transport作为参数传入SFTPClient中
    sftp = paramiko.SFTPClient.from_transport(transport)
    # 将“calculator.py”上传到filelist文件夹中
    sftp.put(f'{src_path_new}', f'{dsc_path}/{com_time}/html.zip')
    # 将centos中的aaa.txt文件下载到桌面
    # sftp.get('/filedir/aaa.txt', r'C:\Users\duany_000\Desktop\test_aaa.txt')
    transport.close()
    print("----------------Upload Complete----------------")
    # 执行命令2
    stdin, stdout, stderr = ssh.exec_command(f'cd {dsc_path}/{com_time}; unzip html.zip')
    # 结果放到stdout中，如果有错误将放到stderr中
    result = stdout.read().decode()
    # 获取错误提示（stdout、stderr只会输出其中一个）
    err = stderr.read()
    # 关闭连接
    ssh.close()
    print("--------------Create Complete--------------")



