import time

from bs4 import BeautifulSoup
import requests

# BeautifulSoup、 lxml写成html.parser也可以，同样的效果，都是解析器

# html = """<html><head><title>The Dormouse's story</title></head><body><p class="title" name="dromouse"><b>The Dormouse'
# s story</b></p><p class="story">Once upon a time there were three little sisters; and their names were<a href="http
# ://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,<a href="http://example.com/lacie" class="sister"
# id="link2">Lacie</a> and<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the
# bottom of a well.</p><p class="story">...</p>"""
#
# # lxml写成html.parser也可以，同样的效果，都是解析器
# soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())
# print("#"*30)
# # print(soup.head.title.string)
# print(soup.title.string)


# 爬取网站学习文章的url梳理
# url = "http://www.crazyant.net"
# header = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
# }
# r = requests.get(url, headers=header)
# if r.status_code != 200:
#     raise Exception
# html_doc = r.text
# soup = BeautifulSoup(html_doc, "html.parser")
# h2_nodes=soup.find_all("h2", class_="entry-title")
# # h2_nodes = soup.find_all("span", class_="cat-links")
# for h2_node in h2_nodes:
#     link = h2_node.find("a")
#     print(link["href"], link.get_text())


# 爬取三国演义小说
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
page_text = requests.get(url=url, headers=headers).content.decode("utf-8")
soup = BeautifulSoup(page_text, 'html.parser')
li_list = soup.select('.book-mulu > ul > li')
# fp = open('./三国演义小说.txt', 'w', encoding='utf-8')
print(li_list)


# for li in li_list:
#     title = li.a.string
#     detail_url = 'https://www.shicimingju.com' + li.a['href']
#     print(detail_url)
#     detail_page_text = requests.get(url=detail_url, headers=headers).content.decode("utf-8")
#     detail_soup = BeautifulSoup(detail_page_text, 'html.parser')
#     div_tag = detail_soup.find('div', class_='chapter_content')
#     content = div_tag.text
#     # time.sleep(60)
#     fp.write('\n' + title + ':' + '\n' + content + '\n\n')
#     print(title, '爬取成功')


