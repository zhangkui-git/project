"""
author:kui.zhang
contact: zkuuuuuu@163.com
datetime:2022/7/08 17:51
run_method: python monitor_gp.py 股票名称或股票代码
"""
import sys

import requests
import random
import time
import datetime
import os
import sys
from log2file import *
import auto_put_vx

gp_name = sys.argv[1]
gp_price_min = float(sys.argv[2])
gp_price_max = float(sys.argv[3])
worker = sys.argv[4]

local_dir = os.getcwd()


def monitor_gp():
    while True:
        url = f"https://finance.pae.baidu.com/selfselect/sug?wd={gp_name}&skip_login=1&finClientType=pc"
        res = requests.get(url)
        gp_price = float(res.json()["Result"]["stock"][0]["price"])
        if gp_price >= gp_price_max:
            s_info = "股票可卖，SSSSSSS"
            auto_put_vx.send_msg(f"{worker}", s_info)
        if gp_price <= gp_price_min:
            b_info = "股票可买，BBBBBBB"
            auto_put_vx.send_msg(f"{worker}", b_info)
        log_info = f'当前时间为: {str(datetime.datetime.now())}, 股票名称：{res.json()["Result"]["stock"][0]["name"]}, 股票当前价格：{gp_price}'
        # print(log_info)
        logging.info(log_info)
        time.sleep(random.randint(1, 10) + random.randint(1, 10))


if __name__ == '__main__':
    monitor_gp()



