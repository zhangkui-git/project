import json
import requests
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import base64
import urllib3
from zk_dev1.test_imp.common_soms_tool.common_conf import *
urllib3.disable_warnings()


def get_key():
    # 通过接口获取IV 、KEY
    url = f"{host}/login/getPublicKey"
    res = requests.get(url=url, verify=False)
    # print(res.json()['data'])
    return res.json()['data']


class SM4Utils():

    def __init__(self, ):
        pass

    def encryptData_CBC(self, plain_text):  # 加密方法
        # 创建 SM4对象
        crypt_sm4 = CryptSM4()
        # iv = b"81e693fc4cd33f0f"
        # key = b"wnt8000LLy&y1234"
        iv = bytes(get_key()["iv"], "UTF-8")
        key = bytes(get_key()["key"], "UTF-8")
        # 定义key值
        secret_key = key
        # print("key: ", secret_key)

        # 设置key
        crypt_sm4.set_key(secret_key, SM4_ENCRYPT)

        # 调用加密方法加密(十六进制的bytes类型)
        # encrypt_value = crypt_sm4.crypt_ecb(plain_text)
        encrypt_value = crypt_sm4.crypt_cbc(iv, plain_text)
        # print("encrypt_value: ", encrypt_value)

        # 用base64.b64encode转码（编码后的bytes）
        cipher_text = base64.b64encode(encrypt_value)

        # print("加密后：", cipher_text)
        # print(cipher_text.decode('utf-8', 'ignore'))
        # 返回加密后的字符串
        return cipher_text.decode('utf-8', 'ignore')

    def decryptData_CBC(self, cipher_text):  # 解密方法
        crypt_sm4 = CryptSM4()
        # iv = b"81e693fc4cd33f0f"
        # key = b"wnt8000LLy&y1234"
        iv = bytes(get_key()["iv"], "UTF-8")
        key = bytes(get_key()["key"], "UTF-8")
        secret_key = key
        # print(secret_key)
        crypt_sm4.set_key(secret_key, SM4_DECRYPT)
        # 将转入参数base64.b64decode解码成十六进制的bytes类型
        byt_cipher_text = base64.b64decode(cipher_text)
        # 调用加密方法解密，解密后为bytes类型
        decrypt_value = crypt_sm4.crypt_cbc(iv, byt_cipher_text)
        # print(decrypt_value)
        # print(decrypt_value.decode('utf-8', 'ignore'))
        # print(json.dumps(decrypt_value.decode('utf-8', 'ignore')))

        return decrypt_value.decode('utf-8', 'ignore')


if __name__ == '__main__':
    SM4_Utils = SM4Utils()
    # iv = b"81e693fc4cd33f0f"
    # key = b"wnt8000LLy&y1234"
    plain_text1 = bytes(user, "UTF-8")
    plain_text2 = bytes(pas, "UTF-8")
    a = SM4_Utils.encryptData_CBC(plain_text1)
    b = SM4_Utils.encryptData_CBC(plain_text2)
    print(a, b)
    # user_login()
    SM4_Utils.decryptData_CBC('bZpZ5bgHJRh5K8gQwl+2Wg==')
    # cipher_text = r"vk2cLOFpUU9fpOs5p9+Mjdl2Ik3s/XXS/BJE1Sgbt8jPFh1kmV2Gf0UUO4ak/Xq4NVARIeK73Q9w7G4MOnRdvxnS4XCWYl7huV2GNew6MEo="
    # SM4_Utils.decryptData_ECB(cipher_text)