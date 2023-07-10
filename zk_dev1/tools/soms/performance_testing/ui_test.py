"""
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2023/3/24 9:38
software: PyCharm
"""
import os
import threading
import time

import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

from setting import DIR_NAME


class TestUi:
    """
    脚本注意事项：
    1 self.name_list   堡垒机用户：op1、op2(需根据实际修改) 密码：self.pwd （需根据实际修改）
    2 需添加资产与用户的权限组
    3 堡垒机远程用户名命名：test10-test30（需存在） 密码： self.rdp_pwd（需根据实际修改）
    4 堡垒机远程用户192.168.4.119：元素的定位方式需根据页面变化(代码101行)
    """

    def __init__(self):
        self.ip = '192.168.100.248'
        self.host = f'https://{self.ip}:8440'  # ip地址
        self.success_num = 0  # 成功次数
        self.failed_num = 0  # 失败次数
        self.count = 1  # 截图次数
        self.threads = []  # 线程数
        self.name_list = ['op1', 'op2']  # 堡垒机用户
        self.pwd = 'Admin@123456'  # 堡垒机用户密码
        self.rdp_pwd = 'Admin@123'  # rdp用户密码

    @staticmethod
    def clear_image():
        """ 清除截图 """
        for i in range(1, 10):  # 执行线程前删除video下的所有图片
            img_list = os.listdir(f'video/test{i}')  # 获取video目录的所有文件
            print(img_list)
            if img_list != []:
                for img in img_list:
                    os.remove(f'video/test{i}/' + img)

    def add_thread(self):
        """ 创建线程并将线程加到列表 threads """

        for i in range(len(self.name_list)):  # 创建线程并将线程加到列表 threads
            num = 1 + i
            t1 = threading.Thread(target=self.search, args=(self.name_list[i], num,))
            self.threads.append(t1)

        # print(self.threads)
        for t in self.threads:  # 启动线程
            t.start()
            time.sleep(60)

        while True:  # 判断线程是否存活，如果不存活移除线程，重新开始新线程
            for num, th in enumerate(self.threads):
                # print(num, th)
                if th.is_alive() is False:
                    # print(num, th, th.is_alive())
                    self.threads.remove(th)  # 移除线程
                    # print(num, self.name_list[num], num + 1)
                    t1 = threading.Thread(target=self.search, args=(self.name_list[num], num + 1,))
                    self.threads.insert(num, t1)  # 新创建的线程插入到失败的线程位置
                    t1.start()  # 开启新线程
            time.sleep(60)

    def search(self, soms_name, num):
        print(num)
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.host)
        time.sleep(1)
        driver.find_element(By.ID, value='details-button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, value='//*[@id="final-paragraph"]/a').click()
        time.sleep(1)
        driver.find_element(By.NAME, value='userName').send_keys(soms_name)
        driver.find_element(By.NAME, value='password').send_keys(self.pwd)  # 堡垒机用户密码
        time.sleep(0.5)
        driver.find_element(By.XPATH, value='//*[@class="el-button el-button--primary"]/span').click()
        time.sleep(1)
        driver.find_element(By.XPATH, value='(//*[@class="el-menu-item submenu-title-noDropdown"])[2]').click()
        time.sleep(2)
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        time.sleep(1)
        # driver.find_element(By.XPATH, value='(//*[@class="el-tree-node__children"])[2]/div[2]').click() # 可运维资产2
        # count = 1  # 截图次数
        # success_num = 0  # 成功数量
        # failed_num = 0  # 失败数量
        while True:
            for i in range(10):  # 10个窗口
                driver.find_element(By.XPATH,
                                    value='(//*[@class="el-tree-node__children"])[2]/div/div[2]/div[2]/div[1]').click()  # 可运维资产2
                time.sleep(1)
                driver.find_element(By.XPATH, value='//*[@class="el-radio-group"]/label[2]/span').click()  # 手动登录
                time.sleep(1)
                driver.find_element(By.XPATH, value='(//*[@class="el-input__inner"])[last()-3]').send_keys(
                    f'test{num}{i}')
                time.sleep(1)
                driver.find_element(By.XPATH, value='(//*[@class="el-input__inner"])[last()-2]').send_keys(
                    self.rdp_pwd)  # rdp用户密码
                time.sleep(1)
                driver.find_element(By.XPATH, value='(//*[@class="el-form-item__content"])[last()]/button[2]').click()
                time.sleep(2)
            for s in range(15):  #
                s = s + 1
                page_total = driver.find_elements(By.XPATH, value=f'(//*[@class= "el-tabs__nav-scroll"]/div/div/span)')
                # print(len(page_total))    # 窗口数量
                driver.find_element(By.XPATH, value=f'(//*[@class="el-tabs__nav is-top"]/div)[1]').click()
                time.sleep(1)
                # 截图操作
                driver.get_screenshot_as_file(f'video/test{num}/{s}-{self.count}.png')  # 截图
                print(f'video/test{num}/{s}-{self.count}.png')
                time.sleep(2)
                # 截取时间图像
                img = Image.open(r'{}/video/test{}/{}-{}.png'.format(DIR_NAME, num, s, self.count))
                # pic_img = img.crop((1300, 100, 1700, 185))    # 软件时间
                pic_img = img.crop((1830, 885, 1895, 990))  # 右下角时间
                pic_img.save(r'{}/video/test{}/{}-{}-small.png'.format(DIR_NAME, num, s, self.count))  # 保存小图
                # 识别图片
                im = Image.open(DIR_NAME + '/video/test{}/{}-{}-small.png'.format(num, s, self.count))
                text = pytesseract.image_to_string(im, config='--psm 6')
                print(text)  # 打印
                if text != '':  # 判断图片是否存在右下角时间
                    self.success_num += 1
                else:
                    self.failed_num += 1
                if self.count > 2:
                    os.remove(DIR_NAME + '/video/test{}/{}-{}.png'.format(num, s, self.count))
                os.remove(DIR_NAME + '/video/test{}/{}-{}-small.png'.format(num, s, self.count))
                driver.find_element(By.XPATH,
                                    value=f'(//*[@class= "el-tabs__nav-scroll"]/div/div/span)[1]').click()  # 关闭窗口
                time.sleep(1)
                if len(page_total) == 1:
                    break
            self.count += 1
            # print(f'thread{somsname[-1:]}成功数量：{self.success_num}')
            # print(f'thread{somsname[-1:]}失败数量：{self.failed_num}')
            print(f'成功数量：{self.success_num}')
            print(f'失败数量：{self.failed_num}')


if __name__ == '__main__':
    test = TestUi()
    test.clear_image()  # 清除截图
    test.add_thread()  # 创建线程
