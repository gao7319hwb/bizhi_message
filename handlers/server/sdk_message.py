from handlers.seven_elasticsearch import *
from handlers.seven_base import *
from models import enum
from models.db_models.message.message_bizhi_model import *
from models.db_models.message.es_sdk_message import *
from seven_framework import CodingHelper
import time

es_index="sdk_bizhimessage_*"
es_doc_type=""

class MessageListHandler(SevenBaseHandler):
    def get_async(self):
        pageSize=30
        pageIndex=0
        useragent=self.get_useragent()
        msgType=self.get_encrypt_param_int("msgType")
        pageIndex=self.get_encrypt_param_int("pageIndex")
        from_=pageIndex*pageSize
        msgTypeTurple=(msgType,)
        userID=int(useragent.login)
        if msgTypeTurple not in enum.MessageType._value2member_map_:
            return self.reponse_invoke(result_code="-1", result_message="msgType参数错误", data=None)
        if msgType==enum.MessageType.User.value[0] and userID<1:
            return self.reponse_invoke(result_code="-1", result_message="用户未登录", data=None)
        if int(useragent.pid)<=0:
            return self.reponse_invoke(result_code="-1", result_message="未知请求", data=None)
        
        index_part=userID%10
        es_index="sdk_bizhimessage_{0}".format(index_part)
        es_doc_type="sdk_user"
        es=SevenElasticSearch(index_name= es_index, doc_type_name=es_doc_type)

        if msgType==enum.MessageType.System.value[0]:
            term_dict={"terms":{"msgType":[1000]}}
        elif msgType==enum.MessageType.User.value[0]:
            term_dict={"terms":{"msgType":[2000]}}
        else:
            term_dict={"terms":{"msgType":[1000,2000]}}

        range_dict={"range":{"addDateInt":{"gte":202001}}}
        must_dict={"must":[term_dict,{"term":{"toUserId":userID}},range_dict]}
        #es_body={"query":{"bool":must_dict}}
        es_body={"query":{"match_all":{}}}
        #print(es_body)
        message_list=es.es_querypage(es_body,pageSize,from_)

        return self.reponse_invoke(data=message_list)

class MessageOperateHandler(SevenBaseHandler):
    def get_async(self):
        msgId=self.get_encrypt_param_int("msgId")
        act=self.get_encrypt_param_int("act")
        msgType=self.get_encrypt_param_int("msgType")#1000-系统  2000-个人
        useragent=self.get_useragent()
        userID=int(useragent.login)
        if msgId<=0:#已读
            return self.reponse_invoke(result_code="ParamError",result_message="msgId不能为空")
        if int(useragent.pid)<=0:
            return self.reponse_invoke(result_code="-1", result_message="未知请求", data=None)
        if act==0:
            es=SevenElasticSearch(index_name= es_index, doc_type_name=es_doc_type)
            record=es.es_queryrecord("msgId",msgId)
            if not record:
                return self.reponse_invoke(result_code="-1", result_message="数据不存在", data=None)
            index=userID%10
            es_index="sdk_bizhimessage_{0}".format(index) 
            es_doc_type="sdk_user"
            es=SevenElasticSearch(index_name= es_index, doc_type_name=es_doc_type)
            result=es.es_update(key_id=record["retainedID"],isRead=1)
            MessageBizhiModel.update_table("IsRead=1","ID={0}".format(msgId))
        elif act==1:#清空
            msgType=2000
            index=userID%10
            es_index="sdk_bizhimessage_{0}".format(index) 
            es_doc_type="sdk_user"
            es=SevenElasticSearch(index_name= es_index, doc_type_name=es_doc_type)
            es_body={"query":{"bool":{"must":[{"term":{"toUserId":userID}},"term":{"msgType":msgType}]}}}
            result= es.es_delete_by_query(es_body)
        elif act==2:#消息全部设为已读(个人消息）
            if userID<1:
                self.reponse_invoke("-1","请先登录")
            index=userID%10
            es_index="sdk_bizhimessage_{0}".format(index) 
            es_doc_type="sdk_user"
            #es_body={"script":{"source":"ctx._source['isRead']=1"},"query":{"bool":{"must":[{"term":{"isRead":0}},{"exists":{"field":"isRead"}}]}}}
            script_dict={"source":"ctx._source['isRead']=1"}
            query_dict={"bool":{"must":[{"term":{"isRead":0}},{"term":{"toUserId":userID}},{"exists":{"field":"isRead"}}]}}
            es_body={"script":script_dict,"query":query_dict}
            es=SevenElasticSearch(index_name= es_index, doc_type_name=es_doc_type)
            result= es.es_update_by_query(es_body=es_body)
            MessageBizhiModel.update_table("IsRead=1","ToUserID={0} AND IsRead=0".format(userID))
        return self.reponse_invoke(data=result)

class MessageCountHandler(SevenBaseHandler):
    def get_async(self):
        useragent=self.get_useragent()
        
        userID=int(useragent.login)
        if userID<=0:
            return self.reponse_invoke("-1","用户未登录")
        
        index_part=userID%10
        es_index="sdk_bizhimessage_{0}".format(index_part)
        es_doc_type="sdk_user"

        must_body={"must":[{"term":{"toUserId":userID}},{"range":{"state":{"gt":-1}}}]}
        es_body={"query":{"bool":must_body}}

        es=SevenElasticSearch(es_index= es_index, doc_type_name=es_doc_type)
        result=es.es_querycount(es_body)
        
        message_count=int(result["count"])
        if message_count>99:
            message_count=99

        count={"count":message_count} 
        return self.reponse_invoke(data=count)

