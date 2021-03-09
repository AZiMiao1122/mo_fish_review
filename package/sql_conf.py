import pymysql
import base64
# 数据库配置

host = 'localhost'
port = 3306
username = 'root'
password = 'YXppbWlhbzExMjI=' # base64加密
db_name = 'english_review'

db_connect = pymysql.connect(host=host, port=port, user=username, passwd=base64.b64decode(password).decode('utf-8'),
                             db=db_name)
db_cursor = db_connect.cursor()
