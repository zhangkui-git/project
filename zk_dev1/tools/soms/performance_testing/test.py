'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/1/7 15:33
software: PyCharm
'''
# str = '54.99% 17.10GB/31.09GB'
# print(str.split(' '))
# coding:UTF-8登录后复制
# from scapy.all import*
# import time
# class PcapDecode:
#     def __init__(self):
#         #ETHER：读取以太网层协议配置文件
#         with open('./protocol/ETHER','r',encoding='UTF-8')as f:
#             ethers=f.readlines()
#
#         self.ETHER_DICT=dict()
#         for ether in ethers:
#         ether = ether.strip().strip('\n').strip（'\r）.strip（'\r\n'）
#         self.ETHER_DICT[int（ether.split（'："）[0]）]=ether.split（'：）[1]#将配置文件中的信息（0257：Experi
#         #IP：读取IP层协议配置文件
#         with open（./protocol/IP"，'r'，encoding='UTF-8'）as f：ips=f.readlines（）
#         self.IP_DICT=dict（）
#         for ip in ips：ip=ip.strip（）.strip（"\n'）.strip（'\r"）.strip（'\r\n'）
#         self.IP_DICT[int（ip.split（："）[e]）]=ip.split（'：）[1]#将配置文件中的信息（41：IPV6）存入dic
#         #PORT：读取应用层协议端口配置文件
#         with open（./protocol/PORT'，'r'，encoding='UTF-8'）as f：ports=f.readlines（）
#         seLf.PORT_DICT=dict（）
#         for port in ports：port=port.strip（）.strip（'\n）.strip（"\r"）.strip（'\r\n'）
#         seLf.PORT_DICT[int（port.split（"："）[e]）]=port.split（'："）[1]#如：21：FTP
#         #TCP：读取TCP层协议配置文件
#         with open（./protocol/TCP'，'r'，encoding='UTF-8'）as f：tcps=f.readlines（）
#         seLf.TCP_DICT=dict（）
#         for tcp in tcps：tcp=tcp.strip（）.strip（'\n"）.strip（'\r）.strip（"\r\n'）
#         self.TCP_DICT[int（tcp.split（"："）[0]）1=tcp.split（'：）[1]#465：SMTPS
import base64
import datetime
import ipaddress
import os
import threading
import time

import pytesseract
from PIL import Image
from scapy.sendrecv import sniff

# from setting import DIR_NAME
#
# # with open(DIR_NAME+"\\config\\capture_file_eth0_20220108115744.pcap", 'r', encoding='UTF-8')as f:
# #     line = f.readlines()
# #     print(line)
# from scapy.all import *
# pkts = rdpcap(DIR_NAME+"\\config\\capture_file_eth0_20220108115744.pcap")
# # print(pkts)
# print(pkts[0], type(pkts[0]))
# # for item in pkts:
# #     print(item, type(item))
# #     print(item.time)
# #     print(item.fields)
# #     print(item.overload_fields)
# #     print(item.payload)
# #     print(item.wirelen)
# pcap = sniff(offline=DIR_NAME+"\\config\\capture_file_eth0_20220108115744.pcap")
# pcap[0].show()
# print(type(str(pcap[0].show())))
# s = '192.168.100.71' in str(pcap[0].show())
# print(s)
# pcap_str = bytes(raw(pcap[0]))
# print(pcap_str, type(pcap_str))
# ss = pcap_str.decode('utf-8')
# print(ss)

# print(int(ipaddress.ip_address(pkts[0].fields['dst'])))
# # print(pkts[0].decode(encoding='UTF-8'))
# print(pkts[0].encode(encoding='UTF-8'))

# s =b'<\xec\xef /rh\x91\xd0\xd1\t/\x08\x00E\x00\x00\xb9\xa6t\x00\x00\x7f\x11\xaaz\xc0\xa8\x04\xad'
# sss = s.decode('raw_unicode_escape')
# ss=sss.decode(encoding='utf-8')
#
# print(ss)
# print(type(ss))
# def decode(base64str):
#
#     tmp = base64.b64decode(base64str)
#     print(tmp)
#     return bytearray([(b<<1&255)|(b>>7) for b in tmp]).decode("utf-8")
#
# s = 'CwKMQChO9vIAYw=='
# str = decode('sLBzS1h0309zR9IxMQ==')
# print(str)
# print(str.encode('utf-8'))
from selenium import webdriver
from selenium.webdriver.common.by import By

from setting import DIR_NAME


def search(somsname, num):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://192.168.100.248:8440')
    time.sleep(1)
    driver.find_element(By.ID, value='details-button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, value='//*[@id="final-paragraph"]/a').click()
    time.sleep(1)
    driver.find_element(By.NAME, value='userName').send_keys(somsname)
    driver.find_element(By.NAME, value='password').send_keys('Admin@123456')  # 堡垒机用户密码
    time.sleep(0.5)
    driver.find_element(By.XPATH, value='//*[@class="el-button el-button--primary"]/span').click()
    time.sleep(1)
    driver.find_element(By.XPATH, value='(//*[@class="el-menu-item submenu-title-noDropdown"])[2]').click()
    time.sleep(2)
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    time.sleep(1)
    # driver.find_element(By.XPATH, value='(//*[@class="el-tree-node__children"])[2]/div[2]').click() # 可运维资产2
    count = 1  # 截图次数
    success_num = 0  # 成功数量
    failed_num = 0  # 失败数量
    while True:
        for i in range(10):
            driver.find_element(By.XPATH,
                                value='(//*[@class="el-tree-node__children"])[2]/div/div[2]/div[2]/div[1]').click()  # 可运维资产2
            time.sleep(1)
            driver.find_element(By.XPATH, value='//*[@class="el-radio-group"]/label[2]/span').click()  # 手动登录
            time.sleep(1)
            driver.find_element(By.XPATH, value='(//*[@class="el-input__inner"])[last()-3]').send_keys(f'test{num}{i}')
            time.sleep(1)
            driver.find_element(By.XPATH, value='(//*[@class="el-input__inner"])[last()-2]').send_keys(
                'Admin@123')  # rdp用户密码
            time.sleep(1)
            driver.find_element(By.XPATH, value='(//*[@class="el-form-item__content"])[last()]/button[2]').click()
            time.sleep(2)
        for i in range(15):
            page_total = driver.find_elements(By.XPATH, value=f'(//*[@class= "el-tabs__nav-scroll"]/div/div/span)')
            # print(len(page_total))    # 窗口数量
            driver.find_element(By.XPATH, value=f'(//*[@class="el-tabs__nav is-top"]/div)[1]').click()
            time.sleep(1)
            # 截图操作
            driver.get_screenshot_as_file(f'video/test{num}/{i}-{count}.png')  # 截图
            time.sleep(1)
            # 截取时间图像
            img = Image.open(r'{}\\video/test{}/{}-{}.png'.format(DIR_NAME, num, i, count))
            pic_img = img.crop((1300, 100, 1700, 185))
            pic_img.save(r'{}\\video/test{}/{}-{}-small.png'.format(DIR_NAME, num, i, count))  # 保存小图
            # 识别图片
            im = Image.open(DIR_NAME + '\\video/test{}/{}-{}-small.png'.format(num, i, count))
            text = pytesseract.image_to_string(im, config='--psm 6')
            print(text)  # 打印
            if text != '':
                success_num += 1
            else:
                failed_num += 1
            if count > 1:
                os.remove(DIR_NAME + '\\video/test{}/{}-{}.png'.format(num, i, count))
            os.remove(DIR_NAME + '\\video/test{}/{}-{}-small.png'.format(num, i, count))
            driver.find_element(By.XPATH, value=f'(//*[@class= "el-tabs__nav-scroll"]/div/div/span)[1]').click()  # 关闭窗口
            time.sleep(1)
            if len(page_total) == 1:
                break
        count += 1
        print(f'thread{somsname[-1:]}成功数量：{success_num}')
        print(f'thread{somsname[-1:]}失败数量：{failed_num}')
    # while True:
    #     pass

    # number = 1  # 数量
    # while True:
    #     '''
    #     num(堡垒机账户)
    #     c （rdp桌面用户)
    #     number 堡垒机账户-rdp桌面用户-number（截图数量）
    #     '''
    #     for count in range(10):  # 点击rdp用户窗口
    #         c = count + 1
    #         driver.find_element(By.XPATH, value=f'(//*[@class="el-tabs__nav is-top"]/div)[{c}]').click()  # 轮流切换窗口
    #         # time.sleep(60)
    #         time.sleep(2)  # 调试
    #         driver.get_screenshot_as_file(f'video/test{num}/{num}-{c}-{number}.png')  # 截图
    #         time.sleep(1)
    #         try:
    #             # 截取时间图像
    #             img = Image.open(r'{}\\video\\test{}\\{}-{}-{}.png'.format(DIR_NAME, num, num, c, number))
    #             pic_img = img.crop((1300, 100, 1700, 185))
    #             pic_img.save(r'{}\\video\\test{}\\{}-{}-{}-small.png'.format(DIR_NAME, num, num, c, number))  # 保存小图
    #             # 识别图片neir
    #             im = Image.open(DIR_NAME + '\\video\\test{}\\{}-{}-{}-small.png'.format(num, num, c, number))
    #             text = pytesseract.image_to_string(im, config='--psm 6')
    #             # print(text)  # 打印
    #             now_time = identify_picture_conversion_time(
    #                 '\\video\\test{}\\{}-{}-{}-small.png'.format(num, num, c, number))
    #             if number > 1:  # 打印两个图片截图的时间差
    #                 if now_time == '丢失':
    #                     print(f'test{num}-{num}-{c}丢失')
    #                     time.sleep(1)
    #                     os.remove(f'video/test{num}/{num}-{c}-{number}-small.png')
    #                     os.remove(f'video/test{num}/{num}-{c}-{number - 1}.png')  # 清除大图
    #                 else:
    #                     time_difference = datetime.datetime.strptime(identify_picture_conversion_time(
    #                         '\\video\\test{}\\{}-{}-{}-small.png'.format(num, num, c, number - 1)),
    #                         '%Y-%m-%d %H:%M') - datetime.datetime.strptime(
    #                         now_time, '%Y-%m-%d %H:%M')
    #                     # time_difference = now_time - identify_picture_conversion_time('\\video\\test{}\\{}-{}-{}-small.png'.format(num, num, c, number-1))
    #                     print(f'test{num}-{num}-{c}-{number - 1}和test{num}-{num}-{c}-{number}的时间差：{time_difference}')
    #                     time.sleep(1)
    #                     os.remove(f'video/test{num}/{num}-{c}-{number}.png')  # 清除大图
    #                     os.remove(f'video/test{num}/{num}-{c}-{number - 1}-small.png')
    #         except:
    #             print('计算时间错误')
    #     number += 1


