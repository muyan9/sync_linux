#coding: utf8
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.conf")
# # 返回所有的section
# s = cf.sections()
# print 'section:', s
# 
# o = cf.options("database")
# print 'options:', o
# 
# v = cf.items("database")
# print 'db:', v
# 
# print '-'*60
# #可以按照类型读取出来
# db_host = cf.get("db", "db_host")
# db_port = cf.getint("db", "db_port")
# db_user = cf.get("db", "db_user")
# db_pass = cf.get("db", "db_pass")
# 
# # 返回的是整型的
# threads = cf.getint("concurrent", "thread")
# processors = cf.getint("concurrent", "processor")
# print cf.items('global')
# print cf.sections()
# print cf.options('global')
# print cf.optionxform("EFS")