#coding: utf8
import MySQLdb

class db_operate():
    conn = object

    def __init__(self):
        #TODO: get paramiter from config file
        self.conn = MySQLdb.Connect(host = "10.255.193.222", port=3306, user="sync", passwd="linux", db="sync_linux")
        
    def execute_sql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
#         cursor.close()
        
    def fetchall(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def fetchone(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
    
if __name__ == "__main__":
    db = db_operate()
    print db.fetchall("show tables")
    print db.fetchone("show tables")
