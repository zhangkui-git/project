import logging
from logging.handlers import TimedRotatingFileHandler
from zk_dev1.dev_imp.common_tool.common_conf import log_dir_name


class GetLog(object):
    def __init__(self):
        self.log = logging.getLogger("auto_dev_imp")
        self.log.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)
        self.sh.setFormatter(self.formatter)
        self.fh = TimedRotatingFileHandler(filename=log_dir_name, when='H', interval=1, backupCount=2)
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)  # 给handler添加formatter
        self.fh.suffix = '%Y-%m-%d_%H-%M'  # 切割后的日志设置后缀
        # self.log.addHandler(self.sh)
        self.log.addHandler(self.fh)

    def get_log(self):
        return self.log



