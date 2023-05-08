import requests

url = "https://192.168.4.107:8440/userpermission/usermanage/getAllUserInfo"
header = {"Content-Type": "application/json;charset=UTF-8", "Connection": "keep-alive", "Authorization": "0dd6503580ff0ae060525a745587832f2b2c3f86ceb5f6a228e468b3a4397806174ed6e9df276dcbdc2c11071cd64e67e8cbc4bebc5aa66490577abff7a8c8e1fb8c67f311f2ba725e94b433cbcf46ea90e1bea2b214f074f532837c04281ec19d1bd88805f5c309443eab883fe9cef28f3757db761b73d92054eed4cf9f6fcb9f5f094c93ae6373c1a81cc5e541003f4759019faf2397d5d479a72e41e18409e7c303524b7b39689ccd64cbb915e74b0a724768d53d08245d931ed79c6d501507072b39d42d2c7934272db76203f28d458c194ab55d4b74a196eb77761c521692a0a5836eb36e2c989daf6594d9bc927047ffe537c0f59ce8a27ac0221cd094c9a8983630d12e724c54bf0dbe99de0fd65bf077926d80a1"}
body = {"keywords": "admin", "startPage": 1, "pageSize": 20, "order": ""}

res = requests.post(url=url, headers=header, json=body, verify=False)

print(res.json())































