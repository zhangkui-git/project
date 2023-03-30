
# import requests
# res = requests.post('https://www.cnblogs.com/zhengyihan1216/p/11549820.html', verify=False)
# # res.encoding = res.apparent_encoding
# print(res.content.decode('utf-8'))
# print(res.text)
import datetime

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup as bs
import time
import re
import gzip
import urllib.request
from io import StringIO, BytesIO
from lxml import etree
import os

# ua = UserAgent()
# # header = {'User-Agent': f'{ua.chrome}', 'Cookie': 'acw_tc=2760779916794751608163076ee5aaa98ebf6109750844345fa69a1bd55895; acw_sc__v2=641ac1d86ef74858c95d120d4bd93e8839074eae'}
# header = {'User-Agent': f'{ua.firefox}'}
# # url = 'https://www.1ppt.com/plus/download.php?open=0&aid=103166&cid=3'
# # url = 'http://hb.offcn.com/html/jiaoshi/zhaokaoxinxi/hengshui/'
# # url = 'http://hb.offcn.com/html/hebeigongwuyuan/zhaokaoxinxi/hengshui/'
# url = 'http://hb.offcn.com/html/shiyedanwei/zhaokaoxinxi/hengshui/'
# res = requests.post(url=url, headers=header, verify=False)
# res.encoding = res.apparent_encoding
# r_html = res.text
# soup5 = bs(r_html, "html.parser")
# # soup5 = bs(r_html, 'lxml')
# # print(r_html)
# word_list = soup5.find('ul', class_="lh_newBobotm02")('li')
# # print(word_list)
#
# n = 1
# for b in word_list:
#     if n <= 5:
#         print(b.find_next('span').text.replace('\n', '').strip(),  '  ', b.select('a')[1].text, b.select('a')[1]['href'], '\n===================')
#         # print(222222, b.select('a')[1].text, b.select('a')[1]['href'])
#         # time.sleep(300)
#         n += 1
#     else:
#         break

# print(str(datetime.datetime.now())[:11])

import gzip

path = "D:\MyInfo_file\edpi.gz"  # 你的文件路径
f = gzip.open(path, 'rb')
num_zu = []
num_zu_1 = []
num_end = []
tmp_a_s = ''
start_time = datetime.datetime.now()

for line in f.readlines():  # 按行进行读取
    # s 为string类型，就是我们读取的文件中的一行
    s = line.decode('utf-8', errors='ignore').rstrip('\n')  # 读取之后要进行解码
    # s = str(line, encoding="utf-8")
    # print(s)
    # 取出秒数之前的字符串区别分组名称
    a_s = s.split('||')[0][:-1]
    a_ip = s.split('||')[1]

    name_zu = a_s + '0'
    if a_s != '' and a_s not in num_zu_1:
        num_zu.append(name_zu)
        num_zu_1.append(a_s)
        tmp_a_s = a_s
        tmp_num_end = {}
        num_end.append(tmp_num_end)
    elif a_s != '' and a_s in num_zu_1:
        a_s_index = num_zu_1.index(a_s)
        if a_ip in num_end[a_s_index]:
            num_end[a_s_index][a_ip] = num_end[a_s_index][a_ip] + 1
        else:
            num_end[a_s_index][a_ip] = 1

    elif a_s != '' and a_s == tmp_a_s and a_ip not in tmp_num_end:
        tmp_num_end[a_ip] = 1
    elif a_s != '' and a_s == tmp_a_s and a_ip in tmp_num_end:
        tmp_num_end[a_ip] = tmp_num_end[a_ip] + 1

# 打印分组的名称
print(num_zu)


for x, i in enumerate(num_end):
    a_val = list(i.values())
    a_key = list(i.keys())
    # print(sorted(a_val, reverse=True))
    # print(a_val.index(599))
    # print(a_key[285])
    num_max = str(sorted(i.values(), reverse=True)[0])
    print(num_zu[x] + '|' + a_key[a_val.index(sorted(i.values(), reverse=True)[0])] + '|' + num_max)

    # time.sleep(300)

stop_time = datetime.datetime.now()
print('耗时----: ', stop_time - start_time)




























# response1 = urllib.request.urlopen(url=url)
# print(33333, response1.info().get('Content-Encoding'))
# # print(response1.read())
# if response1.info().get('Content-Encoding') == 'gzip':
#     print(333)
#     # buf = StringIO(str(response1.read()))
#     buf = BytesIO(response1.read())
#     print(4444)
#     # buf = StringIO(response1.read())
#     # print(9999)
#     f = gzip.GzipFile(fileobj=buf)
#     print(555, type(f))
#     data = f.read()
#     print(data)
#     print(66666)
#     # 处理
#     f.close()
# else:
#     data = str(response1.read())

