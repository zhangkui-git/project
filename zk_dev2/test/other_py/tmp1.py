import requests

url = 'https://192.168.4.113:8440/userpermission/usermanage/addUser'
header = {'Authorization': '0dd6503580ff0ae060525a745587832f2b2c3f86ceb5f6a228e468b3a4397806174ed6e9df276dcbdc2c11071cd64e67e8cbc4bebc5aa66438d852f229665f7f3bdef5249729a4985e94b433cbcf46ea90e1bea2b214f074f532837c04281ec1af4b0ac9ee40c82fb6bc388bbf8f4078dd1c8c9a20829a032054eed4cf9f6fcb9f5f094c93ae6373fbafb2ad000b703c4759019faf2397d5d479a72e41e18409fd7399c8b91586bad8ccbed5b099a83f74ce25594de3707a29f9e64bbbaefdc3a33210391cee3321a5b275d6d4b13c9c2c441c42c246d4dbc07d40efc710239ed75c6ff1d72800dd77453cc0a038bc98cf229be4774e7a6fa402bfc2643ce2e59942b4f99819a859df688a76828cacdb5f8ded3959844747ff072789a76b3f42ce86432881c13eacb6e95358650429c04335b5797c0d8c03dfa7b9d0651079b9', 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/530.4 (KHTML, like Gecko) Chrome/2.0.172.0 Safari/530.4'}
body = {
  "userName": "a11",
  "roleId": 1,
  "telephone": "13211131113",
  "email": "123@qq.com",
  "realName": "a11",
  "authType": 0,
  "validTime": "2023-06-13",
  "invalidTime": "2023-06-29",
  "password": "Admin@123",
  "description": "a11",
  "updateType": 3
}

res = requests.post(url=url, headers=header, json=body, verify=False)
print(res.json())


