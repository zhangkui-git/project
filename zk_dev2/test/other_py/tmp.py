
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

print(str(datetime.datetime.now())[:11])


file_object2 = open("tmp_info.txt",'r')
try:
    lines = file_object2.readlines()
    print("type(lines)=",type(lines))  # type(lines)= <type 'list'>\
    info1 = ''
    for line in lines:
        info1 = info1 + line
    print("line=222", info1)
finally:
    file_object2.close()




















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

