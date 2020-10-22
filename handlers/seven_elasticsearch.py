from elasticsearch import Elasticsearch
from seven_framework import config
import ast
import json

class SevenElasticSearch():
    def __init__(self,index_name,doc_type_name):
        host=config.get_value("es")['host']
        port=config.get_value("es")['port']
        hostAddress=["{0}:{1}".format(host,port)]
        self.index_name=index_name
        self.doc_type_name=doc_type_name
        self.es=Elasticsearch(hostAddress,sniffer_timeout=600)
    
    def es_query_data(self,param_body,param_size,param_from_):
        return self.es.search(index=self.index_name,doc_type=self.doc_type_name, body=param_body,size=param_size,from_=param_from_)

    def es_querypage(self,param_body,param_size,param_from_):
        data= self.es.search(index=self.index_name,doc_type=self.doc_type_name, body=param_body,size=param_size,from_=param_from_)
        dic_list=[]
        for item in data['hits']['hits']:
            dic_list.append(item['_source'])
        return dic_list

    def es_querycount(self,param_body):
        count= self.es.count(body=param_body,index=self.index_name,doc_type=self.doc_type_name)
        #print(count)
        return count
    def es_queryrecord(self,key_name,key_value):
        es_body={"query":{"term":{str(key_name):key_value}}}
        data= self.es.search(index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        dic_list=[]
        for item in data['hits']['hits']:
            dic_list.append(item['_source'])
        if len(dic_list)>0:
            return dic_list[0]
        return ""

    def es_update(self,key_id,**param_dict):
        """
        @description: 根据id更新数据
        @param key_id:主键id
        @param param_dict: 更新字段，字典传值
        @return: 更新成功即为True 失败则为False
        @last_editors: HuangWenBin
        """
        es_body={"doc":param_dict}
        result= self.es.update(id=key_id, index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        return result

    def es_update_by_query(self,es_body):
        """
        @description: 根据条件更新数据表
        @param es_body: 更新语句
        @return: 更新成功即为True 失败则为False
        @last_editors: HuangWenBin
        """
        result= self.es.update_by_query(index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        return result

    def es_add(self,id,**param):
        es_body=param
        result=self.es.create(index=self.index_name,doc_type=self.doc_type_name,id=id,body=es_body)

    def es_delete_by_query(self,es_body):
        """
        @description: 根据条件更新数据表
        @param es_body: 更新语句
        @return: 更新成功即为True 失败则为False
        @last_editors: HuangWenBin
        """
        result= self.es.delete_by_query(index=self.index_name,doc_type=self.doc_type_name,body=es_body)
        return result

if __name__ == "__main__":    
    host="http://admin:JwFa6BSq6ypxUpF@tianzhi-elastic.gao7.com"
    port="80"
    hostAddress=["{0}:{1}".format(host,port)]
    index_name="sdk_bizhimessage_202009"
    doc_type_name="ESSdkMessageInfo_202009"
    es=Elasticsearch(hostAddress,sniffer_timeout=600)

    es_body={"script":{"source":"ctx._source['isRead']=1"},"query":{"bool":{"must":[{"term":{"isRead":0}},{"exists":{"field":"isRead"}}]}}}
    data= es.update_by_query(index=index_name,body= es_body,doc_type=doc_type_name)

    print(json.dumps(data['hits']['hits'])) 

    #print(data['hits']['hits'][0])