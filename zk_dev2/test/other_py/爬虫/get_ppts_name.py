import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import requests
import os

url = 'http://www.1ppt.com'
ua = UserAgent()
header = {'User-Agent': f'{ua.chrome}'}


# 获取PPT类目栏前7个列表、ppt列表获取ppt类型
def get_ppts():
    count = 1
    ppts_http_list = {}
    # print(header)
    res = requests.post(url=url, headers=header)
    res.encoding = res.apparent_encoding
    res_html = res.text
    soup = bs(res_html, "html.parser")
    li_1 = soup.find("div", id='navMenu')
    li1_list = li_1.find_all('li')
    for li in li1_list:
        if count <= 7:
            # print(url + li.a['href'], li.a['href'], li.a.string)
            # print(url + li.a['href'], "    ", li.a.string)
            ppts_http_list[li.a.string] = url + li.a['href']
        count += 1
    # ppt类型列表
    print(ppts_http_list)
    # 开始获取ppt列表中的ppt类型
    ppts1_http_list = {}
    for i in ppts_http_list:
        # print(i, ppts_http_list[i])
        res1 = requests.post(url=ppts_http_list[i], headers=header)
        res1.encoding = res1.apparent_encoding
        res1_html = res1.text
        soup1 = bs(res1_html, "html.parser")
        li_2 = soup1.find('div', class_='col_nav clearfix')
        li2_list = li_2.find_all('li')[1:]
        tmp_ppts1_http_list = {}
        for f in li2_list:
            tmp_ppts1_http_list[f.a.string] = url + f.a['href']
        ppts1_http_list[i] = tmp_ppts1_http_list
    print(ppts1_http_list)

    for h in ppts1_http_list:
        for k in h:
            res2 = requests.post(url=ppts_http_list[i], headers=header)
            res2.encoding = res2.apparent_encoding
            res2_html = res2.text
            print(res2_html)
            time.sleep(600)
    # ppts2_http_list = {}
    # for h in ppts1_http_list:
    #     print(h)
    #     for j in ppts1_http_list[h]:
    #         res2 = requests.post(url=j, headers=header)
    #         res2.encoding = res2.apparent_encoding
    #         res2_html = res2.text
    #         soup2 = bs(res2_html, 'html.parser')
    #         li_3 = soup2.find('ul', class_='tplist')
    #         li3_list = li_3.find_all('li')
    #         tmp2_res = []
    #         for k in li3_list:
    #             tmp2_res.append(url + k.a['href'])
    #         ppts2_http_list[h] = tmp2_res
    # print(ppts2_http_list)













if __name__ == '__main__':
    get_ppts()









