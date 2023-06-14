from zk_dev1.test_imp.common_soms_tool.SM4_CBC import *

user = SM4Utils().encryptData_CBC(bytes('a11', "UTF-8"))
pas = SM4Utils().encryptData_CBC(bytes('Admin@123', "UTF-8"))

add_user = {
  "userName": f"{user}",
  "roleId": 1,
  "telephone": "13211131113",
  "email": "123@qq.com",
  "realName": "a11",
  "authType": 0,
  "validTime": "2023-06-13",
  "invalidTime": "2023-06-29",
  "password": f"{pas}",
  "description": "a11",
  "updateType": 3
}

user_role = {
  "name": "test1",
  "parentRole": 1,
  "description": "",
  "menuIds": [
    2000,
    3000,
    5000,
    5100,
    5200,
    5300,
    5400,
    5600,
    6000,
    6100,
    6200,
    7000,
    7100,
    8000,
    8100,
    9050,
    9100,
    9150,
    9200,
    9300,
    9450,
    9500,
    9550,
    9650,
    10000,
    10100,
    10300,
    11000,
    11100,
    11200,
    11300,
    11400,
    11500,
    11600
  ]
}




































