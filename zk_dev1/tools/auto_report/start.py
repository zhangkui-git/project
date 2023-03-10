import os
import sys

local_dir = os.getcwd()
method = input("请输入使用的方式，1. LAA全自动化性能测试，2. ISA/USM全自动化性能测试，3. 普通打流，请输入1/2/3 其中一个：")

if int(method) == 1 or int(method) == 2:
    product = input("请输入测试产品名称：")
    version = input("请输入测试产品版本号：")
    host = input("请输入需要测试的服务器地址：")
    host_pwd = input("请输入测试服务器密码(若为空，则为默认密码，直接回车即可)：")
    if host_pwd == "":
        host_pwd = "Wnt.1@3456"
    else:
        host_pwd = host_pwd
    es_name = input("请输入测试服务器的ES的账号(若为空，则为默认账号，直接回车即可)：")
    if es_name == "":
        es_name = "elastic"
    else:
        es_name = es_name
    es_pwd = input("请输入测试服务器的ES的密码(若为空，则为默认密码，直接回车即可)：")
    if es_pwd == "":
        es_pwd = "changeme"
    else:
        es_pwd = es_pwd
    time1 = input("请输入性能测试时间（正整数，单位：小时，例如：1、2、3）：")
    mem = input("请输入性能测试服务器的规格（示例：32G/16G/8G/双机服务器, 请输入32G/16G/8G/双机 其中一个）: ")
    speed = input("请输入性能测试的速率（正整数）：")


elif int(method) == 3:
    host = input("请输入需要打流的服务器IP：")
    speed = input("请输入固定的速率（正整数）：")
    time1 = input("定时：请输入打流的时长（正整数，单位：小时，例如：1、2、3）：")
    sum1 = input("定额：请输入打流的日志总量（正整数，单位：千万，例如：1、2、3）：")
else:
    print("请根据提示输入1/2/3 其中一个！")
    sys.exit(0)


def write_file(comand):
    file = fr"{local_dir}\start.bat"
    # print(file)
    # 使用密码需要根据执行主机的系统编码，否则无法终端执行bat文件，dos窗口：chcp，活动代码936 代表GBK编码
    # myfile = open(file, "w", encoding="utf-8")
    myfile = open(file, "w")
    myfile.write(comand)
    myfile.close()


if __name__ == '__main__':
    if int(method) == 1:
        cmd = f"python common/main_laa.py {product} {version} {host} {host_pwd} {es_name} {es_pwd} {time1} {mem} {speed}"
    elif int(method) == 3:
        cmd = f"python common/main_put.py {host} {speed} {time1} {sum1}"
    else:
        cmd = f"python common/main_isa.py {product} {version} {host} {host_pwd} {es_name} {es_pwd} {time1} {mem} {speed}"
    print(f"程序手动启动目录：{local_dir}", "\n", "程序启动命令：", cmd)
    write_file(cmd)
    os.chdir(local_dir)
    # print(os.getcwd())
    os.system('auto.vbs')
    print("\n---------------------\n程序已启动，请在Windows的任务管理器的详细信息页面查看python.exe进程")




