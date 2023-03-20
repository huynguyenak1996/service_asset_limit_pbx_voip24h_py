import pymongo
import requests
import datetime
import socket
from pprint import pprint
from fastapi import FastAPI

app = FastAPI()

# Tạo client kết nối đến MongoDB
client = pymongo.MongoClient("mongodb://192.168.2.113:27017/")
# Chọn database và collection để truy vấn
db = client["admin"]
collection = db["cdrdb"]
# Thực hiện truy vấn (ví dụ: tìm kiếm một document)
query = {}

start_time = datetime.datetime.now()

# Đặt kích thước batch_size
batch_size = 10000
# Truy vấn dữ liệu và lấy tài liệu với batch_size
result = collection.find({}, batch_size=batch_size)

# for x in result:
    # store = x['store']
    # db = client[store]
    # col = db["campaign_dialer_admin"]
    # for i in col.find():
    # print(x)
    # break
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)  
print(result)
end_time = datetime.datetime.now()
elapsed_time = end_time - start_time

print(f"Thời gian thực thi: {elapsed_time.total_seconds()} giây")

# response = requests.get('https://www.google.com')
# pprint(result)

# @app.get("/")
# async def read_root():
    # return {"Hello": "Worldsscxcxc"}
    
    






