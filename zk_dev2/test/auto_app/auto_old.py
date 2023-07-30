import random

import pyautogui
import time
import datetime

time.sleep(10)
x, y = pyautogui.position()


def write_file(str1):
    file = open('./log.txt', 'a')
    file.write(str1)
    file.close()


def add_click():
    n = 1
    while n <= 50:
        pyautogui.click(x, y)
        n += 1


write_file(f"{datetime.datetime.now()}----------------程序开始运行，获取人物坐标   \n")

m = 1
while 1:
    # 150次回合结束 或 首次开始，需要重新点击pk键
    pyautogui.click(520, 124)
    pyautogui.hotkey('alt', 'a')
    time.sleep(float('1' + '.' + str(random.randint(1, 1000))))
    # 首次启动程序需要选择人物，该选择的人物鼠标定位为桌面非打开游戏界面的人物的坐标位置
    # pyautogui.click(x, y)
    write_file(f"{datetime.datetime.now()}----------------第{m}次循环开始   \n")
    add_click()
    # time.sleep(200)
    for i in range(1, 301):
        pyautogui.hotkey('alt', 'z')
        # time.sleep(0.005)
        pyautogui.hotkey('alt', 'z')
        # time.sleep(0.005)
        pyautogui.hotkey('alt', 'tab')
        # time.sleep(0.005)
        pyautogui.hotkey('alt', 'z')
        # time.sleep(0.005)
        pyautogui.hotkey('alt', 'z')
        # time.sleep(0.005)
        pyautogui.hotkey('alt', 'tab')
        i += 1
    write_file(f"{datetime.datetime.now()}----------------第{m}次循环结束   \n")
    m += 1



