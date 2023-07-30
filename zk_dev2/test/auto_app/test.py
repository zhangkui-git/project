import pyautogui
import time
import datetime
import random


def write_file(str1):
    file = open('log.txt', 'a')
    file.write(str1)
    file.close()


# time.sleep(5)
# x, y = pyautogui.position()
# write_file(f"{datetime.datetime.now()}----------------程序开始运行，获取人物坐标{x, y}---------------\n")
write_file(f"{datetime.datetime.now()}----------------程序开始运行，获取人物坐标---------------\n")


m = 1

while 1:
    # 150次回合结束 或 首次开始，需要重新点击pk键
    write_file(f"{datetime.datetime.now()}---第{m}次点击pk，alt+a---\n")
    time.sleep(1)
    # 首次启动程序需要选择人物，该选择的人物鼠标定位为桌面非打开游戏界面的人物的坐标位置
    pyautogui.moveTo(random.randint(820 - 15, 820 + 15), random.randint(136 - 15, 136 + 15))
    time.sleep(5)
    pyautogui.leftClick()
    write_file(f"{datetime.datetime.now()}---第{m}次选择人物---\n")
    time.sleep(1)
    write_file(f"{datetime.datetime.now()}---第{m}次开始循环---\n")
    for i in range(1, 301):
        i += 1
    write_file(f"{datetime.datetime.now()}---第{m}次循环结束，等待30秒---\n")
    print(m)
    time.sleep(1)
    m += 1






