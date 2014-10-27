#coding: utf8
"""
定期扫描目录
判断文件变化，文件夹监测
更新变化文件
解压文件（是否需要循环解），支持增加压缩格式，
#TODO: 增加是否压缩包标记
"""

"""
数据库中设置各发行版本的根目录存储位置
同时为了扩容做准备，可能分布式存储，需要记录host flag
也考虑加一张表记录host flag与ip的对应关系
工作节点的配置文件中记录当前节点的host flag，自动注册并心跳工作状态，干自己的任务
"""

"""
执行初次hash任务时停止rsync进程和其他可能导致文件变化的进程
考虑是否有必要做全库验证和monitor异常退出可能产生的文件变化监测丢失检测
"""

"""
处理增量文件：分解host flag，root，查找父节点
#TODO: 是否将父节点精确到目录
"""


"""
当前执行进度保存，用于hash任务的大解压文件的任务恢复
数据库中记录任务栈
包文件增加标记，是否全部处理完成
"""