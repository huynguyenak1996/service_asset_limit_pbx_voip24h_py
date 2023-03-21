import pymysql.cursors

def getConnection(config):
    if config.get('host'):
        host = config.get('host')
        if config.get('user'):
            user = config.get('user')
            if config.get('password'):
                password = config.get('password')
                if config.get('db'):
                    db = config.get('db')
                    connection = pymysql.connect(host=host,user=user,password=password,db=db,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
                    return connection
                else:
                    return "không tìm thấy hoặc thiếu db"
            else:
                return "không tìm thấy hoặc thiếu password"
        else:
            return "không tìm thấy hoặc thiếu user"
    else:
        return "không tìm thấy hoặc thiếu host"

def mysql_query_all(sql,connection,limit=0):
    try:
        with connection.cursor() as cursor:
            # Thực thi câu lệnh truy vấn (Execute Query).
            cursor.execute(sql)
            if limit != 0:
                data = cursor.fetchmany(limit)
            else:
                data = cursor.fetchall()
            return data
    except connection.Error as error:
        print("Failed to read data from table", error)
    finally:
        # Đóng kết nối (Close connection).
        connection.close()

def mysql_query_find_one(sql,connection):
    try:
        with connection.cursor() as cursor:
            # Thực thi câu lệnh truy vấn (Execute Query).
            cursor.execute(sql)
            data = cursor.fetchone()
            return data
    finally:
        # Đóng kết nối (Close connection).
        connection.close()