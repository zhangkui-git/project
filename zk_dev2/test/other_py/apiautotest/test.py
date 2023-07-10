'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/5/20 18:25
software: PyCharm
'''
# import tkinter

# top = tkinter.Tk()
# # 进入消息循环
# # 创建两个列表
# li = ['C', 'python', 'php', 'html', 'SQL', 'java']
# movie = ['CSS', 'jQuery', 'Bootstrap']
# listb = tkinter.Listbox(top)  # 创建两个列表组件
# listb2 = tkinter.Listbox(top)
# for item in li:  # 第一个小部件插入数据
#     listb.insert(0, item)
#
# for item in movie:  # 第二个小部件插入数据
#     listb2.insert(0, item)
#
# listb.pack()  # 将小部件放置到主窗口中
# listb2.pack()
# top.mainloop()  # 进入消息循环
import socket
from tkinter import messagebox, RIGHT, LEFT, TOP, BOTTOM

#
# top = tkinter.Tk()
#
#
# def helloCallBack():
#     # tkMessageBox.showinfo("Hello Python", "Hello Runoob")
#     messagebox.showinfo("Hello Python", "Hello Runoob")
#
#
#
# B = tkinter.Button(top, text="点我", command=helloCallBack)
#
# B.pack()
# top.mainloop()

# top = tkinter.Tk()
# root = tkinter.Tk()
# # 创建一个Canvas，设置其背景色为白色
# cv = tkinter.Canvas(root, bg='white')
# # 创建一个矩形，坐标为(10,10,110,110)
# cv.create_rectangle(10, 10, 110, 110)
# cv.pack()
# root.mainloop()
# # 为明显起见，将背景色设置为白色，用以区别 root
# top.mainloop()

# top = tkinter.Tk()
# CheckVar1 = tkinter.IntVar()
# CheckVar2 = tkinter.IntVar()
# C1 = tkinter.Checkbutton(top, text="RUNOOB", variable=CheckVar1,
#                          onvalue=1, offvalue=0, height=5,
#                          width=20)
# C2 = tkinter.Checkbutton(top, text="GOOGLE", variable=CheckVar2,
#                          onvalue=1, offvalue=0, height=5,
#                          width=20)
# B = tkinter.Button(top, text="点我")
# #
# B.pack()
# C1.pack()
# C2.pack()
# top.mainloop()
# top = tkinter.Tk()
# L1 = tkinter.Label(top, text="网站名")
# L1.pack(side=LEFT)
# E1 = tkinter.Entry(top, bd=5)
# E1.pack(side=RIGHT)
#
# top.mainloop()

# def say_hi():
#     print("hello ~ !")
#
#
# root = tkinter.Tk()
#
# frame1 = tkinter.Frame(root)
# frame2 = tkinter.Frame(root)
# root.title("tkinter frame")
#
# label = tkinter.Label(frame1, text="Label", justify=LEFT)
# label.pack(side=LEFT)
#
# hi_there = tkinter.Button(frame2, text="say hi~", command=say_hi)
# hi_there.pack()
#
# frame1.pack(padx=1, pady=1)
# frame2.pack(padx=10, pady=10)
#
# root.mainloop()
# import requests
# import urllib3
# import tkinter
# from api.login_api import login_test
# from common.encry_decry import RsaEncrypt
# from config.config import host
# from data.common_data import admin, password
# from setting import DIR_NAME
#
#
# def user_created(ip, header, user_describ, name, pwd):
#     """
#     创建用户接口
#     header: 登录header
#     user_describ: 用户描述
#     name: 用户名
#     pwd: 密码
#     """
#     url = f"https://{ip}:8440" + '/userpermission/usermanage/addUser'
#     user = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(name)  # 加密后的用户名
#     pas = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(pwd)  # 加密后的密码
#     if user_describ == 'operator':  # 判断角色id值为2，用户描述为'operator'，值为3用户描述为'audit'
#         roleId = 2
#     elif user_describ == 'audit':
#         roleId = 3
#     else:
#         print('输入的roleId值错误')
#         raise Exception
#
#     json = {
#         "userName": user,
#         "userPassword": pas,
#         "roleId": roleId, "userDescription": user_describ}
#     resp = requests.post(url=url, json=json, headers=header, verify=False)
#     result = resp.json()
#     print(result)
#     assert result['message'] == '操作成功' or result['message'] == '用户名重复'  # 断言操作成功或用户名重复
#
#
# def add_all_user(ip, user_name):
#     try:
#         role_name = ['operator', 'audit']
#         urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 取消ssl安全提示
#         header = login_test(admin, password)  # admin登录返回header
#         user_list = []  # 所有用户列表
#         for role in role_name:  # 遍历角色
#             for user in user_name:  # 遍历测试组名字
#                 userName = '{}_{}'.format(role, user)  # 平台用户名 例如： operator_cyt
#                 user_created(ip=ip, header=header, user_describ=role, name=userName, pwd=password)
#                 user_list.append(userName)
#         print(user_list)  # 打印添加的用户名
#         result = user_list
#         return result
#     except:
#         result = '输入有误'
#         return result
#
#
# def f1():
#     ip, user = show()
#     if ',' in user:
#         username = user.split(',')
#     elif '，' in user:
#         username = user.split('，')
#     else:
#         username = [user]
#     result = add_all_user(ip, username)
#     if result !='输入有误':
#         tkinter.messagebox.showinfo(message=f'添加{result}成功')
#     else:
#         tkinter.messagebox.showwarning(message='请检查ip或者用户名是否正确')
# def show():
#     output1 = E1.get()
#     output2 = E2.get()
#     print(output1, output2)
#     return output1, output2
#
#
# top = tkinter.Tk()
# top.title('创建用户')
# top.geometry('300x200')
# L1 = tkinter.Label(top, text="*i p:")
# L1.place(x=50, y=40, anchor='nw')
# # L1.pack()
#
# E1 = tkinter.Entry(top, bd=5)
# E1.place(x=90, y=40)
# # E1.pack()
#
# L2 = tkinter.Label(top, text="*用户:", height=0)
# # L2.pack()
# L2.place(x=50, y=80)
# E2 = tkinter.Entry(top, bd=5)
# E2.place(x=90, y=80)
# # E2.pack()
# tip = tkinter.Label(top, text='(格式：xxx或者xxx,xxx)', height=0)
# tip.place(x=50, y=110)
# # tip.pack()
# b1 = tkinter.Button(top, text='设置', command=f1)
# b1.place(x=150, y=150)
# # b1.pack()
#
# top.mainloop()

# def go():
#     print(entry1.get())
#
#
# root = tkinter.Tk()
# entry1 = tkinter.Entry(root, width=50)
# b = tkinter.Button(root, text='click', command=go)
# b.pack()
# entry1.pack()
#
# root.mainloop()
# import tkinter
# from tkinter import ttk
# import time
# import json
# import requests
# import urllib
# import random
# import re
# from bs4 import BeautifulSoup
# import urllib3
#
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# import os
# import sys
# import xlwt
#
# db_book_le = []
# db_film_le = []
# db_music_le = []
# db_game_le = []
# baidu_le = []
# flag = 0
#
# win = tkinter.Tk()
# win.title("智能提取")
# win.geometry("1200x800")
# t1 = tkinter.Text(win, width=35, height=2, font=("隶书", 18))
# t1.place(x=50, y=80, anchor='nw')
# t1.insert("insert", "人工智能")
#
# t2 = tkinter.Text(win, width=2, height=1, font=("隶书", 18))
# t2.place(x=160, y=160, anchor='nw')
# t2.insert("insert", 3)
#
# w1 = tkinter.Label(win, text="关键字输入：", font=("隶书", 20), fg="green")
# w1.place(x=50, y=40, anchor='nw')
# w2 = tkinter.Label(win, text="生成地址：", font=("隶书", 20), fg="green")
# w2.place(x=570, y=20, anchor='nw')
# w3 = tkinter.Label(win, text="查阅页数：", font=("隶书", 16), fg="green")
# w3.place(x=50, y=160, anchor='nw')
# w4 = tkinter.Label(win, text="是否用百度搜索：", font=("隶书", 20), fg="blue")
# w4.place(x=50, y=220, anchor='nw')
#
# tree_date = ttk.Treeview(win, height=32, columns=('name', 'url'))
# # tree_date['columns'] = ['name','url']
# tree_date.heading('name', text='title')
# tree_date.heading('url', text='url')
# tree_date.column("#0", width=40, anchor="center")
# tree_date.column('name', width=200)
# tree_date.column('url', width=380)
# tree_date.place(x=570, y=60)
#
# group = tkinter.LabelFrame(win, text='豆瓣网', font=("隶书", 18), labelanchor='n', padx=5, pady=5)
# group.place(x=50, y=400, anchor='nw')
#
# LANGS = [('书籍', 1), ('电影', 2), ('音乐', 3), ('游戏', 4)]
# v1 = tkinter.IntVar()
# v1.set(1)
# for lang, num in LANGS:
#     b = tkinter.Radiobutton(group, text=lang, font=("隶书", 18), variable=v1, value=num, padx=0, pady=0)
#     b.pack(fill='y', side='left', padx=20, pady=20)
#
#
# def db_book(key_word, num):
#     url = 'https://www.douban.com/j/search?q={}&start={}&cat=1001'.format(key_word, num)
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
#     }
#     res = requests.get(url, headers=headers, verify=False)
#     print(res.status_code)
#     if res.status_code == 200:
#         r = res.text
#         r = json.loads(r)
#         items = r['items']
#         print(len(items))
#         for item in items:
#             soup = BeautifulSoup(item, "lxml")
#             t = soup.find_all(class_='nbg')
#             # print(type(t))
#             for ul in t:
#                 url = ul.attrs['href'].strip()
#                 title = ul.attrs['title'].strip()
#                 if url:
#                     print(title, '3333')
#                     # tree_date.insert('',i,text=i,values=(title,url))
#                     # time.sleep(0.1)
#                     dic = {'title': title, 'url': url}
#                     db_book_le.append(dic)
#                 print(db_book_le)
#
#
# def f11(key_word, num):
#     if key_word:
#         for i in range(num):
#             num = i * 20
#             try:
#                 db_book(key_word, num)
#             # time.sleep(1)
#             except:
#                 break
#     print(len(db_book_le), '777')
#
#     i = 0
#     for book in db_book_le:
#         i += 1
#         if i < len(db_book_le) + 1:
#             tree_date.insert('', i, text=i, values=(book['title'], book['url']))
#         else:
#             break
#
#
# def db_film(key_word, num):
#     url = 'https://www.douban.com/j/search?q={}&start={}&cat=1002'.format(key_word, num)
#
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
#     }
#     res = requests.get(url, headers=headers, verify=False)
#     print(res.status_code)
#     if res.status_code == 200:
#         r = res.text
#         r = json.loads(r)
#         items = r['items']
#         print(len(items))
#         for item in items:
#             soup = BeautifulSoup(item, "lxml")
#             t = soup.find_all(class_='nbg')
#             # print(type(t))
#             for ul in t:
#                 url = ul.attrs['href'].strip()
#                 title = ul.attrs['title'].strip()
#                 if url:
#                     print(title, '3333')
#                     # tree_date.insert('',i,text=i,values=(title,url))
#                     # time.sleep(0.1)
#                     dic = {'title': title, 'url': url}
#                     db_film_le.append(dic)
#                 print(db_film_le)
#
#
# db_film_le = []
#
#
# def f12(key_word, num):
#     if key_word:
#         for i in range(num):
#             num = i * 20
#             try:
#                 db_film(key_word, num)
#             # time.sleep(1)
#             except:
#                 break
#     print(len(db_film_le), '777')
#
#     i = 0
#     for book in db_film_le:
#         i += 1
#         if i < len(db_film_le) + 1:
#             tree_date.insert('', i, text=i, values=(book['title'], book['url']))
#         else:
#             break
#
#
# def db_music(key_word, num):
#     url = 'https://www.douban.com/j/search?q={}&start={}&cat=1003'.format(key_word, num)
#
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
#     }
#     res = requests.get(url, headers=headers, verify=False)
#     print(res.status_code)
#     if res.status_code == 200:
#         r = res.text
#         r = json.loads(r)
#         items = r['items']
#         print(len(items))
#         for item in items:
#             soup = BeautifulSoup(item, "lxml")
#             t = soup.find_all(class_='nbg')
#             # print(type(t))
#             for ul in t:
#                 url = ul.attrs['href'].strip()
#                 title = ul.attrs['title'].strip()
#                 if url:
#                     print(title, '3333')
#                     # tree_date.insert('',i,text=i,values=(title,url))
#                     # time.sleep(0.1)
#                     dic = {'title': title, 'url': url}
#                     db_music_le.append(dic)
#                 print(db_music_le)
#
#
# def f13(key_word, num):
#     if key_word:
#         for i in range(num):
#             num = i * 20
#             try:
#                 db_music(key_word, num)
#             # time.sleep(1)
#             except:
#                 break
#     print(len(db_music_le), '777')
#
#     i = 0
#     for book in db_music_le:
#         i += 1
#         if i < len(db_music_le) + 1:
#             tree_date.insert('', i, text=i, values=(book['title'], book['url']))
#         else:
#             break
#
#
# def db_game(key_word):
#     url = 'https://www.douban.com/search?cat=3114&q={}'.format(key_word)
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
#     }
#     res = requests.get(url, headers=headers, verify=False)
#     print(res.status_code)
#     if res.status_code == 200:
#         r = res.text
#         soup = BeautifulSoup(r, "lxml")
#         t = soup.find_all(class_='nbg')
#         print(type(t))
#         for ul in t:
#             url = ul.attrs['href'].strip()
#             title = ul.attrs['title'].strip()
#             if url:
#                 print(title, '3333')
#                 # tree_date.insert('',i,text=i,values=(title,url))
#                 # time.sleep(0.1)
#                 dic = {'title': title, 'url': url}
#                 db_game_le.append(dic)
#             print(db_game_le)
#
#
# def f14(key_word, num):
#     if key_word:
#         for i in range(num):
#             num = i * 20
#             try:
#                 db_game(key_word)
#             # time.sleep(1)
#             except:
#                 break
#     print(len(db_game_le), '777')
#
#     i = 0
#     for book in db_game_le:
#         i += 1
#         if i < len(db_game_le) + 1:
#             tree_date.insert('', i, text=i, values=(book['title'], book['url']))
#         else:
#             break
#
#
# def f1():
#     global flag
#     flag = 0
#     if v1.get() == 1:
#         x = tree_date.get_children()
#         for item in x:
#             tree_date.delete(item)
#         key_word = t1.get('0.0', 'end').strip()
#         num = int(t2.get('0.0', 'end').strip())
#         global db_book_le
#         if len(db_book_le) > 0:
#             db_book_le = []
#         f11(key_word, num)
#     elif v1.get() == 2:
#         x = tree_date.get_children()
#         for item in x:
#             tree_date.delete(item)
#         key_word = t1.get('0.0', 'end').strip()
#         num = int(t2.get('0.0', 'end').strip())
#         global db_film_le
#         if len(db_film_le) > 0:
#             db_film_le = []
#         f12(key_word, num)
#     elif v1.get() == 3:
#         x = tree_date.get_children()
#         for item in x:
#             tree_date.delete(item)
#         key_word = t1.get('0.0', 'end').strip()
#         num = int(t2.get('0.0', 'end').strip())
#         global db_music_le
#         if len(db_music_le) > 0:
#             db_music_le = []
#         f13(key_word, num)
#     elif v1.get() == 4:
#         x = tree_date.get_children()
#         for item in x:
#             tree_date.delete(item)
#         key_word = t1.get('0.0', 'end').strip()
#         num = int(t2.get('0.0', 'end').strip())
#         global db_game_le
#         if len(db_game_le) > 0:
#             db_game_le = []
#         f14(key_word, 1)
#
#
# def f2():
#     if v1.get() == 1 and flag == 0:
#         if len(db_book_le) > 0:
#             book1 = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
#             sheet1 = book1.add_sheet(u'Sheet1', cell_overwrite_ok=True)  # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
#
#             sheet1.write(0, 0, '序号')  # 第0行第0列
#             sheet1.write(0, 1, 'title')  # 第0行第1列
#             sheet1.write(0, 2, 'url')  # 第0行第2列
#             s = 0
#             for book in db_book_le:
#                 s += 1
#                 sheet1.write(s, 0, s)  # 第s行第0列
#                 sheet1.write(s, 1, book['title'])  # 第s行第1列
#                 sheet1.write(s, 2, book['url'])  # 第s行第2列
#             # path = os.path.dirname(os.path.abspath(__file__))
#             name = t1.get('0.0', 'end').strip()
#             num = t2.get('0.0', 'end').strip()
#             path = os.path.abspath(os.path.dirname(sys.argv[0]))  # 当前文件夹
#             book1.save(path + '{}豆瓣book前{}页.xls'.format(name, num))
#     elif v1.get() == 2 and flag == 0:
#         if len(db_film_le) > 0:
#             book1 = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
#             sheet1 = book1.add_sheet(u'Sheet1', cell_overwrite_ok=True)  # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
#
#             sheet1.write(0, 0, '序号')  # 第0行第0列
#             sheet1.write(0, 1, 'title')  # 第0行第1列
#             sheet1.write(0, 2, 'url')  # 第0行第2列
#             s = 0
#             for book in db_film_le:
#                 s += 1
#                 sheet1.write(s, 0, s)  # 第s行第0列
#                 sheet1.write(s, 1, book['title'])  # 第s行第1列
#                 sheet1.write(s, 2, book['url'])  # 第s行第2列
#             name = t1.get('0.0', 'end').strip()
#             num = t2.get('0.0', 'end').strip()
#             path = os.path.abspath(os.path.dirname(sys.argv[0]))  # 当前文件夹
#             book1.save(path + '{}豆瓣film前{}页.xls'.format(name, num))
#     elif v1.get() == 3 and flag == 0:
#         # db_db_music_le
#         if len(db_music_le) > 0:
#             book1 = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
#             sheet1 = book1.add_sheet(u'Sheet1', cell_overwrite_ok=True)  # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
#
#             sheet1.write(0, 0, '序号')  # 第0行第0列
#             sheet1.write(0, 1, 'title')  # 第0行第1列
#             sheet1.write(0, 2, 'url')  # 第0行第2列
#             s = 0
#             for book in db_music_le:
#                 s += 1
#                 sheet1.write(s, 0, s)  # 第s行第0列
#                 sheet1.write(s, 1, book['title'])  # 第s行第1列
#                 sheet1.write(s, 2, book['url'])  # 第s行第2列
#             name = t1.get('0.0', 'end').strip()
#             num = t2.get('0.0', 'end').strip()
#             path = os.path.abspath(os.path.dirname(sys.argv[0]))  # 当前文件夹
#             book1.save(path + '{}豆瓣music前{}页.xls'.format(name, num))
#     elif v1.get() == 4 and flag == 0:
#         # db_db_game_le
#         if len(db_game_le) > 0:
#             book1 = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
#             sheet1 = book1.add_sheet(u'Sheet1', cell_overwrite_ok=True)  # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
#
#             sheet1.write(0, 0, '序号')  # 第0行第0列
#             sheet1.write(0, 1, 'title')  # 第0行第1列
#             sheet1.write(0, 2, 'url')  # 第0行第2列
#             s = 0
#             for book in db_game_le:
#                 s += 1
#                 sheet1.write(s, 0, s)  # 第s行第0列
#                 sheet1.write(s, 1, book['title'])  # 第s行第1列
#                 sheet1.write(s, 2, book['url'])  # 第s行第2列
#             name = t1.get('0.0', 'end').strip()
#             num = t2.get('0.0', 'end').strip()
#             path = os.path.abspath(os.path.dirname(sys.argv[0]))  # 当前文件夹
#             book1.save(path + '{}豆瓣game前{}页.xls'.format(name, num))
#     elif flag == 1:
#         if len(baidu_le) > 0:
#             book1 = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
#             sheet1 = book1.add_sheet(u'Sheet1', cell_overwrite_ok=True)  # 创建sheet，Sheet1为表的名字，cell_overwrite_ok为是否覆盖单元格
#
#             sheet1.write(0, 0, '序号')  # 第0行第0列
#             sheet1.write(0, 1, 'title')  # 第0行第1列
#             sheet1.write(0, 2, 'url')  # 第0行第2列
#             s = 0
#             for book in baidu_le:
#                 s += 1
#                 sheet1.write(s, 0, s)  # 第s行第0列
#                 sheet1.write(s, 1, book['title'])  # 第s行第1列
#                 sheet1.write(s, 2, book['url'])  # 第s行第2列
#             name = t1.get('0.0', 'end').strip()
#             num = t2.get('0.0', 'end').strip()
#             path = os.path.abspath(os.path.dirname(sys.argv[0]))  # 当前文件夹
#             book1.save(path + '{}百度前{}页.xls'.format(name, num))
#
#
# def f3():
#     t1.delete('1.0', 'end')
#     x = tree_date.get_children()
#     for item in x:
#         tree_date.delete(item)
#
#
# def baidu(key_word, num):
#     url = 'https://www.baidu.com/s?wd={}&pn={}'.format(key_word, num)
#
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Host': 'www.baidu.com',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'none',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#         'Cookie': 'BIDUPSID=ECC8764E5930648D9EE7445D0B577857; PSTM=1570677970; BAIDUID=94F743F08B49ADF3CF4D398C22C5DFE8:SL=0:NR=10:FG=1; ORIGIN=0; bdime=0; sug=0; sugstore=1; BD_UPN=12314353; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; H_PS_PSSID=1431_21107_30824_26350_30717; delPer=0; BD_CK_SAM=1; PSINO=1; shifen[71452001866_10703]=1583138129; BCLID=10943101803183982058; BDSFRCVID=DK4OJeC627aZJgTuVLvJMBPFNmHbOOcTH6ao6xpSElEcKui1x_vjEG0PDf8g0Ku-S2EqogKKQeOTHZ_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRAOoC8atDvHjjrP-trf5DCShUFs0UPJB2Q-5KL-JbjAOR325qjd5xIILR3lWtr7KeO93MbdJJjoM4nx0UoSQttU5fuDhpRq2eTxoUJg5DnJhhvGqq-KQJ_ebPRiQ4Q9QgbzMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHj_aej5B3J; __yjsv5_shitong=1.0_7_5a018d568558427ed363241e4b3f88e3b211_300_1583138131526_117.136.3.185_0d95aab2; COOKIE_SESSION=19_0_4_9_0_11_0_3_2_6_9_7_0_0_0_0_0_0_1583140097%7C9%23435658_49_1583114491%7C9; H_PS_645EC=2fdf7QnmS4e%2BNBcWTXMe0VGifR872HzNWBC6bFZM%2FgwGxp6M%2F6HVGz9VqEI'
#     }
#     res = requests.get(url, headers=headers, verify=False)
#     if res.status_code == 200:
#         r = res.text
#         for i in range(num, num + 10):
#             i += 1
#             try:
#                 soup = BeautifulSoup(r, "lxml")
#                 t = soup.find_all(id=str(i))
#                 q = t[0].find_all(name="a")
#                 title = q[0].get_text()
#                 url = q[0].attrs['href'].strip()
#                 print(title, url)
#                 dic = {'title': title, 'url': url}
#                 baidu_le.append(dic)
#             except:
#                 pass
#
#
# def f41(key_word, num):
#     if key_word:
#         for i in range(num):
#             num = i * 10
#             try:
#                 baidu(key_word, num)
#             # time.sleep(1)
#             except:
#                 break
#     print(len(baidu_le), '777')
#     i = 0
#     for book in baidu_le:
#         i += 1
#         if i < len(baidu_le) + 1:
#             tree_date.insert('', i, text=i, values=(book['title'], book['url']))
#         else:
#             break
#
#
# def f4():
#     global flag
#     flag = 1
#     x = tree_date.get_children()
#     for item in x:
#         tree_date.delete(item)
#     key_word = t1.get('0.0', 'end').strip()
#     num = int(t2.get('0.0', 'end').strip())
#     global baidu_le
#     if len(baidu_le) > 0:
#         baidu_le = []
#     f41(key_word, num)
#
#
# button1 = tkinter.Button(win, text="生成地址", font=("隶书", 15), command=f1, width=15, height=3, fg="green")
# button1.place(x=100, y=650, anchor='nw')
# button2 = tkinter.Button(win, text="导出生成Excel", font=("隶书", 15), command=f2, width=15, height=3, fg="green")
# button2.place(x=325, y=650, anchor='nw')
# button3 = tkinter.Button(win, text="清空", font=("隶书", 15), command=f3, width=4, height=2, fg="red")
# button3.place(x=480, y=78, anchor='nw')
# button4 = tkinter.Button(win, text="是", font=("隶书", 15), command=f4, width=4, height=2, fg="red")
# button4.place(x=480, y=208, anchor='nw')
# win.mainloop()

