import time

import cv2
import pyautogui

time.sleep(5)
x, y = pyautogui.position()


def get_xy(img_path):
    """
    用来获取游戏人物在桌面的坐标
    :param img_path: 桌面截图
    :return: 以元组形式返回游戏人物在桌面的坐标
    """
    # 将屏幕截图保存
    pyautogui.screenshot().save("./pic1.png")
    # 载入截图
    img = cv2.imread("./pic1.png")
    # 图像模板
    img_terminal = cv2.imread(r"D:\work_soft\python2021\project\zk_dev2\test\other_py\pic2.png")
    # 读取模板的宽度和高度
    height, width, channel = img_terminal.shape
    # 进行模板匹配
    result = cv2.matchTemplate(img, img_terminal, cv2.TM_SQDIFF_NORMED)
    # 解析出屏幕左上角的坐标
    upper_left = cv2.minMaxLoc(result)[2]
    # 计算匹配区域右下角的坐标
    lower_right = (upper_left[0] + width, upper_left[1] + height)
    # 计算中心区域坐标并且返回
    avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
    return avg


def auto_click(var_avg):
    """
    接收一个元组坐标值
    :param var_avg: 元组坐标
    :return:
    """
    pyautogui.click(var_avg[0], var_avg[1], button='left')
    time.sleep(5)


def routine(img_path, name):
    avg = get_xy(img_path)
    print(f"正在点击{name}")
    auto_click(avg)


n = 1
while n <= 10:
    pyautogui.click(x, y, button='left')
    time.sleep(1)
    pyautogui.hotkey("alt" + "a")
    time.sleep(1)
    routine("./pic2.png", f"桌面{n}")
    time.sleep(1)
    pyautogui.hotkey("esc")
    time.sleep(1)
    n += 1




