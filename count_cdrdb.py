import pymongo
import requests
import socket
import hashlib
import time
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from bson import ObjectId
from model.mongodb_model import *

batch_size = 10000
def mongo_users_192_168_0_149(hostname, database, collection):
    config_192_168_0_149 = {'hostname': hostname, 'port': '27017', 'database': database}
    config_mongo = config_mongodb(config_192_168_0_149)
    database = connect_to_mongo(config_mongo)
    collection = database[collection]
    return collection

def mongo_cdrdb_pbx(hostname, database, collection):
    config = {'hostname': hostname, 'port': '27017', 'database': database}
    config_mongo = config_mongodb(config)
    database = connect_to_mongo(config_mongo)
    collection = database[collection]
    return collection

def md5(string):
    return hashlib.md5(str(string).encode()).hexdigest()
def sha1(string):
    return hashlib.sha1(str(string).encode()).hexdigest()
while True:
    ##### lấy danh sách user của tổng đài
    collection = mongo_users_192_168_0_149('192.168.0.149', 'admin', 'users')
    result = collection.find({}, batch_size=batch_size)
    if result:
        for x in result:
            uid = x['uid']
            store_user = sha1(md5(uid))
            extention = x['extention']
            did = x['did']
            ip_lan_pbx = x['ip_lan_pbx']
            han_muc = x['han_muc']
            han_muc_con_lai = x['han_muc_con_lai']
            collection_store_cdrdb = mongo_cdrdb_pbx(ip_lan_pbx, store_user, 'cdrdb')
            # đánh index cho db mongo
            linkedid = 'linkedid_-1'
            src = 'src_-1'
            dst = 'dst_-1'
            calldate_time = 'calldate_time_-1'
            disposition = 'disposition_-1'
            filezise = 'filezise_-1'
            index_info = collection_store_cdrdb.index_information()
            if linkedid not in index_info:
                collection_store_cdrdb.create_index([('linkedid', -1)])
            if src not in index_info:
                collection_store_cdrdb.create_index([('src', -1)])
            if dst not in index_info:
                collection_store_cdrdb.create_index([('dst', -1)])
            if calldate_time not in index_info:
                collection_store_cdrdb.create_index([('calldate_time', -1)])
            if disposition not in index_info:
                collection_store_cdrdb.create_index([('disposition', -1)])
            if filezise not in index_info:
                collection_store_cdrdb.create_index([('filezise', -1)])
            ### Lấy ngày hiện tại
            date_start = datetime.now().replace(day=1).strftime("%Y-%m-%d 00:00:00")
            date_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S").timestamp()
            time_end = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S").timestamp()
            ## tháng tiếp theo
            now = datetime.now()
            next_month = now.replace(month=now.month + 1).replace(day=1).strftime("%Y-%m-%d 00:00:00")
            pipeline = [
                {
                    "$match": {
                        "calldate_time": {
                            "$gte": datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S").timestamp(),
                            "$lt": datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S").timestamp()
                        },
                        "disposition": "ANSWERED",
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_billsec": {"$sum": "$billsec"}
                    }
                }
            ]
            result = list(collection_store_cdrdb.aggregate(pipeline))
            if len(result) > 0:
                billsec = result[0]['total_billsec']
                total_billsec = str(timedelta(seconds=billsec))
                note = "Tổng thời lượng cuộc gọi là " + total_billsec + " giây"
                if han_muc == 0:
                    user_han_muc = han_muc
                    user_han_muc_con_lai = 0
                    percent_han_muc = '100'
                else:
                    user_han_muc = han_muc
                    if han_muc > billsec:
                        user_han_muc_con_lai = han_muc - billsec
                        percent_han_muc = (user_han_muc_con_lai / user_han_muc) * 100
                collection_store_billsec = mongo_cdrdb_pbx(ip_lan_pbx, store_user, 'billsec')
                collection_store_billsec.update_one({'uid': str(uid)},{"$set": {'total_billsec': total_billsec, 'note': note}})
                where = {}
                where['uid'] = uid
                where['time_end'] = {
                    '$lt': datetime.strptime(next_month, "%Y-%m-%d %H:%M:%S").timestamp(),
                }
                check_store_billsec = collection_store_billsec.find_one(where, batch_size=batch_size)
                if check_store_billsec:
                    param = {
                        'uid': str(uid),
                        'billsec': billsec,
                        'total_billsec': total_billsec,
                        'note': note,
                        'han_muc': user_han_muc,
                        'han_muc_con_lai': user_han_muc_con_lai,
                        'percent_han_muc': str(percent_han_muc) + "%",
                    }
                    update_store_billsec = collection_store_billsec.update_one({'uid': str(uid)}, {"$set": param})
                else:
                    param = {
                        'uid': str(uid),
                        'billsec': billsec,
                        'total_billsec': total_billsec,
                        'note': note,
                        'date_start': date_start,
                        'date_end': date_end,
                        'time_start': time_start,
                        'time_end': time_end,
                        'han_muc': user_han_muc,
                        'han_muc_con_lai': user_han_muc_con_lai,
                        'percent_han_muc': str(percent_han_muc) + "%",
                    }
                    insert_store_billsec = collection_store_billsec.insert_one(param)
                print(percent_han_muc)
            else:
                print("Không có kết quả")
    else:
        print('không có dữ liệu')