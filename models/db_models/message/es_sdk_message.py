from seven_framework.crypto import *

class EsSdkMessage:
    def __init__(self):
        super(EsSdkMessage, self).__init__()
        self.retainedID = 0  
        self.msgId = 0
        self.msgTitle=""
        self.msgDigest = ""
        self.msgContent =""  
        self.isRead=0
        self.state=0
        self.msgType=0  #消息类型
        self.msgTime = "" #
        self.actionType = 0  #打开类型
        self.addTime = ""
        self.addDateInt = 0  #
        self.pid = 0  
        self.userId = 0 
        self.toUserId = 0  
        self.userName = ""  
        self.profileImageUrl = ""  
        self.userType = 0 
        self.picUrl = ""  
        
    @classmethod
    def get_retainedID(self):
        return str(self.msgId)