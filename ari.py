import MySQLdb
from datetime import datetime, timedelta
# from pyst import cdr

# Tạo kết nối tới cơ sở dữ liệu Asterisk
db = MySQLdb.connect(host='14.225.251.72', user='root', passwd='Voip24h.vn@dmin', db='asteriskcdrdb')
print(db)
# Lấy thông tin về cuộc gọi trong khoảng thời gian từ 1 giờ trước đến hiện tại
# start_time = datetime.now() - timedelta(hours=1)
# query = MySQLdb.query(start_time)
#
# # In ra thông tin về các cuộc gọi
# for row in query:
#     print('Call from:', row.src)
#     print('Call to:', row.dst)
#     print('Call start time:', row.calldate)
#     print('Call duration:', row.billsec)