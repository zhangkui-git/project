# 为函数添加一个统计运行时长的功能
import time
import threading


def how_much_time(func):
    def inner():
        t_start = time.time()
        func()
        t_end = time.time()
        print("一共花费了{0}秒时间".format(t_end - t_start, ))

    return inner
    # 将增加的新功能代码以及被装饰函数运行代码func()一同打包返回，返回的是一个内部函数，这个被返回的函数就是装饰器


def sleep_5s():
    time.sleep(5)
    print("%d秒结束了" % (5,))


def sleep_6s():
    time.sleep(6)
    print("%d秒结束了" % (6,))


sleep_5s = how_much_time(sleep_5s)
# 因为sleep_5s函数的功能就是睡5秒钟，虽然增加了统计运行时间的功能，但是他本身功能没变(还是睡5秒钟)，所以仍然用原来函数名接收增加功能了的自己
sleep_6s = how_much_time(sleep_6s)

t1 = threading.Thread(target=sleep_5s)
t2 = threading.Thread(target=sleep_6s)
t1.start()
t2.start()
# 5秒结束了
# 一共花费了5.014161109924316秒时间
# 6秒结束了
# 一共花费了6.011810302734375秒时间









































































