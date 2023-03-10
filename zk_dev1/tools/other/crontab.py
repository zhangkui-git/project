import schedule
import datetime


# 引入schedule和time

def job():
    print(f"{time_now}--------", "I'm working...")


# 定义一个叫job的函数，函数的功能是打印'I'm working...'

schedule.every(3).seconds.do(job)
# schedule.every(10).minutes.do(job)  # 部署每10分钟执行一次job()函数的任务
# schedule.every().hour.do(job)  # 部署每×小时执行一次job()函数的任务
# schedule.every().day.at("10:30").do(job)  # 部署在每天的10:30执行job()函数的任务
# schedule.every().monday.do(job)  # 部署每个星期一执行job()函数的任务
# schedule.every().wednesday.at("13:15").do(job)  # 部署每周三的13：15执行函数的任务

while True:
    time_now = datetime.datetime.now()
    schedule.run_pending()


