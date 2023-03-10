import datetime
import json
import os
import time

import common.requests

ABS_PATH = os.path.abspath(__file__) #获取当前文件的绝对路径
DIR_NAME = os.path.dirname(ABS_PATH) #获取文件所在的目录

print(ABS_PATH)
print(DIR_NAME)
print(DIR_NAME)

# print(str(datetime.datetime.now()).split(' ')[0])
# print(str(datetime.datetime.now())[:10])
# print(str(datetime.datetime.now())[:10] + ' 22:00:00')
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
# print(int(2.3))
# print(int(2.8))

