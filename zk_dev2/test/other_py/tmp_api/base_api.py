
from common.client import RequestsClient
from config.config import host


class BaseApi(RequestsClient):
    Authorization = None
    def __init__(self):
        #首先调用父类初始化
        RequestsClient.__init__(self)
        self.host = host
        self.headers = {
            'Authorization': BaseApi.Authorization

        }
