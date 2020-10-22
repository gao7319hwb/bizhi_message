
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class MissionInfoModel(BaseModel):
    def __init__(self, db_connect_key='gao7_picdata', sub_table=None, db_transaction=None):
        super(MissionInfoModel, self).__init__(MissionInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class MissionInfo:

    def __init__(self):
        super(MissionInfo, self).__init__()
        self.ID = 0  # 标识ID
        self.GUID = ""  # GUID
        self.Title = ""  # 任务标题
        self.SubTitle = ""  # 任务副标题
        self.Icon = ""  # 任务图标
        self.PriseGold = 0  # 奖励金币数/次
        self.Times = 0  # 每日可完成次数
        self.IsShow = 0  # 是否发布
        self.Sort = 0  # 排序
        self.Creator = ""  # 添加人
        self.CreateTime = "1900-01-01 00:00:00"  # 添加时间

    @classmethod
    def get_field_list(self):
        return ['ID', 'GUID', 'Title', 'SubTitle', 'Icon', 'PriseGold', 'Times', 'IsShow', 'Sort', 'Creator', 'CreateTime']
        
    @classmethod
    def get_primary_key(self):
        return "ID"

    def __str__(self):
        return "activity_missioninfo_tb"
    