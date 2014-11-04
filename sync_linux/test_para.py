#coding: utf8

import MySQLdb
conn = MySQLdb.Connect(host = "10.255.193.222", port=3306, user="sync", passwd="linux", db="sync_linux")
cursor = conn.cursor(MySQLdb.cursors.DictCursor)
sql = """select t1.pid, t1.id, t1.filename
from t_hashdata t1, t_hashdata t2
where t1.pid=t2.id
order by pid, filename"""
cursor.execute(sql)
data = cursor.fetchall()
# print data

list_tree = []

def find_parent(list_tree, pid):
    for node in list_tree:
        if type(node)==type([]):
            return find_parent(node, pid)
        elif type(node)==type({}):
            if node['id']==pid:
                return node
            if node.has_key('children'):
                return find_parent(node['children'], pid)
        else:
            print 'no this,', pid

def add_node(node):
    parent = find_parent(list_tree, node['pid'])
    if parent:
        if parent.has_key('children'):
            parent['children'].append(node)
        else:
            parent['children'] = [node]
    else:
        list_tree.append(node)

for node in data:
    if node['pid']==29:
        pass
    add_node(node)
    
print list_tree


# zNodes = { 'name':"父节点1 - 展开", 'open':True,
#             'children': [
#                 { 'name':"父节点11 - 折叠",
#                     'children': [
#                         { 'name':"叶子节点111"},
#                         { 'name':"叶子节点112"},
#                         { 'name':"叶子节点113"},
#                         { 'name':"叶子节点114"}
#                     ]},
#                 { 'name':"父节点12 - 折叠",
#                     'children': [
#                         { 'name':"叶子节点121"},
#                         { 'name':"叶子节点122"},
#                         { 'name':"叶子节点123"},
#                         { 'name':"叶子节点124"}
#                     ]},
#                 { 'name':"父节点13 - 没有子节点", 'isParent':True}
#             ]}
# 
d = {1:11, 2:22, 3:33}
# for i in zNodes:
#     print i