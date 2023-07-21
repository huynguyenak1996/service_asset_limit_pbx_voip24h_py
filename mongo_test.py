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

config = {'hostname':'14.225.251.72','port':'27017','database':'admin'}

config_mongo = config_mongodb(config)

database = connect_to_mongo(config_mongo)
collection = database['cdrdb']
where = {}
# where['_id'] = ObjectId("6417fe0bf11e5be110e98f7a")

#Đặt kích thước batch_size
batch_size = 10000
# Truy vấn dữ liệu và lấy tài liệu với batch_size
result = collection.find(where, batch_size=batch_size)
print(result)
if result:
    for x in result:
        print(x)
else:
    print('không có dữ liệu')

    
    






