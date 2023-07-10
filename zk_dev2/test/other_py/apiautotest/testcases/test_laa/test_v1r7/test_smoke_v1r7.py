'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/5/24 14:16
software: PyCharm
'''
from api.laa.log_collection import AddArea


class Test_Smoking:

    def test_1(self):
        resp = AddArea().send()
        print(resp.json())