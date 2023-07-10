import jsonpath
import requests

from zk_dev2.test.other_py.apiautotest.common.encry_decry import md5
from zk_dev2.test.other_py.apiautotest.common.logger import GetLogger


class RequestsClient:
    # 该类会作为所有单接口测试的基类出现，因此在该类中定义好接口所需要的各个字段
    def __init__(self):
        # 创建一个requests的session对象
        self.session = requests.session()
        self.logger = GetLogger.get_logger()
        self.host = None
        self.url = None
        self.method = None
        self.headers = None
        self.params = None
        self.data = None
        self.json = None
        self.resp = None
        self.files = None
        self.verify = False

    # 因为对于一个请求有很多不确定的参数，因此采用可变参数进行传递
    # def send(self, **kwargs):  # {'params':{xxx,xxx}}
    def send(self, **kwargs):  # {'params':{xxx,xxx}}
        if kwargs.get('url') is None:
            kwargs['url'] = self.url
        if kwargs.get('method') == None:
            kwargs['method'] = self.method
        if kwargs.get('headers') == None:
            kwargs['headers'] = self.headers
        if kwargs.get('params') == None:
            kwargs['params'] = self.params
        if kwargs.get('data') == None:
            kwargs['data'] = self.data
        if kwargs.get('json') == None:
            kwargs['json'] = self.json
        if kwargs.get('files') == None:
            kwargs['files'] = self.files
        if kwargs.get('verify') == None:
            kwargs['verify'] = self.verify
        self.logger.info('接口地址：{}'.format(self.url))
        # for item in kwargs.items():
        #     self.logger.info('接口信息:{}'.format(item))
        print("测试", self.headers)
        self.resp = self.session.request(**kwargs)
        self.logger.info('接口响应状态码:{}'.format(self.resp.status_code))
        self.logger.info('接口响应内容:{}'.format(self.resp.text))
        return self.resp

    def extract_resp(self, jsonpath_express, index=0):
        """
        通过index来控制提取后的结果数量，大于0的按照你指定的index返回对应的值，传-1可以用来表示获取匹配到的所有结果
        :param jsonpath_express:
        :param index:
        :return:
        """
        if self.resp != '' and self.resp != None:
            if index >= 0:
                return jsonpath.jsonpath(self.resp.json(), jsonpath_express)[index]
            else:
                return jsonpath.jsonpath(self.resp.json(), jsonpath_express)


if __name__ == '__main__':
    pass