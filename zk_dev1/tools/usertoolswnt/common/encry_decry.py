'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/11 12:06
software: PyCharm
'''
import base64
import hashlib
import json
import os
import requests
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher, AES
from Crypto.PublicKey import RSA


from config import host
DIR_NAME = os.path.dirname(os.getcwd())

# IP = "192.168.100.248"  # 服务器地址
# host = f"https://{IP}:8440"

def md5(str):
    return hashlib.md5(str.encode('UTF-8')).hexdigest()
class AesEncrypt:
    """
    AES加密
    windows 安装vc++14
    pip install pycryptodome -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

    mac下 pip install pycrypto -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
    """

    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key.encode("utf8"), AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)
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

        with open(self.private_file, 'wb')as f:
            f.write(private_key)

        with open(self.public_file, 'wb')as f:

            f.write(public_key)
            print('生成')
    # 从秘钥文件中获取密钥
    def get_key(self,key_file):
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
    def decrypt_data(self,encrypt_msg):
        private_key = self.get_key(self.private_file)
        cipher = PKCS1_cipher.new(private_key)
        back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
        return back_text.decode('utf-8')

    # rsa 私钥签名数据
    def rsa_private_sign(self,data):
        private_key = self.get_key(self.private_file)
        signer = PKCS1_signature.new(private_key)
        digest = SHA.new()
        digest.update(data.encode("utf8"))
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
        signature = signature.decode('utf-8')
        return signature

    # rsa 公钥验证签名
    def rsa_public_check_sign(self,text,sign):
        publick_key = self.get_key(self.public_file)
        verifier = PKCS1_signature.new(publick_key)
        digest = SHA.new()
        digest.update(text.encode("utf8"))
        return verifier.verify(digest, base64.b64decode(sign))


def generate_public_rsa():
    url = host +'/login/getPublicKey'
    res = requests.get(url=url,verify=False)
    res_json = json.loads(res.text)
    print(res_json['message'])


    with open(DIR_NAME+'/common/public_key.keystore','w')as f:
        f.write('-----BEGIN PUBLIC KEY-----\n')
        f.write(res_json['message']+'\n')
        f.write('-----END PUBLIC KEY-----')

    data = RSA.importKey(open(DIR_NAME+'/common/public_key.keystore').read())
    return data


if __name__ == '__main__':
    print(DIR_NAME+'public_key.keystore')

    print(generate_public_rsa())
    user = RsaEncrypt('public_key.keystore').encrypt_data('audit')
    pas = RsaEncrypt('public_key.keystore').encrypt_data('wnt8000LLy&y')
    data = {"userName": user, "userPassword": pas}
    print(data)
    res = requests.post(url='https://192.168.100.149:8440/login/userLogin', json=data, verify=False)
    result =json.loads(res.text)
    print(result)
    header ={
        'Authorization': result["data"]["accessToken"]
    }
    # res1 = requests.get(url='https://192.168.100.71:8440/kvenum/alarmLevel', headers=header, verify=False)

    # print(json.loads(res.text))
