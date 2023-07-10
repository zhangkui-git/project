import base64
import json

import requests
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher, AES
from gmssl import sm4
from gmssl.sm4 import SM4_ENCRYPT

from config.config import host, IP
from setting import DIR_NAME





class RsaEncrypt():
    """
    初始化时必须传递公钥和私钥存储的文件路径
    """

    def __init__(self, public_file):
        self.public_file = public_file

    #     self.private_file = private_file

    def generate_key(self):
        """
        这个方法是生成公钥和私钥的，在实际企业测试过程中，开发会提供公钥和私钥，我们不用自己生成
        :return:
        """
        random_generator = Random.new().read
        rsa = RSA.generate(2048, random_generator)
        # 生成私钥
        private_key = rsa.exportKey()
        print(private_key.decode('utf-8'))
        # 生成公钥
        public_key = rsa.publickey().exportKey()
        print(public_key.decode('utf-8'))

        with open(self.private_file, 'wb') as f:
            f.write(private_key)

        with open(self.public_file, 'wb') as f:
            f.write(public_key)
            print('生成')

    # 从秘钥文件中获取密钥
    def get_key(self, key_file):
        with open(key_file) as f:
            data = f.read()
            key = RSA.importKey(data)
        return key

    # # rsa 公钥加密数据
    # def encrypt_data(self,msg):
    #     public_key = self.get_key(self.public_file)
    #     cipher = PKCS1_cipher.new(public_key)
    #     encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    #     return encrypt_text.decode('utf-8')
    # rsa 公钥加密数据
    def encrypt_data(self, msg):
        public_key = self.get_key(self.public_file)
        cipher = PKCS1_cipher.new(public_key)
        encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
        return encrypt_text.decode('utf-8')

    # rsa 私钥解密数据
    def decrypt_data(self, encrypt_msg):
        private_key = self.get_key(self.private_file)
        cipher = PKCS1_cipher.new(private_key)
        back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
        return back_text.decode('utf-8')

    # rsa 私钥签名数据
    def rsa_private_sign(self, data):
        private_key = self.get_key(self.private_file)
        signer = PKCS1_signature.new(private_key)
        digest = SHA.new()
        digest.update(data.encode("utf8"))
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
        signature = signature.decode('utf-8')
        return signature

    # rsa 公钥验证签名
    def rsa_public_check_sign(self, text, sign):
        publick_key = self.get_key(self.public_file)
        verifier = PKCS1_signature.new(publick_key)
        digest = SHA.new()
        digest.update(text.encode("utf8"))
        return verifier.verify(digest, base64.b64decode(sign))


def generate_public_rsa():
    url = host + '/login/getPublicKey'
    res = requests.get(url=url, verify=False)
    res_json = json.loads(res.text)
    # print(res_json['message'])

    with open('public_key.keystore', 'w') as f:
        f.write('-----BEGIN PUBLIC KEY-----\n')
        f.write(res_json['data']['key'] + '\n')
        f.write('-----END PUBLIC KEY-----')

    data = RSA.importKey(open(DIR_NAME + '/common/public_key.keystore').read())
    return data


class Sm4Encrypt:
    """
    sm4 加密
    """

    def __init__(self):
        self.sm4_data = sm4.CryptSM4()

    # 加密
    def encrypt_data(self, key_value, iv_value, input_data):    # 转换成bytes类型
        self.sm4_data.set_key(bytes(key_value, encoding='utf-8'), mode=SM4_ENCRYPT)
        data = self.sm4_data.crypt_cbc(bytes(iv_value, encoding='utf-8'), bytes(input_data, encoding='utf-8'))
        return base64.b64encode(data)


