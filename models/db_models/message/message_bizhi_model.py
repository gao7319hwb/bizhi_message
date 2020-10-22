
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class MessageBizhiModel(BaseModel):
    def __init__(self, db_connect_key='gao7_sdk', sub_table=None, db_transaction=None):
        super(MessageBizhiModel, self).__init__(MessageBizhi, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class MessageBizhi:

    def __init__(self):
        super(MessageBizhi, self).__init__()
        self.ID = 0  # 主键
        self.GUID = ""  # GUID
        self.PID = 0  # 产品ID
        self.OwnerUserID = 0  # 所属
        self.ToUserID = 0  # 目标用户ID
        self.G7UDID = ""  # 设备标识
        self.ActionType = 0  # 跳转类型
        self.MessageType = 0  # 消息类型
        self.State = 0  # 状态
        self.IsReaded = 0  # 针对个人消息已读
        self.Title = ""  # 标题
        self.Content = ""  # 内容（无表情）
        self.EncodeContent = ""  # 加密内容
        self.LinkUrl = ""  # 消息链接
        self.PicUrl = ""  # 图片链接
        self.ReplyUserLink = ""  # 跳转用户链接
        self.PushStatus = 0  # 推送状态
        self.PushTimes = 0  # 失败次数
        self.ClassID = 0  # 类型编号
        self.AddTime = "1900-01-01 00:00:00"  # 添加时间
        self.PublicTime = "1900-01-01 00:00:00"  # 发布时间
        self.PushTime = "1900-01-01 00:00:00"  # 推送时间
        self.I1 = 0  # 
        self.I2 = 0  # 
        self.I3 = 0  # 
        self.S1 = ""  # 
        self.S2 = ""  # 
        self.S3 = ""  # 
        self.D1 = "1900-01-01 00:00:00"  # 

    @classmethod
    def get_field_list(self):
        return ['ID', 'GUID', 'PID', 'OwnerUserID', 'ToUserID', 'G7UDID', 'ActionType', 'MessageType', 'State', 'IsReaded', 'Title', 'Content', 'EncodeContent', 'LinkUrl', 'PicUrl', 'ReplyUserLink', 'PushStatus', 'PushTimes', 'ClassID', 'AddTime', 'PublicTime', 'PushTime', 'I1', 'I2', 'I3', 'S1', 'S2', 'S3', 'D1']
        
    @classmethod
    def get_primary_key(self):
        return "ID"

    def __str__(self):
        return "sdk_message_bizhi_tb"
    