threads = []
# name_list = ['op1', 'op2', 'op3', 'op4', 'op5', 'op6', 'op7', 'op8', 'op9']  # 堡垒机用户
name_list = ['op1', 'op2']  # 堡垒机用户

for i in range(1, 10):  # 执行线程前删除video下的所有图片
    img_list = os.listdir(f'video/test{i}')  # 获取video目录的所有文件
    print(img_list)
    if img_list != []:
        for img in img_list:
            os.remove(f'video/test{i}/' + img)
for i in range(len(name_list)):  # 创建线程并将线程加到列表 threads
    num = 1 + i
    t1 = threading.Thread(target=search, args=(name_list[i], num,))
    threads.append(t1)

for t in threads:  # 启动线程
    t.start()
    time.sleep(60)


# 截取时间图像

# img = Image.open(r'{}\\video\\test2\\test3.png'.format(DIR_NAME))
# pic_img = img.crop((1300, 34, 1700, 280))
# pic_img.save(r'{}\\video\\test2\\test3-small.png'.format(DIR_NAME))
# time.sleep(1)

# print(DIR_NAME + '\\video\\test2\\2-7-1.png')
# print('D:\\python\\code\\performance_testing\\video\\test2\\2-7-1.png')
# imgry = im.convert('L')
#
# threshold = 165
# table = []
# for i in range(256):
#     if i <threshold:
#         table.append(0)
#     else:
#         table.append(1)
#
# temp = imgry.point(table, '1')
# today = datetime.datetime.now().today().strftime("%Y-%m-%d") + ' 00:00:00'
# now = datetime.datetime.now().now().strftime("%Y-%m-%d %H:%M:%S")
# print(today, now)


