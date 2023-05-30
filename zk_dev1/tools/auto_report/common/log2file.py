import logging.handlers
import os

# 设置日志文件的存放目录
dir1 = os.getcwd()
log_dir = f'{dir1}\logdir'

# 设置日志文件的名字
log_filename = 'putsyslog.log'

# 日志格式化输出
# LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
# 日期格式
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = log_dir + '\\' + log_filename

# 一个日志50M, 超过 app.log 指定的大小会自动滚动创建日志文件  app.log.1, app.log.2, app.log.3
# 按时间分割分割
"""针对TimedRotatingFileHandler 做个说明
filename：日志文件名的prefix；
when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：
“S”: Seconds
“M”: Minutes
“H”: Hours
“D”: Days
“W”: Week day (0=Monday)
“midnight”: Roll over at midnight
interval: 滚动周期，单位有when指定，比如：when=’D’,interval=1，表示每天产生一个日志文件；
backupCount: 表示日志文件的保留个数
"""
fp = logging.handlers.TimedRotatingFileHandler(log_filename, when='D', backupCount=3, encoding='utf-8')
# fp = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1024 * 1024 * 20, backupCount=30,encoding='utf-8')

# 再创建一个handler，用于输出到控制台
fs = logging.StreamHandler()

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp])
# 测试
if __name__ == '__main__':
    logging.info("打印日志")
