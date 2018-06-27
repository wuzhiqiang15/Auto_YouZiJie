# 数据库连接
import pymysql
import readConfig as readConfig
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()

class MyDB:
    global host, username, password, port, database, readConfig
    host = localReadConfig.get_db("host")
    username = localReadConfig.get_db("username")
    password = localReadConfig.get_db("password")
    port = localReadConfig.get_db("port")
    database = localReadConfig.get_db("database")
    config = {
        'host': str(host),
        'user': username,
        'passwd': password,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    # 连接数据库
    def connectDB(self):
        try:
            self.db = pymysql.connect(**config)
            # 创建数据库的cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(srt(ex))

    # 执行SQL语句
    def executeSQL(self, sql, params):
        self.connectDB()
        # 执行SQL
        self.cursor.execute(sql, params)
        self.db.commit()
        return self.cursor

    # 获取全部的SQL执行结果
    def get_all(self, cursor):
        value = cursor.fetchall()
        return value

    # 获取单个SQL结果
    def get_one(self, cursor):
        value = cursor.fetchone()
        return value

    # 关闭数据库连接
    def closeDB(self):
        self.db.close()
        print("DataBase closed!")