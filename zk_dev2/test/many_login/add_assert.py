import time
import requests
from login import *

token = many_token()


def add_assert(token, ip):
    add_assert_url = "https://192.168.100.248:8440/assets/confirm"
    add_assert_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    add_assert_body = {"ssoUsers":[],"ip":f"{ip}","name":f"{ip}","modelId":"","factoryId":3,"mac":"","alias":"","serialNumber":"","deviceVersion":"","hasGuard":"","operateSystem":"","ipMacs":[],"typeId":"","vendorId":"","belongingUnit":"","belongProfessiona":"","belongingSystem":"","hostName":"","physicalPortNumber":"","loginTime":"","assetBusinessValue":"3","assetConfidentiality":"","assetIntegrity":"","assetAvailability":"","safetyResponsiblePerson":"","values":["",""],"ssoType":"","ssoVersion":"","ssoAddr":""}
    res = requests.post(url=add_assert_url, headers=add_assert_header, json=add_assert_body, verify=False)
    # add_assert_result = res.json()
    # print("操作结果：", add_assert_result)


# def add_many_assert(name):
def add_many_assert():
    # mip = [f'192.{ip1}.55.{ip}' for ip in range(250) for ip1 in range(250)]
    mip = [f'192.{ip1}.55.{ip}' for ip in range(5)]
    n = 0
    for ip in mip:
        add_assert(token[0], ip)
        n += 1
        # time.sleep(0.002)
        print(f"新增了资产{n}个")


if __name__ == '__main__':
    add_many_assert()

