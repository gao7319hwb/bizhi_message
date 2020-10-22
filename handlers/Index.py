from handlers.seven_base import *
from handlers.seven_elasticsearch import *

class IndexHandler(SevenBaseHandler):
    def get(self):
        es= SevenElasticSearch()
        query={"query": {"match_all": {}}}
        data= es.es_querypage("bizhi_setpiccomment_*","",query,20,0)
        self.write(data)
        #useragent=self.get_useragent()

"""        if useragent.pid=="70":            
            self.write("最美壁纸")
        else:
            self.write("其他壁纸")"""