class AddMessageHandler(SevenBaseHandler):
    def get_async(self):
        pid=self.get_encrypt_param_int("pid")
        url=self.get_encrypt_param_string("url")
        content=self.get_encrypt_param_string("content")

        url=url.strip()
        if len(url)==0:
            self.reponse_invoke("-1","url为空，则不插消息") 
        
        url = CodingHelper.url_decode(url)

        tp=self.get_url_param("tp")
        msgTypeStr=self.get_url_param(url,"msgType")
        if len(msgTypeStr.strip())==0:
            self.reponse_invoke("-1","无msgType，则不插消息") 
        msgType=int(msgTypeStr)
        
        toUserID=0
        fromUserID=0
        actionType=int(tp)
        linkUrl=url
        time_now= time.localtime()

        messageEntity= MessageBizhi()
        messageEntity.ToUserID=toUserID
        messageEntity.PID=pid
        messageEntity.OwnerUserID=fromUserID
        messageEntity.MessageType=msgType
        messageEntity.ActionType=actionType
        messageEntity.EncodeContent=content.encode()
        messageEntity.Content=content.replace(r"\p{Cs}", "[表情]")
        messageEntity.LinkUrl=linkUrl
        messageEntity.AddTime=time.strftime("%Y-%m-%d %H:%M:%S",time_now)
        id= MessageBizhiModel.add_entity(messageEntity)
        messageEntity.ID=id
        if id>0:
            es_sdk_message_info=ConvertMessageToESInfo(messageEntity.__dict__)
            es_index="sdk_bizhimessage_public"
            es_doc_type="sdk_system"
            es=SevenElasticSearch(es_index,es_doc_type)
            es.es_add(es_sdk_message_info)

class MessageReportHandler(SevenBaseHandler):
    def get_async(self):
        messageContext=MessageBizhiModel()
        messageInfo= messageContext.get_entity_by_id(2963255)
        self.reponse_invoke(data=messageInfo)

class GetRecordHandler(SevenBaseHandler):
    def get_async(self):
        useragent=self.get_useragent()
        retainedID=self.get_encrypt_param_string("retainedID")
        userID=int(useragent.login)
        if userID<=0:
            return self.reponse_invoke("-1","用户未登录")
        es=SevenElasticSearch(index_name= es_index, doc_type_name=es_doc_type)
        result=es.es_queryrecord(key_name="retainedID",key_value=retainedID)
        return self.reponse_invoke(data=result)

def ConvertMessageToESInfo(**messagebizhi):
    es_sdk_message_info=EsSdkMessage()
    es_sdk_message_info.msgId=messagebizhi["ID"]
    es_sdk_message_info.actionType=messagebizhi["ActionType"]
    es_sdk_message_info.isRead=messagebizhi["IsRead"]
    es_sdk_message_info.retainedID=es_sdk_message_info.get_retainedID()

    pic_url=str(messagebizhi["PicUrl"])
    pic_url_array=[]
    if len(pic_url)!=0:
        pic_url_array=pic_url.split(",")
    msgCount=json.dumps({"LinkUrl":messagebizhi["LinkUrl"],"PicUrl":pic_url_array})
    es_sdk_message_info.msgContent=msgCount

    es_sdk_message_info.msgTitle=messagebizhi["Content"]
    es_sdk_message_info.msgTime=messagebizhi["AddTime"]
    es_sdk_message_info.picUrl=messagebizhi["PicUrl"]
    msgType=int(messagebizhi["MessageType"])
    if msgType<enum.MessageType.System.value[0]:
        msgType=1000
    else:
        msgType=2000
    
    es_sdk_message_info.msgType=msgType
    es_sdk_message_info.state=messagebizhi["State"]
    es_sdk_message_info.toUserId=messagebizhi["ToUserID"]

    pid=messagebizhi["PID"]
    if es_sdk_message_info.msgType==enum.MessageType.System.value[0]:
        es_sdk_message_info.userId=-1
        es_sdk_message_info.profileImageUrl="http://wanmei.yimeitu.cn/Content/Images/wanmei-icon.jpg"
        es_sdk_message_info.userName="玩美壁纸"
        es_sdk_message_info.userType=999
    else:
        es_sdk_message_info.userId=-1
        if pid==70:
            es_sdk_message_info.profileImageUrl="http://p1-ks3.532106.com/cdd6712c011048c2b0aabf980f76054b.jpg"
            es_sdk_message_info.userName="最美壁纸"
        elif pid==75:
            es_sdk_message_info.profileImageUrl="http://p1-ks3.532106.com/7a66b589f5004cebae1437e1c70f8d88.png"
            es_sdk_message_info.userName="口袋壁纸"
        else:
            es_sdk_message_info.profileImageUrl="http://wanmei.yimeitu.cn/Content/Images/wanmei-icon.jpg"
            es_sdk_message_info.userName="玩美壁纸"    