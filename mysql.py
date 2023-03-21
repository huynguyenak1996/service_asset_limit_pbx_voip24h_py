import pymysql.cursors
# Kết nối vào database.
connection = pymysql.connect(host='203.162.56.208',
                             user='root',
                             password='report@2018',
                                db='asterisk_center',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
print(connection)
print("connect successful!!")
try:
    with connection.cursor() as cursor:
        # SQL
        sql = "SELECT * FROM ask_staff"
        # Thực thi câu lệnh truy vấn (Execute Query).
        cursor.execute(sql)
        print ("cursor.description: ", cursor.description)
        print()
        for row in cursor:
            print(row)
            break
finally:
    # Đóng kết nối (Close connection).
    connection.close()

# # tạo đối tượng connection
# myconn = MySQLdb.connect(host="203.162.56.208", user="root", passwd="report@2018")
# # in đối tượng connection ra màn hình
# print(myconn)
#
# # tạo đối tượng cursor
# cur = myconn.cursor()
#
# # in đối tượng cursor ra màn hình
# print(cur)