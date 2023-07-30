import time
import pyautogui


time.sleep(10)
# 等待10秒自动获取鼠标
x, y = pyautogui.position()
pyautogui.click(x, y, button='left')


while 1:
    n = 1
    while n <= 5:
        pyautogui.hotkey('alt', 'z')
        time.sleep(0.05)
        pyautogui.hotkey('ctrl', '1')
        time.sleep(0.05)
        n += 1
    time.sleep(180)







