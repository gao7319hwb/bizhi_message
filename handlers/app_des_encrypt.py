from pyDes import des,PAD_PKCS5,CBC
from seven_framework import config
from seven_framework import CodingHelper
import base64

class app_des_encrypt():
    def __init__(self):
        self.des_secret_key=config.get_value("des_encrypt_key")
        self.des_obj = des(self.des_secret_key, CBC, self.des_secret_key,None, padmode=PAD_PKCS5)  # 初始化一个des对象，参数是秘钥，加密方式，偏移， 填充方式

    def des_encrypt(self,content):
        secret_bytes = self.des_obj.encrypt(content.encode())   # 用对象的encrypt方法加密
        return base64.b64encode(secret_bytes)
        
    def des_decrypt(self,content):
        content=base64.b64decode(content)
        secret_bytes = self.des_obj.decrypt(content)   # 用对象的encrypt方法加密
        return secret_bytes

def des_encrypt(content):
        des_secret_key="n84mUckz"
        des_obj = des(des_secret_key, CBC, des_secret_key,None, padmode=PAD_PKCS5)  # 初始化一个des对象，参数是秘钥，加密方式，偏移， 填充方式
        secret_bytes = des_obj.encrypt(content.encode())   # 用对象的encrypt方法加密
        return base64.b64encode(secret_bytes)

def des_decrypt(content):
        des_secret_key="n84mUckz"
        des_obj = des(des_secret_key, CBC, des_secret_key,None, padmode=PAD_PKCS5)  # 初始化一个des对象，参数是秘钥，加密方式，偏移， 填充方式
        content=base64.b64decode(content)
        secret_bytes = des_obj.decrypt(content)   # 用对象的encrypt方法加密
        return secret_bytes

class IndexTest():
    def __init__(self):
        self.name="hwb"
        self.age="35"
        self.sex="男"
if __name__ == "__main__":
    #dic={}
    #dic=IndexTest().__dict__
    strEncrypt="GxpCMzgDXF3/I53CyadN9uXxj7iMWTjcFe8cSag+d79akYs1y0oiOuENHFpjNx6OIdXnqHmVerf8kvw5d+o91Ri4eCoO7jfay9cem5Eci7S49dvaWurZh8QhBoG1KVeWJuJ5RxDvcZvmB4Ie7NmyB5P8Qrsfv1qJHrRW5C88IRhTrCxMiZQq5/P0lE9Id08hWMET8tVDIFrz/1nJHOnBmez+2RTeGB8jM+9SHcYNlXPxi65XkafThJ+OSWOPcAmSwocrWYsdkPw9ug4x+QxCLGgv6sAolxwGK6TcuU0eSMUGEWmHRTxasxRosJsKJZjW2qiH3Vefyj0f/fd2PeFvieIMxUl79OUY85435IcnFseM+vV+x2KxuMZ23XhL5V0plTRhUcPP+3zGNkx61c6KlXb9I3/3blC9624HyY3Av6/LF6cwfXIynlbC+JJmY5086hBq5Kjtc0Ty426UUWodVmHHsb6gS/JaFTAcgMGTERQhEUkFIAfilcdBYryv+nA9iTi22xxlsMLATdmeDXO6/zwv7kWl4h8jPYPmgnIeh7zQkjG1HJzCqQ=="
    result= des_decrypt(strEncrypt)
    name=""
    dict_useragent={}
    dict_str = str.split(CodingHelper.url_decode(
        result.decode("unicode_escape'")), "&")
    for item in dict_str:
        kv = str.split(item, "=")
        dict_useragent[kv[0]] = kv[1]
    


