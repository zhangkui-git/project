import time
import requests
from login import *

token = many_token()


def add_assert(token, ip):
    print(token)
    add_assert_url = f"{host}/assets/confirm"
    add_assert_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    add_assert_body = {"ssoUsers":[],"ip":f"{ip}","name":f"{ip}","modelId":"","factoryId":5,"mac":"","alias":"","serialNumber":"","deviceVersion":"","hasGuard":"","operateSystem":"","ipMacs":[],"typeId":"","vendorId":"","belongingUnit":"","belongProfessiona":"","belongingSystem":"","hostName":"","physicalPortNumber":"","loginTime":"","assetBusinessValue":"3","assetConfidentiality":"","assetIntegrity":"","assetAvailability":"","safetyResponsiblePerson":"","values":[],"ssoType":"","ssoVersion":"","ssoAddr":""}
    res = requests.post(url=add_assert_url, headers=add_assert_header, json=add_assert_body, verify=False)
    add_assert_result = res.json()
    print("操作结果：", add_assert_result)


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
    # add_many_assert()
    token1 = '0dd6503580ff0ae060525a745587832f2b2c3f86ceb5f6a228e468b3a4397806174ed6e9df276dcbdc2c11071cd64e67e8cbc4bebc5aa664fa982c4232a77ed4a293e1bd647aecaf5e94b433cbcf46ea90e1bea2b214f074f532837c04281ec1f8aee3743a2b851e5a6a6931f7610a69869a527f6ef0dfb22054eed4cf9f6fcb9f5f094c93ae6373c1a81cc5e541003f4759019faf2397d5d479a72e41e18409e7c303524b7b39689ccd64cbb915e74b0a724768d53d08245d931ed79c6d5015f4e65cbad7752e52a2308153d62fead1458c194ab55d4b74a2b43cb29e3dd5556053132415970d76434944694966ea8c0d2712d80043aa0ab0cc241baad32dce48997dc3f56c4e814e9928d788fd22997c5ca967ff87a2500d7b6ad74c6ed53d'
    add_assert(token[0], '192.1.1.10')
