import os
import sys

local_dir = os.getcwd()
print(local_dir)


def write_file(file, str1):
    myfile = open(file, 'w')
    myfile.write(str1)
    myfile.close()


if __name__ == '__main__':
    file = 'start.bat'
    cmd = 'python get_ppts_name.py'
    write_file('start.bat', cmd)
    os.chdir(local_dir)
    os.system('auto.vbs')
    print("\n---------------------\n程序已启动，请在Windows的任务管理器的详细信息页面查看python.exe进程")