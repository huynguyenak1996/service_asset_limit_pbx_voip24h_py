import pymongo
import requests
import paramiko
from pprint import pprint
from bson import ObjectId
from pymongo import MongoClient

from model.mongodb_model import *

# Thông tin kết nối SSH
ssh_host = '222.255.115.84'
ssh_user = 'root'
ssh_pass = 'Voip@Report@092020'
# Thông tin kết nối MongoDB
mongo_host = '192.168.0.149'
# mongo_user = 'root'
# mongo_pass = 'Voip@Report@092020'
mongo_db = 'admin'

# Tạo kết nối SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_host, username=ssh_user, password=ssh_pass)

# Tạo đường hầm SSH
ssh_tunnel = ssh.get_transport().open_channel('direct-tcpip', (mongo_host, 27017))

# Tạo kết nối MongoDB thông qua đường hầm SSH
client = MongoClient('192.168.0.149', 27017)
db = client[mongo_db]
collection = db['users']

result = collection.find({}, batch_size=1000)

# data = {
#     'key1': 'value1',
#     'key2': 'value2',
#     'key3': 'value3'
# }
# result = collection.insert_one(data)
for x in result:
    print(x)


# # Thiết lập thông tin SSH
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('222.255.115.84', username='root', password='Voip@Report@092020')
#
# # Thiết lập thông tin MongoDB
# mongo_client = MongoClient('192.168.0.149', 27017)
# mongo_client.server_info() # kiểm tra kết nối đến MongoDB
#
# # Kết nối tới MongoDB qua SSH
# ssh_port = ssh.get_transport().open_channel('direct-tcpip', ('192.168.0.149', 27017), ('192.168.0.149', 27017))
# mongo_client = MongoClient('192.168.0.149', 27017, serverSelectionTimeoutMS=3000, socketTimeoutMS=3000, connectTimeoutMS=3000, sock_info=ssh_port)
#
# # Kiểm tra kết nối đến MongoDB qua SSH
# mongo_client.server_info()



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
# print(result)
# if result:
#     for x in result:
#         print(x)
# else:
#     print('không có dữ liệu')
