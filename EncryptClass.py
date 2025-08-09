import base64
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''
class Encryptclass:
    # def __init__(self, key, e_text,d_text):
    #     self.key = key
    #     self.e_text = e_text
    #     self.d_text = d_text
    # str不是16的倍数那就补足为16的倍数
    def add_to_16(self,value):
        while len(value.encode('utf8')) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    #加密方法
    def encrypt_oracle(self,key,e_text):
        # 初始化加密器
        aes = AES.new(self.add_to_16(key), AES.MODE_ECB)
        #先进行aes加密
        encrypt_aes = aes.encrypt(self.add_to_16(e_text))
        #用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        encrypted_text = encrypted_text.strip() # strip， 后面会有一个换行符
        return encrypted_text

    #解密方法
    def decrypt_oralce(self,key,d_text):
        # 初始化加密器
        aes = AES.new(self.add_to_16(key), AES.MODE_ECB)
        #优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(d_text.encode(encoding='utf-8'))
        #执行解密密并转码返回str
        decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','')
        return decrypted_text