import time

import pyautogui
import pyperclip
# from apscheduler.schedulers.blocking import BlockingScheduler

# 操作间隔
pyautogui.PAUSE = 1

wx_hotkey = {"open": ('ctrl', 'alt', 'w'), "send": ('enter',), "shot": ('ctrl', 'alt', 'j')}


def send_msg(name: str, msg: str, hotkey=None) -> None:
    # 打开微信
    if hotkey is None:
        hotkey = wx_hotkey

    pyautogui.hotkey(*hotkey["open"])
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    # 找到用户
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press(*hotkey["send"])
    time.sleep(1)
    # 发送消息
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press(*hotkey["send"])
    time.sleep(1)
    # 隐藏微信
    pyautogui.hotkey(*hotkey["open"])

# 定时任务
# def timing(task, time: dict) -> None:
#     scheduler = BlockingScheduler()  # 实例化一个调度器
#     scheduler.add_job(task, 'cron', hour=time["hour"], minute=time["minute"])  # 添加任务
#     # scheduler.add_job(task, 'interval', seconds=5)  # 添加任务
#     scheduler.start()


# if __name__ == '__main__':
#     send_msg("文件传输", "1234")












