import os
local_dir = os.getcwd()

gp_name = input("请输入监控的股票名称：")
gp_price_min = input("请输入股票的最低买入价格：")
gp_price_max = input("请输入股票最低的售卖价格：")
worker = input("请输入要通知的微信用户名（备注名）：")


def write_file(comand):
    file = fr"{local_dir}\run.bat"
    # 使用密码需要根据执行主机的系统编码，否则无法终端执行bat文件，dos窗口：chcp，活动代码936 代表GBK编码
    # myfile = open(file, "w", encoding="utf-8")
    myfile = open(file, "w")
    myfile.write(comand)
    myfile.close()


if __name__ == '__main__':
    cmd = f"python {local_dir}\\monitor_gp.py {gp_name} {gp_price_min} {gp_price_max} {worker}"
    write_file(cmd)
    os.chdir(local_dir)
    os.system('run.vbs')
    print("\n---------------------\n程序已启动，请在Windows的任务管理器查看python.exe")