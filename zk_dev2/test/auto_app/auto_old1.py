import win32api
import win32con
import time
import datetime
import random


def write_file(str1):
    file = open('log.txt', 'a')
    file.write(str1)
    file.close()


time.sleep(5)
x, y = 1, 2
write_file(f"{datetime.datetime.now()}----------------程序开始运行，获取人物坐标---------------\n")


m = 1


while 1:
    # 150次回合结束 或 首次开始，需要重新点击pk键
    win32api.SetCursorPos([1673 + random.randint(1, 50), 110])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(random.randint(1, 4))
    win32api.SetCursorPos([random.randint(x - 15, x + 15), random.randint(y - 20, y + 20)])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 使用键盘码操作，18：alt，65：a，先按alt，在按下a，然后释放
    win32api.keybd_event(18, 0, 0, 0)
    win32api.keybd_event(65, 0, 0, 0)
    win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
    write_file(f"{datetime.datetime.now()}---第{m}次点击pk，alt+a---\n")
    time.sleep(random.randint(1, 4))
    write_file(f"{datetime.datetime.now()}---第{m}次选择人物点击---\n")
    # 开始选中人物
    win32api.SetCursorPos([random.randint(x - 15, x + 15), random.randint(y - 20, y + 20)])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(random.randint(1, 3))
    write_file(f"{datetime.datetime.now()}---选择人物完成，第{m}次开始循环---\n")
    for i in range(1, 301):
        # 执行alt + z 操作
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(90, 0, 0, 0)
        win32api.keybd_event(90, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.001)
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(90, 0, 0, 0)
        win32api.keybd_event(90, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.001)
        # 执行alt + tab操作
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(9, 0, 0, 0)
        win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.002)
        # 开始执行第二个页面的alt + z
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(90, 0, 0, 0)
        win32api.keybd_event(90, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.001)
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(90, 0, 0, 0)
        win32api.keybd_event(90, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.001)
        # 执行alt + tab操作
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(9, 0, 0, 0)
        win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        i += 1
    write_file(f"{datetime.datetime.now()}---第{m}次循环结束，等待5秒---\n")
    time.sleep(random.randint(0, 4))
    m += 1






