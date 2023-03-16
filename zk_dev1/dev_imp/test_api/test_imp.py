import requests
from zk_dev1.dev_imp.common_tool.common_conf import common_url, username, password
from zk_dev1.dev_imp.common_tool.logger import GetLog

write_log = GetLog().get_log()

"""登录"""
def Login():
    url = f"{common_url}/login/userLogin"
    headers = {"Content-Type": "application/json"}
    body = {"userName": f"{username}", "userPassword": f"{password}"}
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    a = []
    a.append(res.json()['statusCode'])
    a.append(res.json()['message'])
    write_log.info(f'登录成功---{res.text}')
    return a, res.json()['data']['accessToken']

# 添加日志源
def log_source_Add():
    token = Login()[1]
    add_url = f"{common_url}/log/source/add"
    add_headers = {"Content-Type": "application/json;charset=UTF-8",
                    "Authorization": f'{token}'}
    add_body = {"logSourceName":"testzk2","assetIp":"192.168.92.128","assetType":1,"factory":3,"port":"","protocolType":1,"snmpVersion":1,"normalizeGroup":[1399],"community":"","isAnonymousLogin":0,"userName":"","password":"","filePath":"","originalEncoding":"UTF-8","downloadRate":1000,"taskInterval":300,"ftpMode":1,"dbType":"MySQL","dbName":"","customerSqlStatus":0,"dbTableName":"","selectSql":"","logType":[]}
    res = requests.post(add_url, headers=add_headers, json=add_body, verify=False)
    a = []
    a.append(res.json()['statusCode'])
    a.append(res.json()['message'])
    write_log.info(f'添加日志源成功---{res.text}')
    return a, res.json()

# 删除日志源
def log_source_Del():
    token = Login()[1]
    del_url = f"{common_url}/log/source/delete/batch"
    del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    ids = input('请输入ids---:')
    del_body = {'ids': [f'{ids}']}
    res = requests.delete(del_url, headers=del_headers, json=del_body, verify=False)
    a = []
    a.append(res.json()['statusCode'])
    a.append(res.json()['message'])
    return a, res.json()

# 删除日志
def UpDel():
    token = Login()[1]
    del_url = f"{common_url}/normalize/delete/batch"
    del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    del_body = {"ids": ["62zhangkuiac9"]}
    res = requests.delete(del_url, headers=del_headers, json=del_body, verify=False)
    a = []
    a.append(res.json()['statusCode'])
    a.append(res.json()['message'])
    return a, res.json()


