
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

ua = UserAgent()
# header = {'User-Agent': f'{ua.firefox}', 'Cookie': "global_cookie=ly9htoz4k600ggakp3xvzvbcl18lfmde5gn; __utmz=147393320.1679651997.1.1.utmcsr=fangjia.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; csrfToken=wYk5QwML5sJOKArdZuASIIyk; __utmc=147393320; city=hs; __utma=147393320.2094528334.1679651997.1680244532.1680504167.3; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; global_wapandm_cookie=3o8ggf348y5wh82mqecm0rllx1ulg0gt44l; unique_wapandm_cookie=U_3o8ggf348y5wh82mqecm0rllx1ulg0gt44l*1; g_sourcepage=xf_lp%5Elb_pc; __utmb=147393320.40.10.1680504167; unique_cookie=U_sgopr3p872nki88yh0phen0d926lfw67kiq*24"}
header = {'User-Agent': f'{ua.firefox}'}
url = 'https://hs.newhouse.fang.com/house/s/e31/'
res = requests.get(url=url, headers=header, verify=False)
res.encoding = res.apparent_encoding
r_html = res.text
# soup5 = bs(r_html, "html.parser")
# soup5 = bs(r_html, 'lxml')
print(r_html)
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



