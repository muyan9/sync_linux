#coding: utf8
"""
定期扫描目录
判断文件变化，文件夹监测
更新变化文件
解压文件（是否需要循环解），支持增加压缩格式
"""

import gio

# print dir(gio)
for i in dir(gio):
    print i

def directory_changed(monitor, file1, file2, evt_type):
    print 1, evt_type, file1, file2  
 
    if evt_type == gio.FILE_MONITOR_EVENT_CREATED or evt_type == gio.FILE_MONITOR_EVENT_DELETED:
        print "测试成功！"  
        print "变化：",evt_type
        print type(evt_type)
#    
#    
gfile = gio.File(".")
monitor = gfile.monitor_directory(gio.FILE_MONITOR_NONE, None)  
monitor.connect("changed", directory_changed)   
    
import glib
ml = glib.MainLoop()  
ml.run()