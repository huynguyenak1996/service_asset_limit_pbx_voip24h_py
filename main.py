import pymongo
import requests
import socket
import hashlib
import time
from datetime import datetime
from pprint import pprint
from bson import ObjectId
from fastapi import FastAPI
from model.mongodb_model import *
from model.mysql_model import *

# app = FastAPI()
# @app.get("/")
# async def read_root():
    # return {"Hello": "Worldsscxcxc"}
    
batch_size = 10000
def mongo_users_192_168_0_149(hostname,database,collection):
    config_192_168_0_149 = {'hostname':hostname,'port':'27017','database':database}
    config_mongo = config_mongodb(config_192_168_0_149)
    database = connect_to_mongo(config_mongo)
    collection = database[collection]
    return collection
    
def mongo_cdrdb_pbx(hostname,database,collection):
    config = {'hostname':hostname,'port':'27017','database':database}
    config_mongo = config_mongodb(config)
    database = connect_to_mongo(config_mongo)
    collection = database[collection]
    return collection

def md5(string):
    return hashlib.md5(str(string).encode()).hexdigest()

def sha1(string):
    return hashlib.sha1(str(string).encode()).hexdigest()
    
def where_mongo_cdrdb_pbx(connect,extention,did):
    where = {}
    where_or = []
    where['type'] = {'$in': ['inbound', 'outbound', 'local']}
    where_or = []
    where['src'] = {'$nin': ['*78', '*79', 's', 'v', '*97', '*']}
    where['dst'] = {'$nin': ['*78', '*79', 's', 'v', '*97', '*']}
    ##### Lấy ngày hiện tại
    date_start = datetime.now().replace(day=1).strftime("%Y-%m-%d 00:00:00")
    print(date_start)
    now = datetime.now()
    date_end = now.replace(month=now.month+1).replace(day=1).strftime("%Y-%m-%d 00:00:00")
    print(date_end)
    where['calldate_time'] = {
        '$gte': int(datetime.strptime(date_start,"%Y-%m-%d %H:%M:%S").timestamp()),
        '$lte': int(datetime.strptime(date_end,"%Y-%m-%d %H:%M:%S").timestamp())
    }
    where_or.append({'src': {'$in': extention}})
    where_or.append({'dst': {'$in': extention}})
    where_or.append({'did': {'$in': did}})
    if where_or:
        where['$and'] = [{'$or': where_or}]
    print(where)
    result = connect.find(where, batch_size=batch_size)
    return result


while True:
    ##### lấy danh sách user của tổng đài 
    collection = mongo_users_192_168_0_149('192.168.0.149','admin','users')
    result = collection.find({}, batch_size=batch_size)
    if result:
        for x in result:
            uid = x['uid']
            store_user = sha1(md5(uid))
            extention = x['extention']
            did = x['did']
            ip_lan_pbx = x['ip_lan_pbx']
            ### kiểm tra user profile trong store ko nếu ko thì insert nếu có thì update
            collection_store_profile_cdrdb = mongo_cdrdb_pbx(ip_lan_pbx,store_user,'profile')
            check_store_user = collection_store_profile_cdrdb.find_one({'uid':uid}, batch_size=batch_size)
            if check_store_user:
                update_store_user = collection_store_profile_cdrdb.update_one({'uid':str(uid)},{"$set": x})
            else:
                insert_store_user = collection_store_profile_cdrdb.insert_one(x)
            ##### lấy dữ liệu cdrdb của tổng đài theo tài khoản đó
            start_time = time.time()
            connect_cdrdb = mongo_cdrdb_pbx(ip_lan_pbx,'admin','cdrdb')
            result_cdrdb = where_mongo_cdrdb_pbx(connect_cdrdb,extention,did) 
            end_time = time.time()
            collection_store_cdrdb = mongo_cdrdb_pbx(ip_lan_pbx,store_user,'cdrdb')
            if result_cdrdb:
                ### cập nhật cdrdb vào store đã tạo 
                start_time2 = time.time()
                for i in result_cdrdb:
                    # pprint(i)
                    _id = str(i['_id'])
                    where_store_cdrdb = {}
                    where_store_cdrdb['_id'] = ObjectId(_id)
                    check_store_cdrdb = collection_store_cdrdb.find_one(where_store_cdrdb, batch_size=batch_size)
                    if check_store_cdrdb:
                        update_store_cdrdb = collection_store_cdrdb.update_one(where_store_cdrdb,{"$set":i})
                    else:
                        insert_store_cdrdb = collection_store_cdrdb.insert_one(i)
                end_time2 = time.time()
                print("lấy dữ liệu cdrdb: ", end_time - start_time, "seconds")
                print("cập nhật cdrdb vào store đã tạo: ", end_time2 - start_time2, "seconds")
                print(result_cdrdb.count())
            print(uid)
            # break
    else:
        print('không có dữ liệu')




