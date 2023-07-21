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
    sql = "SELECT s.id,s.datacenter FROM ask_databases as d JOIN ask_staff as s ON d.id = s.datacenter WHERE d.network_master_lan = '192.168.2.113'"
    res = mysql_query_find_all(sql,connection_mysql)
    if res:
        data = []
        for i in res:
            uid = i['id']
            datacenter = i['datacenter']
            # lấy my extention
            sql_extention = "SELECT name FROM ask_extends WHERE staff = '"+str(uid)+"' AND datacenter = '"+str(datacenter)+"'"
            res_extention = mysql_query_find_all(sql_extention, connection_mysql)
            my_extention = []
            if res_extention:
                for e in res_extention:
                    my_extention.append(e['name'])
            sql_did = "SELECT name FROM ask_did WHERE staff = '"+str(uid)+"' AND datacenter = '"+str(datacenter)+"'"
            res_did = mysql_query_find_all(sql_did, connection_mysql)
            my_did = []
            if res_did:
                for d in res_did:
                    my_did.append(d['name'])
            data.append({
                'uid':uid,
                'datacenter':datacenter,
                'my_extention':my_extention,
                'my_did':my_did,
            })
        pprint(data)
    else:
        print('không có dữ liệu')





