#coding: utf8
import MySQLdb
import os
import inspect
# from MySQLdb.connections import Connection
# print inspect.getmembers(MySQLdb)
print inspect.getsource(os.path)
conn = MySQLdb.Connect(host = "10.255.193.222", port=3306, user="sync", passwd="linux", db="sync_linux")

path_linux_origin = ""