import jsonpath
import requests

from zk_dev1.test_imp.common_soms_tool.logger import GetLog


class RequestsClient:
    # 该类会作为所有单接口测试的基类出现，因此在该类中定义好接口所需要的各个字段
    def __init__(self):
        # 创建一个requests的session对象
        self.session = requests.session()
        self.logger = GetLog().get_log()
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
        if kwargs.get('method') is None:
            kwargs['method'] = self.method
        if kwargs.get('headers') is None:
            kwargs['headers'] = self.headers
        if kwargs.get('params') is None:
            kwargs['params'] = self.params
        if kwargs.get('data') is None:
            kwargs['data'] = self.data
        if kwargs.get('json') is None:
            kwargs['json'] = self.json
        if kwargs.get('files') is None:
            kwargs['files'] = self.files
        if kwargs.get('verify') is None:
            kwargs['verify'] = self.verify
        self.logger.info('传入参数header：{}'.format(self.headers))
        print(1233333333)
        self.logger.info('传入参数body: {}'.format(self.json))
        print(1244444444)
        self.logger.info('接口地址：{}'.format(self.url))
        # for item in kwargs.items():
        #     self.logger.info('接口信息:{}'.format(item))
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
    print(RequestsClient().send())
    pass






