import requests


url = "https://192.168.4.154:8440/login/userLogin"
# headers = {"Content-Type": "application/json;charset=UTF-8"}
headers = {"Content-Type": "application/json"}
body = {"userName":"VfvSIaquH4PmXwHWNcFS5jtXldQT0pyPfV4jTrI5cRfB749Q3SbXsxneK/pU6zXr/SRoBLs4QR4D27VYkTAPnaLd8sqOqiqIFZ5sLTP2hH0i7KOeuEJtxJ6jGl+GkU2Sopt2AqrBOrNGI0IJdZ1v3PM7EziuaqxX3R96y+k+nALnexUEb2iaQg1Qxrs5UqM7TINttzG0VeAOBPjGQLwM2kdu3G2OJqismk4WwhUXczMbws1e9G5N2evHMQHCj/VboDRD9cCOSy5gbMRO30qmM6xdfS7cwpPnIcRq7fnIUfzRVtc7tTk/wM6ui4fasxNh7drKwPZwBok1r+CC1hr0aQ==","userPassword":"bBEpADbXLJbhHiOCsFgN31CVT4Wn3g0WM0+dcfZenjjZMoTvIULiRLgX8fYCU0P57EbKcDNxQMkzPIdyGy5w/dl8BjJWSCnBY0bVoqSP4KRcj1huHFqoKbsAISti5TJrC19gT+mhdQpNUoMwC5Y4uB529bfewJWm4K8F4t3v9fUdGndVzgn+BjhIEWnZc+wDThd78XjMDIZeSGwux+W1wzU8nOYBquSxSehbevL87pXrj21q1k8BfTt2oV+0GVJdJT5VVpmHDX7xD89nO9jLjxAQenXXbDOdH93mDs0d+Zz5ZEr8dl+xW7/omtVm7cAyqVy7BO+KV1iA/xfPFuqYyw=="}

class TestDel(object):
    def UpDel():
        res = requests.post(url=url, headers=headers, json=body, verify=False)
        token = res.json()['data']['accessToken']
        del_url = "https://192.168.4.154:8440/normalize/delete/batch"
        del_headers = {"Content-Type": "application/json;charset=UTF-8",
                    "Authorization": f'{token}'}
        del_body = {"ids": ["62zhangkuiac9"]}
        print(del_headers)
        res = requests.delete(del_url, headers=del_headers, json=del_body, verify=False)
        a = []
        a.append(res.json()['statusCode'])
        a.append(res.json()['message'])
        print(a)
        return a, res.json()


# if __name__ == '__main__':
#     TestDel.UpDel()
