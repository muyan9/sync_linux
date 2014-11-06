#coding: utf8
import os, json, MySQLdb
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import config

conn = MySQLdb.Connect(host = config.cf.get('database', 'ip'), 
                       port = config.cf.getint('database', 'port'), 
                       user = config.cf.get('database', 'user'), 
                       passwd = config.cf.get('database', 'pass'), 
                       db = config.cf.get('database', 'dbname'))
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

def find_parent(list_tree, pid):
    for node in list_tree:
        if type(node)==type([]):
            return find_parent(node, pid)
        elif type(node)==type({}):
            if node['id']==pid:
                return node
            if node.has_key('children'):
                ret = find_parent(node['children'], pid)
                if ret:
                    return ret
        else:
            print 'no this,', pid

def add_node(list_tree, node):
    parent = find_parent(list_tree, node['pid'])
    if parent:
        if parent.has_key('children'):
            parent['children'].append(node)
        else:
            parent['children'] = [node]
            parent['isParent'] = True
    else:
        list_tree.append(node)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.path = 'index.html' if self.path=='/' else self.path[1:]
            
            if self.path=='data':
                sql = """select t1.pid, t1.id, t1.filename as name, t1.md5, t1.sha1, t1.sha256, 
t1.filesize, t1.filetype, DATE_FORMAT(t1.add_time, '%Y-%m-%d %H:%i:%s') as add_time
from t_hashdata t1""" #, t_hashdata t2
#where t1.pid=t2.id
#""" #order by pid, name
                cursor.execute(sql)
                data = cursor.fetchall()
                list_tree = []
                for node in data:
                    add_node(list_tree, node)
                
                s_json = json.dumps(list_tree,indent=4, )
                self.send_response(200)
                self.send_header('Content-type', 'text/json')#   'text/html')
                self.end_headers()
                self.wfile.write(s_json)
                return
            

            if self.path.endswith(".js"):
                s = 'application/x-javascript'
            
            if self.path.endswith(".css"):
                s = 'text/css'

            if self.path.endswith(".js"):
                s = 'text/html'

            if self.path.endswith(".png"):
                s = 'image/x-png'

            if self.path.endswith(".gif"):
                s = 'image/gif'

            if self.path.endswith(".html"):
                s = 'text/html'
            
            path = os.path.join(os.curdir, self.path)
            
            f = open(path, 'rb')
            self.send_response(200)
            self.send_header('Content-type', s)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

def main():
    try:
        server = HTTPServer(('', config.cf.getint('web_server', 'port')), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
