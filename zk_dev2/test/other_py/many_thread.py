import time
import threading
import requests
# import log2file
#
list_data = [{"userName": "VrsFf/Za7yoRuMBJBpvkgqFB1M5KbgIpw0Rf326TuA/Q8rWbPN0o+FGhgGfi3lnmoKH1BSUTSM6D4KBJSM/HBy09g9UqkDKn0h5xkDe/rSl7LU9//BdZBsRLdhufbkOzV+MkjFJWApSVLgGf9d80gjfg+BaF7mIGfDiqAMNkyzCp4NJ/OAyXVNukVQimkOFTCb4t1FXv+k/28u0gmR24M7jvGbaGAnoSn0BVp4twKD47PBoY3b2BV6vJTi5q+OvnQ5r0gb0DevnDE46pHrwNhqTmBO91/S/3qfgKT46TIfAXy81eN0hPZcCLkLdTWzcFPpt6PBcr/s3GSLag+Q8ZHQ==","userPassword": "LpYRaOzwpKcCD6KVry/v8dRR0A9lQUt604q6iqgTojbgPLxETo1H7RFG3eFRlDWppPWmC4YdssUlFFaW2eO6TgDBmPNDCSO6EOOyfrF0REi5rvXaRW8pi4TmbpKCt2YdUxpAAB7byKE2eNZnxhxIGzlLVdYRqwN23UPcciePg3cODOH8ohwateod7WCFAcj/kZC26tKMmlvne7ukdyYXh9RsbKTvCkYOJv+5NneWQSx9Pkp/aIEJRgP4a12g/iZ4Mozk3yqnvc0k99DgFx/lgX0dgOtqhlk8PxORrrUbYNB7YEC7g1xHOR+yCh75lmU93K0b7W9ET8mxsgWLgW2PAw=="},{"userName":"YR+UuIlgihAglpzcfzt1o4oU2EUgB0BNdG7JE239W0Q/XCF6i1vz0Zx+l7vR3SwDAf8eSRdSO2Oj8KY3yZsV7BlL3x23JdQuhRgrgkW23X1pWyc3oIrWjcwEzlQJmNyKXPRRhLzLqNuDT+u8cgmpCjPVt3bD5qWfBVz9j7X5rCg/tsBLIVPE41BrisAQni43T3hbH0HoQHQm3nkfLUTMcbIPzl3KylwmC95Za2GEA9n+g7jrX1zk6Uxn+LMo/4IAtmFYObsugXTIORWCPrjDM8NZXGcrg7azuxuVgAaI490vwvi/nBUK/5MqiXDdhRTaizzvuTHnx6HtDtnq43b1VA==","userPassword":"N9BOV3LIWP7cu5cBrVXtF/AUrjZoL3s4v1MfTew0zbywHMMapD814ENdjwkhP54KcoVtervLT5V0X0RaKgPU2wKor3V53gyBPqiJ3tJ9KssP0wuBGnHPr1qyQOwoGUmbWVMbiQ/+vQMN0Ql5tLE4nEbb/J4+s2sP7J6qW+abZvIpgg/AVsTMacVqM6hbyDUb2dYzTOyFhaXGxwItn+ucge/gH5Kg86hJ4NDQEAAQCjhL1FGSD0hclPyJ2rri0VqnTTUyRKjjhsvnMZTUCOFk1suAeI8um9LJ5kfM0o+VvrWbGiw4i+dDQn8UqvjhGD0jtRhf9vGX6KGHsExV8WbQxA=="}]


def select_1(num, body):
# def select_1(num):
    url = "https://192.168.100.248:8440/login/userLogin"
    headers = {"Content-Type": "application/json"}
    # body = list_data[num]
    body = body
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    print(f"线程{num}启动成功", f"{res.json()['data']['accessToken']}")
    token = res.json()['data']['accessToken']
    create_file_url = "https://192.168.100.248:8440/event/page"
    create_file_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    create_file_body = {"startPage":1,"pageSize":20,"filter":[],"keyword":"192.168.0.60"}
    while True:
        create_file_res = requests.post(url=create_file_url, headers=create_file_headers, json=create_file_body, verify=False)
        print(f"线程{num}返回结果：", create_file_res.json())
        time.sleep(5)


def many_thread():
    threads = []
    for x, name in enumerate(list_data):
        threads.append(threading.Thread(target=select_1, args=(x, name)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


# def self_run():
#     t1 = threading.Thread(target=select_1, args=(0,))
#     t2 = threading.Thread(target=select_1, args=(1,))
#     t1.start()
#     time.sleep(1)
#     t2.start()


if __name__ == '__main__':
    # self_run()
    many_thread()









