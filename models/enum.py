from enum import Enum, unique

class MessageType(Enum):
    System = 1000,#系统
    User = 2000,#个人
    UserAndSystem = 999,#个人+系统=所有消息


class ActionType(Enum):    
    none = 0,
    AppStore = 1,
    InnerWebView = 2,
    OutsideWebView = 3,

        #壁纸自定义  PID+序号
    BizhiAlbum = 3701,#专辑
    BizhiKeyword = 3702,#关键字
    BizhiStar = 3703,#星座

    BizhiPicSet = 3704,#图集
    BizhiWallDetail = 3705,#壁纸详情
    BizhiUserDetial = 3706,#用户详情
    