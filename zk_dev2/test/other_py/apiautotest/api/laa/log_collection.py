'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/5/24 14:22
software: PyCharm
'''

# 区域管理
from api.base_api import BaseApi
from config.config import host


class AddArea(BaseApi):
    def __init__(self, name="test",address='', factoryIpScope='', factoryRegion=["110000", "110100", "110101"], longitude='116.41005', latitude='39.93157', description='', level=1, parentId=2, homePageChat=2, regionMap='', userConfirmed=False):
        """ 新增区域 """
        BaseApi.__init__(self)
        self.url = host + '/factory/add'
        self.method = 'post'
        self.json = {"factoryName": name, "factoryAddress": address, "factoryIpScope": factoryIpScope,
                     "factoryRegion": factoryRegion, "longitude": longitude, "latitude": latitude,
                     "description": description, "level": level, "parentId": parentId, "homePageChat": homePageChat, "regionMap": regionMap,
                     "userConfirmed": userConfirmed}
