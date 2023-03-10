import json
import requests
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import base64


class SM4Utils:

    def __init__(self, ):
        pass

    # 加密方法
    def encryptData_ECB(self, plain_text):
        # 创建 SM4对象
        crypt_sm4 = CryptSM4()
        # 定义key值
        secret_key = b"wnt8000LLy&y1234"
        print("key: ", secret_key)

        # 设置key
        crypt_sm4.set_key(secret_key, SM4_ENCRYPT)

        # 调用加密方法加密(十六进制的bytes类型)
        # encrypt_value = crypt_sm4.crypt_ecb(plain_text)
        iv = b"81e693fc4cd33f0f"
        encrypt_value = crypt_sm4.crypt_cbc(iv, plain_text)
        print("encrypt_value: ", encrypt_value)

        # 用base64.b64encode转码（编码后的bytes）
        cipher_text = base64.b64encode(encrypt_value)

        print("加密后：", cipher_text)
        print(cipher_text.decode('utf-8', 'ignore'))
        # 返回加密后的字符串
        return cipher_text.decode('utf-8', 'ignore')

    def decryptData_ECB(self, cipher_text):
        crypt_sm4 = CryptSM4()
        secret_key = b"wnt8000LLy&y1234"
        print(secret_key)
        crypt_sm4.set_key(secret_key, SM4_DECRYPT)
        # 将转入参数base64.b64decode解码成十六进制的bytes类型
        byt_cipher_text = base64.b64decode(cipher_text)
        # 调用加密方法解密，解密后为bytes类型
        decrypt_value = crypt_sm4.crypt_ecb(byt_cipher_text)
        print(decrypt_value)
        print(decrypt_value.decode('utf-8', 'ignore'))
        print(json.dumps(decrypt_value.decode('utf-8', 'ignore')))

        return decrypt_value.decode('utf-8', 'ignore')


# def user_login(user, pas):   # 登录
def user_login():   # 登录
    url = "https://192.168.4.220:8440/login/userLogin"
    headers = {"Content-Type": "application/json"}
    # body = {"userName": f"{user}", "password": f"{pas}"}
    body = {"userName": "rgcQyLX1LWVzHEMj6SL3Kw==", "password": "bZpZ5bgHJRh5K8gQwl+2Wg=="}
    print(12345555, body)
    # body = {'userName': 'hLCCDHQsDnMJrY27wg81WTFCA47LrpypWjy5Kvw8t1t2vnO2XOlsWb0V1Mp8WeTzvUwEAeH39BbA/9q+XAbYfvd9SCjbDW8H9krRqD/wegYz6o0lVuodqkjOFik7flmcdimYq1gjR/ftrCqPGjgeIbRDv6DdJWiyUtGRmYYMFjlu9oN0huJcXbodDawHea1IOmQd6tCI8Po1VhzHsnhJBXqbIMdwE3traRGaTku+Uaa/KM8Fjg3q7Do6Js0B6eoecvvg0ogOdd459NF5eXU3qipNUhsxI6e3NuUWH9h26z4uB7kJbKreCJ9Aua2iS09mDTwAHODz9p3yO1YkoXyInw==', 'userPassword': 'O1tHGqbKK0Zw7Od63xE9CHWSAguF6to8JA97m1w+jdApBfAX06MZDJt/pyJjOhpjrl1taimLItgaln+ebEwUc0yPojhM2aavnLnoExWUTG4GDdW0+T4sPNpCby2ijTlaBHyK0amd3M6hleDeSs5X7bwD97V47vz4IOuQQj5DS9G2bFPmPkxd7t1P7wEbHzrQJIGxIxk+MGNRsshLG1Fn2ZZbY2kW9jHxl7e2ypiA6E5YTotZ7EPWd6DDvdU49WvOT/48jFww3nj/aGbAM2ctWLNQDxiKkSMN+uXthoflAv0WDUyS6JQTsaaOwuxeDI8ASv/aPRaiuR+CGsrSfdilkA=='}
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    print(res.json())
    # return a, res.json()['data']['accessToken']


if __name__ == '__main__':
    SM4_Utils = SM4Utils()

    plain_text1 = b'op13'
    plain_text2 = b"Admin@123456"
    a = SM4_Utils.encryptData_ECB(plain_text1)
    b = SM4_Utils.encryptData_ECB(plain_text2)
    print(a, b)
    # user_login()

    # cipher_text = r"vk2cLOFpUU9fpOs5p9+Mjdl2Ik3s/XXS/BJE1Sgbt8jPFh1kmV2Gf0UUO4ak/Xq4NVARIeK73Q9w7G4MOnRdvxnS4XCWYl7huV2GNew6MEo="
    # SM4_Utils.decryptData_ECB(cipher_text)