import datetime
import logging
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import requests
import os
from log2file import *

url = 'http://www.1ppt.com'
ua = UserAgent()
header = {'User-Agent': f'{ua.chrome}'}
file = './ppts_url.txt'
logging.info('--------------爬虫开始-------------')


def write_file(str1):
    myfile = open(file, 'w')
    myfile.write(str1)
    myfile.close()


# 获取PPT类目栏前7个列表、ppt列表获取ppt类型、每页PPT的URL根据列表+类型 写入字典
def get_pages_ppts_url():
    count = 1
    ppts_http_list = {}
    res = requests.post(url=url, headers=header, verify=False)
    res.encoding = res.apparent_encoding
    res_html = res.text
    soup = bs(res_html, "html.parser")
    li_1 = soup.find("div", id='navMenu')
    li1_list = li_1.find_all('li')
    for li in li1_list:
        if count <= 7:
            ppts_http_list[li.a.string] = url + li.a['href']
        count += 1
    logging.info('--------------ppts_http_list 写入字典完成-------------')
    # ppt类型列表
    # print(ppts_http_list)
    # 开始获取ppt列表中的ppt类型
    ppts1_http_list = {}
    for i in ppts_http_list:
        res1 = requests.post(url=ppts_http_list[i], headers=header, verify=False)
        res1.encoding = res1.apparent_encoding
        res1_html = res1.text
        soup1 = bs(res1_html, "html.parser")
        li_2 = soup1.find('div', class_='col_nav clearfix')
        li2_list = li_2.find_all('li')[1:]
        tmp_ppts1_http_list = {}
        for f in li2_list:
            tmp_ppts1_http_list[f.a.string] = url + f.a['href']
        ppts1_http_list[i] = tmp_ppts1_http_list
    logging.info('--------------ppts1_http_list 写入字典完成-------------')
    # 开始获取列表中每个ppt类型的页数的url
    ppts2_http_list = {}
    for h in ppts1_http_list:
        tmp_ppts2_http_list = {}
        for k in ppts1_http_list[h]:
            tmp_res2 = []
            res2 = requests.post(url=ppts1_http_list[h][k], headers=header, verify=False)
            res2.encoding = res2.apparent_encoding
            res2_html = res2.text
            soup2 = bs(res2_html, "html.parser")
            li_3 = soup2.find('dl', class_='dlbox')
            li3_list = li_3.find('div', class_='clearfix')('li')[2:-2]
            tmp_res2.append(ppts1_http_list[h][k])
            for j in li3_list:
                tmp_res2.append(ppts1_http_list[h][k] + j.a['href'])
            tmp_ppts2_http_list[k] = tmp_res2
        ppts2_http_list[h] = tmp_ppts2_http_list
    logging.info('--------------ppts2_http_list 写入字典完成-------------')
    return ppts2_http_list


# 根据每页的PPT的URL 获取 每页每个PPT的URL ， 在进一步获取每个ppt的url的下载url
def get_pages_down_zip():
    ppts2_http_list = get_pages_ppts_url()
    ppts3_http_list = {}
    # 根据每页的PPT的URL 获取 每页每个PPT的URL
    for l in ppts2_http_list:
        tmp_ppts3_http_list = {}
        for h in ppts2_http_list[l]:
            tmp_res3 = []
            for a in ppts2_http_list[l][h]:
                res3 = requests.post(url=a, headers=header, verify=False)
                res3.encoding = res3.apparent_encoding
                res3_html = res3.text
                soup3 = bs(res3_html, "html.parser")
                li_4 = soup3.find('ul', class_='tplist')('li')
                for b in li_4:
                    tmp_res3.append(url + b.a['href'])
            tmp_ppts3_http_list[h] = tmp_res3
        ppts3_http_list[l] = tmp_ppts3_http_list
    print(3333, ppts3_http_list)
    logging.info('--------------ppts3_http_list 写入字典完成-------------')
    ppts4_http_list = {}
    for c in ppts3_http_list:
        tmp_ppts4_http_list = {}
        for d in ppts3_http_list[c]:
            tmp_res4 = []
            for e in ppts3_http_list[c][d]:
                res4 = requests.post(url=e, headers=header, verify=False)
                res4.encoding = res4.apparent_encoding
                res4_html = res4.text
                soup4 = bs(res4_html, "html.parser")
                li_5 = soup4.find('ul', class_='downurllist')('li')
                # for m in li_5:
                #     tmp_res4.append(url + m.a['href'])
                tmp_res4.append(url + li_5[0].a['href'])
            tmp_ppts4_http_list[d] = tmp_res4
        ppts4_http_list[c] = tmp_ppts4_http_list
    print(44444, ppts4_http_list)
    logging.info('--------------ppts4_http_list 写入字典完成-------------')
    logging.info(f'ppts4_http_list字典：{ppts4_http_list}')
    try:
        write_file(str(ppts4_http_list))
    except OSError as reason:
        print(reason)
        logging.info(f'写入文件异常：{reason}')
    logging.info('--------------写入文件完成-------------')
    logging.info('--------------爬虫结束-------------')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("开始时间：", start_time)
    get_pages_down_zip()
    # write_file('111111111')
    stop_time = datetime.datetime.now()
    print("运行时间：", stop_time - start_time)
    logging.info(f'------------运行时间：{stop_time - start_time}-------------')







