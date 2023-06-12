import time
import requests

from zk_dev1.test_imp.common_tool.encry_decry import *


user = RsaEncrypt('public_key.keystore').encrypt_data(f'{username}')
pas = RsaEncrypt('public_key.keystore').encrypt_data(f'{password}')

class test1():
    def user_login():   # 登录
        url = f"{host}/login/userLogin"
        headers = {"Content-Type": "application/json"}
        body = {"userName": f"{user}", "userPassword": f"{pas}"}
        # body = {'userName': 'hLCCDHQsDnMJrY27wg81WTFCA47LrpypWjy5Kvw8t1t2vnO2XOlsWb0V1Mp8WeTzvUwEAeH39BbA/9q+XAbYfvd9SCjbDW8H9krRqD/wegYz6o0lVuodqkjOFik7flmcdimYq1gjR/ftrCqPGjgeIbRDv6DdJWiyUtGRmYYMFjlu9oN0huJcXbodDawHea1IOmQd6tCI8Po1VhzHsnhJBXqbIMdwE3traRGaTku+Uaa/KM8Fjg3q7Do6Js0B6eoecvvg0ogOdd459NF5eXU3qipNUhsxI6e3NuUWH9h26z4uB7kJbKreCJ9Aua2iS09mDTwAHODz9p3yO1YkoXyInw==', 'userPassword': 'O1tHGqbKK0Zw7Od63xE9CHWSAguF6to8JA97m1w+jdApBfAX06MZDJt/pyJjOhpjrl1taimLItgaln+ebEwUc0yPojhM2aavnLnoExWUTG4GDdW0+T4sPNpCby2ijTlaBHyK0amd3M6hleDeSs5X7bwD97V47vz4IOuQQj5DS9G2bFPmPkxd7t1P7wEbHzrQJIGxIxk+MGNRsshLG1Fn2ZZbY2kW9jHxl7e2ypiA6E5YTotZ7EPWd6DDvdU49WvOT/48jFww3nj/aGbAM2ctWLNQDxiKkSMN+uXthoflAv0WDUyS6JQTsaaOwuxeDI8ASv/aPRaiuR+CGsrSfdilkA=='}
        res = requests.post(url=url, headers=headers, json=body, verify=False)
        a = []
        a.append(res.json()['statusCode'])
        a.append(res.json()['message'])
        print(a, res.json()['data']['accessToken'])
        return a, res.json()['data']['accessToken']


    def test_up_add():
        token = test1.user_login()[1]
        print(token, 111111)
        up_add_url = f"{host}/normalize/copy"
        up_add_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
        up_add_body = {"ruleName":"配置变更日志-副本11111","ruleId":"62d691c37794295966c3571b"}
        res = requests.post(up_add_url, headers=up_add_headers, json=up_add_body, verify=False)
        c = []
        c.append(res.json()['statusCode'])
        c.append(res.json()['message'])
        print(res.json())

    # def test_log_source_add():  # 添加日志源
    #     token = test1.user_login()[1]
    #     log_source_add_url = f"{host}/log/source/add"
    #     log_source_add_headers = {"Content-Type": "application/json;charset=UTF-8",
    #                               "Authorization": f'{token}'}
    #     log_source_add_body = {"logSourceName": "testzk2", "assetIp": "192.168.92.128", "assetType": 1, "factory": 3,
    #                            "port": "", "protocolType": 1, "snmpVersion": 1, "normalizeGroup": [1399],
    #                            "community": "", "isAnonymousLogin": 0, "userName": "", "password": "", "filePath": "",
    #                            "originalEncoding": "UTF-8", "downloadRate": 1000, "taskInterval": 300, "ftpMode": 1,
    #                            "dbType": "MySQL", "dbName": "", "customerSqlStatus": 0, "dbTableName": "",
    #                            "selectSql": "", "logType": []}
    #     res = requests.post(log_source_add_url, headers=log_source_add_headers, json=log_source_add_body, verify=False)
    #     print(res.json())


if __name__ == '__main__':
    test1.test_up_add()

