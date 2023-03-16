import requests
import logging


logger = logging.getLogger("allure_log")

url = "https://192.168.4.154:8440/login/userLogin"
# headers = {"Content-Type": "application/json;charset=UTF-8"}
headers = {"Content-Type": "application/json"}
body = {"userName":"VfvSIaquH4PmXwHWNcFS5jtXldQT0pyPfV4jTrI5cRfB749Q3SbXsxneK/pU6zXr/SRoBLs4QR4D27VYkTAPnaLd8sqOqiqIFZ5sLTP2hH0i7KOeuEJtxJ6jGl+GkU2Sopt2AqrBOrNGI0IJdZ1v3PM7EziuaqxX3R96y+k+nALnexUEb2iaQg1Qxrs5UqM7TINttzG0VeAOBPjGQLwM2kdu3G2OJqismk4WwhUXczMbws1e9G5N2evHMQHCj/VboDRD9cCOSy5gbMRO30qmM6xdfS7cwpPnIcRq7fnIUfzRVtc7tTk/wM6ui4fasxNh7drKwPZwBok1r+CC1hr0aQ==","userPassword":"bBEpADbXLJbhHiOCsFgN31CVT4Wn3g0WM0+dcfZenjjZMoTvIULiRLgX8fYCU0P57EbKcDNxQMkzPIdyGy5w/dl8BjJWSCnBY0bVoqSP4KRcj1huHFqoKbsAISti5TJrC19gT+mhdQpNUoMwC5Y4uB529bfewJWm4K8F4t3v9fUdGndVzgn+BjhIEWnZc+wDThd78XjMDIZeSGwux+W1wzU8nOYBquSxSehbevL87pXrj21q1k8BfTt2oV+0GVJdJT5VVpmHDX7xD89nO9jLjxAQenXXbDOdH93mDs0d+Zz5ZEr8dl+xW7/omtVm7cAyqVy7BO+KV1iA/xfPFuqYyw=="}


class Testlogsrc(object):
    def log_source_Add():
        res = requests.post(url=url, headers=headers, json=body, verify=False)
        token = res.json()['data']['accessToken']
        print(token)
        add_url = "https://192.168.4.154:8440/log/source/add"
        add_headers = {"Content-Type": "application/json;charset=UTF-8",
                        "Authorization": f'{token}'}
        add_body = {"logSourceName":"testzk2","assetIp":"192.168.92.128","assetType":1,"factory":3,"port":"","protocolType":1,"snmpVersion":1,"normalizeGroup":[1399],"community":"","isAnonymousLogin":0,"userName":"","password":"","filePath":"","originalEncoding":"UTF-8","downloadRate":1000,"taskInterval":300,"ftpMode":1,"dbType":"MySQL","dbName":"","customerSqlStatus":0,"dbTableName":"","selectSql":"","logType":[]}
        print(add_headers)
        res1 = requests.post(add_url, headers=add_headers, json=add_body, verify=False)
        a = []
        a.append(res1.json()['statusCode'])
        a.append(res1.json()['message'])
        print(a)
        return a, res1.json()

    def log_source_Del():
        res = requests.post(url=url, headers=headers, json=body, verify=False)
        token = res.json()['data']['accessToken']
        del_url = "https://192.168.4.154:8440/log/source/delete/batch"
        del_headers = {"Content-Type": "application/json;charset=UTF-8",
                        "Authorization": f'{token}'}
        ids = input("请输入ids---:")
        del_body = {"ids": [f"{ids}"]}
        res1 = requests.delete(del_url, headers=del_headers, json=del_body, verify=False)
        # print(res.json())
        a = []
        a.append(res1.json()['statusCode'])
        a.append(res1.json()['message'])
        print(a)
        return a, res1.json()


# if __name__ == '__main__':
#     Testlogsrc.log_source_Add()
#     Testlogsrc.log_source_Del()
