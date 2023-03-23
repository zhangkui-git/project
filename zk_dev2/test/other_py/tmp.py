# import os
# local_dir = os.getcwd()
#
#
# def write_file():
#     # file1 = fr"{local_dir}\1.bat"
#     file1 = fr"{local_dir}\1.sql"
#     # file2 = fr"{local_dir}\2.bat"
#     # comand1 = f"net user test{n} Admin@123 /add"
#     myfile1 = open(file1, "w")
#     n = 51
#     while n <= 150:
#         comand1 = f"INSERT INTO soms.soms_asset_user_pwd (id, asset_id, username, password, create_time, update_time, protocol) VALUES({n}, 1, 'test{n}', '6933921fa54e5ef3b5be8ccb015329b3', '2023-02-21 09:58:41', '2023-02-21 09:58:41', 'RDP');\n"
#         myfile1.write(comand1)
#         n += 1
#     # comand2 = f"net group Administrators test{n} /add"
#     # print(file)
#     # 使用密码需要根据执行主机的系统编码，否则无法终端执行bat文件，dos窗口：chcp，活动代码936 代表GBK编码
#     # myfile = open(file, "w", encoding="utf-8")
#     # myfile2 = open(file2, "w")
#     # myfile2.write(comand2)
#     myfile1.close()
#     # myfile2.close()
#
#
# if __name__ == '__main__':
#     write_file

# import requests
# res = requests.post('https://www.cnblogs.com/zhengyihan1216/p/11549820.html', verify=False)
# # res.encoding = res.apparent_encoding
# print(res.content.decode('utf-8'))
# print(res.text)


from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
import time
import re
import gzip
import urllib.request
from bs4 import BeautifulSoup
from io import StringIO, BytesIO
from lxml import etree
import os

ua = UserAgent()
# header = {'User-Agent': f'{ua.chrome}', 'Cookie': 'acw_tc=2760779916794751608163076ee5aaa98ebf6109750844345fa69a1bd55895; acw_sc__v2=641ac1d86ef74858c95d120d4bd93e8839074eae'}
header = {'User-Agent': f'{ua.firefox}'}
url = 'https://www.1ppt.com/plus/download.php?open=0&aid=103166&cid=3'
# url = 'http://www.1ppt.com/article/103166.html'
res = requests.post(url=url, headers=header, verify=False)
# res = requests.post(url=url, headers=header)
res.encoding = res.apparent_encoding
r_html = res.text
# r_html = gzip.decompress(bytes(r_html)).decode('utf-8')
# soup5 = bs(r_html, "html.parser")
# soup5 = bs(r_html, 'lxml')
print(r_html)


# url1 = 'https://ppt.1ppt.com/uploads/soft/1907/1-1ZGR05445.zip'
# header = {'User-Agent': f'{ua.firefox}'}
#
#
# def downloadfile(url, filename=None):
#   if(not filename):                         # 如果参数没有指定文件名
#     filename = os.path.basename(url)          # 取用url的尾巴为文件名
#   leng = 1
#   while(leng==1):
#     torrent = requests.get(url, headers=header)
#     leng = len(list(torrent.iter_content(1024)))  # 下载区块数
#     if(leng == 1):                                # 如果是1 就是空文件 重新下载
#       print(filename,'下载失败,重新下载')
#       time.sleep(1)
#     else:
#       print('下载完成')
#   with open(filename, 'wb') as f:
#     for chunk in torrent.iter_content(1024):    # 防止文件过大，以1024为单位一段段写入
#       f.write(chunk)
#
#
# if __name__ == '__main__':
#     downloadfile(url1)



















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

