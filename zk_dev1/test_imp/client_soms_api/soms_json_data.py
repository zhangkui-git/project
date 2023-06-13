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






































