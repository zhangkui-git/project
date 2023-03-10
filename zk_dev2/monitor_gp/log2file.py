import logging.handlers
import os

# 设置日志文件的存放目录
log_dir = 'logdir'
# 设置日志文件的名字
log_filename = 'monitor_gp.log'

# 日志格式化输出
# LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
# 日期格式
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"

log_dir = os.getcwd() + "/" + log_dir
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = log_dir + '/' + log_filename

# 一个日志50M, 超过 app.log 指定的大小会自动滚动创建日志文件  app.log.1, app.log.2, app.log.3
fp = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1024 * 1024 * 50,
                                             backupCount=30,encoding='utf-8')

# 再创建一个handler，用于输出到控制台
fs = logging.StreamHandler()

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp])
# 测试
if __name__ == '__main__':
    logging.info("打印日志")
