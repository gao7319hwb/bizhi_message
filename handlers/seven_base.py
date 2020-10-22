from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_framework.redis import *
from handlers.app_des_encrypt import *
from models.seven_model import *
from seven_framework import CodingHelper
import base64

import ast
import random

class SevenBaseHandler(BaseApiHandler):
    """
    @description: 
    @param {type} 
    @return: 
    @last_editors: HuangJingCan
    """
    def options_async(self):
        self.reponse_json_success()

    def check_xsrf_cookie(self):
        return

    def json_dumps(self, rep_dic):
        """
        @description: 用于将字典形式的数据转化为字符串
        @param rep_dic：字典对象
        @return: str
        @last_editors: HuangJingCan
        """
        if hasattr(rep_dic, '__dict__'):
            rep_dic = rep_dic.__dict__
        return json.dumps(rep_dic, ensure_ascii=False, cls=JsonEncoder)

    def reponse_custom(self, rep_dic):
        """
        @description: 输出公共json模型
        @param rep_dic: 字典类型数据
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        self.http_reponse(self.json_dumps(rep_dic))
    
    def reponse_invoke(self, result_code="0", result_message="", data=None):
        """
        @description:输出壁纸客户端数据
        @param result_code:接口码，调用成功（result_code="0"）时，服务端返回的数据
        @param result_message:接口信息，调用不成功（result_code!="0"）时，返回错误信息
        @param data:返回的数据(2+(data).desentrypt)
        @return 将data dumps后加密返回给客户端
        @last_editors: HuangWenBin
        """
        if hasattr(data,"__dict__"):
            data=data.__dict__        
        result_data={}
        result_data["ResultCode"]=result_code
        result_data["ResultMessage"]=result_message
        result_data["Data"]=data
        encrypt=app_des_encrypt()
        self.write("2")
        self.write(encrypt.des_encrypt(self.json_dumps(result_data)))
    
    def get_useragent(self):
        """
        @description:获取app客户端头部信息
        @return：返回头部信息
        @last_editors: HuangWenBin
        """
        user_agent= UserAgentInfo()
        dic_header=self.request.headers
        user_agent1=dic_header._dict["User-Agent1"]
        if user_agent1.startswith("2"):
            user_agent1=user_agent1[1:]
        #dict_useragent={}
        decrypt=app_des_encrypt()
        user_agent1=decrypt.des_decrypt(user_agent1)
        list_str = str.split(CodingHelper.url_decode(user_agent1.decode("unicode_escape'")), "&")

        for item in list_str:
            kv=item.split("=")
            if hasattr(user_agent, kv[0]) and len(kv)==2:
                setattr(user_agent, kv[0], kv[1])
        #user_agent=json.loads(json.dumps(dict_useragent),object_hook=UserAgentInfo)
        return user_agent

    def get_url_param(self,url,param_name):
        url=CodingHelper.url_decode(url)
        list_str = str.split(url,"&")
        for item in list_str:
            kv=item.split("=")
            if len(kv)==2 and kv[0]==param_name:
                return kv[1]        
        return ""

    def get_encrypt_param_int(self,param_name):
        param_value=0
        p=self.get_param("p")
        if p.isspace():
            return param_value
        if p.startswith("2"):
            p=p[1:]

        decrypt=app_des_encrypt()
        p=decrypt.des_decrypt(p)
        list_str = str.split(CodingHelper.url_decode(p.decode("unicode_escape'")), "&")
        
        for item in list_str:
            kv=item.split("=")
            if len(kv)==2 and kv[0]==param_name:
                try:
                    param_value=int(kv[1])
                except:
                    param_value=0
                break
        
        return param_value

    def get_encrypt_param_string(self,param_name):
        param_value=""
        p=self.get_param("p")
        if p.isspace():
            return param_value

        if p.startswith("2"):
            p=p[1:]

        decrypt=app_des_encrypt()
        p=decrypt.des_decrypt(p)
        list_str = str.split(CodingHelper.url_decode(p.decode("unicode_escape'")), "&")

        for item in list_str:
            kv=item.split("=")
            if len(kv)==2 and kv[0]==param_name:
                try:
                    param_value=str(kv[1])
                except:
                    param_value=0
                break        
        return param_value        


    def reponse_common(self, success=True, data=None, error_code="", error_message=""):
        """
        @description: 输出公共json模型
        @param success: 布尔值，表示本次调用是否成功
        @param data: 类型不限，调用成功（success为true）时，服务端返回的数据
        @param errorCode: 字符串，调用失败（success为false）时，服务端返回的错误码
        @param errorMessage: 字符串，调用失败（success为false）时，服务端返回的错误信息
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        if hasattr(data, '__dict__'):
            data = data.__dict__
        template_value = {}
        template_value['success'] = success
        template_value['data'] = data
        template_value['error_code'] = error_code
        template_value['error_message'] = error_message

        rep_dic = {}
        rep_dic['success'] = True
        rep_dic['data'] = template_value

        self.http_reponse(self.json_dumps(rep_dic))

    def reponse_json_success(self, data=None):
        """
        @description: 通用成功返回json结构
        @param data: 返回结果对象，即为数组，字典
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        self.reponse_common(data=data)

    def reponse_json_error(self, error_code="", error_message=""):
        """
        @description: 通用错误返回json结构
        @param errorCode: 字符串，调用失败（success为false）时，服务端返回的错误码
        @param errorMessage: 字符串，调用失败（success为false）时，服务端返回的错误信息
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: HuangJingCan
        """
        self.reponse_invoke(error_code, error_message)

    def reponse_json_error_params(self):
        """
        @description: 通用参数错误返回json结构
        @param desc: 返错误描述
        @return: 将dumps后的数据字符串返回给客户端
        @last_editors: ChenXiaolei
        """
        self.reponse_json_error("params error", "参数错误")

    def redis_init(self, db=None):
        """
        @description: redis初始化
        @return: redis_cli
        @last_editors: HuangJingCan
        """
        host = config.get_value("redis")["host"]
        port = config.get_value("redis")["port"]
        if not db:
            db = config.get_value("redis")["db"]
        password = config.get_value("redis")["password"]
        redis_cli = RedisHelper.redis_init(host, port, db, password)
        return redis_cli

    
    def get_is_test(self):
        """
        @description: 判断是否本地测试
        @return: str
        @last_editors: HuangJianYi
        """
        if self.get_taobao_param().env != "online":
            return True
        return False

    def check_post(self, redis_key, expire=1):
        """
         @description: 请求太频繁校验
         @return: str
         @last_editors: HuangJianYi
         """
        post_value = self.redis_init().get(redis_key)
        if post_value == None:
            return True
        self.redis_init().set(redis_key, 10, ex=expire)
        return False

    def check_lpush(self, queue_name, value, limitNum=100):
        """
         @description: 入队列校验
         @return: str
         @last_editors: HuangJianYi
         """
        list_len = self.redis_init().llen(queue_name)
        if int(list_len) >= int(limitNum):
            return False
        self.redis_init().lpush(queue_name, json.dumps(value))
        return True

    def lpop(self, queue_name):
        """
         @description: 出队列
         @return: str
         @last_editors: HuangJianYi
         """
        result = self.redis_init().lpop(queue_name)
        return result

    def acquire_lock(self, lock_name, acquire_time=10, time_out=5):
        """
        @description: 获取一个分布式锁
        @param lock_name：锁定名称
        @param acquire_time: 客户端等待获取锁的时间
        @param time_out: 锁的超时时间
        @return bool
        @last_editors: HuangJianYi
        """
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_time
        lock = "lock:" + lock_name
        while time.time() < end:
            if self.redis_init().setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.redis_init().expire(lock, time_out)
                return identifier
            if not self.redis_init().ttl(lock):
                self.redis_init().expire(lock, time_out)
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name, identifier):
        """
        @description: 释放一个锁
        @param lock_name：锁定名称
        @param identifier: identifier
        @return bool
        @last_editors: HuangJianYi
        """
        lock = "lock:" + lock_name
        pip = self.redis_init().pipeline(True)
        while True:
            try:
                pip.watch(lock)
                lock_value = self.redis_init().get(lock)
                if not lock_value:
                    return True
                if lock_value.decode() == identifier:
                    pip.multi()
                    pip.delete(lock)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except redis.excetions.WacthcError:
                pass
        return False