def identify_picture_conversion_time(picture_path):
    """
    识别图片，转换时间格式
    picture_path: \\video\\test2\\test3-small.png
    """
    # im = Image.open(DIR_NAME + '\\video\\test2\\test3-small.png')
    im = Image.open(DIR_NAME + picture_path)
    text = pytesseract.image_to_string(im, config='--psm 6')
    # print(pytesseract.get_languages(config=''))
    # print(text)

    # 将时间格式化

    if 'PM' in text:
        text, gar = text.split('\n')[:2]
        t, day = text.split('PM')
        hour, minute = t.split(':')
        if hour != 12:
            hour = str(12 + int(hour))
        # print('年月日时分' + t, day, hour, minute)
        if len(day) == 11:
            day = day[1:]
        if len(minute) == 3:
            minute = minute[1:]
        now_time = day + ' ' + hour + ':' + minute
    elif 'AM' in text:
        text, gar = text.split('\n')[:2]
        t, day = text.split('AM')
        hour, minute = t.split(':')
        if int(hour) < 10:
            hour = '0' + hour
        if len(day) == 11:
            day = day[1:]
        if len(minute) == 3:
            minute = minute[1:]
        hour = hour[:-1]
        # print('年月日时分' + t, day, hour, minute)
        now_time = day + ' ' + hour + ':' + minute
    else:
        now_time = '丢失'
    print('时间：' + now_time)

    return now_time

# 时间比对

# s = text.split('\n')
# print(s)
# year, month, day = s[1].split('/')
# if int(month) < 10:
#     month = f'0{month}'
# # day = s[1].replace('/', '-')
# day = f'{year}-{month}-{day}'
# now_time = day + ' ' + s[0]
# print(now_time)
# print(datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M') - datetime.datetime.now())
