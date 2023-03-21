import pymongo
import requests
import datetime
import socket
from pprint import pprint
from bson import ObjectId
from fastapi import FastAPI
from model.mongodb_model import *
from model.mysql_model import *

app = FastAPI()
@app.get("/")
async def read_root():
    return {"Hello": "Worldsscxcxc"}

config_mysql_model = {
    'host':'203.162.56.208',
    'user':'root',
    'password':'report@2018',
    'db':'asterisk_center',
}
connection_mysql = getConnection(config_mysql_model)
if connection_mysql:
    sql = "SELECT * FROM ask_staff"
    res = mysql_query_all(sql,connection_mysql,10)
    if res:
        for i in res:
            print(i)
    else:
        print('không có dữ liệu')



#
# config = {'hostname':'14.225.251.72','port':'27017','database':'admin'}
#
# config_mongo = config_mongodb(config)
#
# database = connect_to_mongo(config_mongo)
# collection = database['cdrdb']
# where = {}
# # where['_id'] = ObjectId("6417fe0bf11e5be110e98f7a")
#
# #Đặt kích thước batch_size
# batch_size = 10000
# # Truy vấn dữ liệu và lấy tài liệu với batch_size
# result = collection.find(where, batch_size=batch_size)
#
# if collection.count_documents(where) > 0:
#     for x in result:
#         print(x)
#         break
# else:
#     print('không có dữ liệu')

    
    






