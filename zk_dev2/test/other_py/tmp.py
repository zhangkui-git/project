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

from io import StringIO
import gzip


ua = UserAgent()
header = {'User-Agent': f'{ua.chrome}'}
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
url = 'http://www.1ppt.com/plus/download.php?open=0&aid=103166&cid=3'

res = requests.get(url=url, headers=header)
res.encoding = res.apparent_encoding
r_html = res.text
soup5 = bs(r_html, "html.parser")
# print(res.status_code)
# print(r_html)




response1 = urllib.request.urlopen(url=url)
# print(response1.info().get('Content-Encoding'))
# print(response1.read())
# if response1.info().get('Content-Encoding') == 'gzip':
#     buf = StringIO(response1.read())
#     f = gzip.GzipFile(fileobj=buf)
#     data = f.read()
#     print(data)
#     # 处理
#     f.close()
# else:
#     data = response1.read()


# urlopen()向URL发请求,返回响应对象
response = urllib.request.urlopen('http://www.baidu.com/')
# 提取响应内容
html = response.read().decode('utf-8')
# 打印响应内容
# print(html)

a = {'b': 'zhang'}
print(str(a))

