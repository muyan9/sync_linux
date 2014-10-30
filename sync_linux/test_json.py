#coding: utf8
import json

import MySQLdb
conn = MySQLdb.Connect(host = "10.255.193.222", port=3306, user="sync", passwd="linux", db="sync_linux")
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path=='/':
                path = curdir + sep + 'index.html'
                print path
                f = open(path)
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".js") or self.path.endswith(".css"):
                path = curdir + sep + self.path
                print path
                f = open(path)
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".html"):
                path = curdir + sep + self.path
                print path
                f = open(path)
                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
                
            if self.path=='data':
                sql = """select t1.id, t1.pid, t1.filename, t1.md5, t1.sha1, t1.sha256, 
t1.filesize, t1.filetype, DATE_FORMAT(t1.add_time, '%Y-%m-%d %H:%i:%s') as add_time
from t_hashdata t1, t_hashdata t2
where t1.pid=t2.id
order by pid, id, filename"""
                cursor.execute(sql)
                data = cursor.fetchall()
                s_json = json.dumps(data,indent=4, )
                self.send_response(200)
                self.send_header('Content-type', 'text/html')#   'text/html')
                self.end_headers()
                self.wfile.write(s_json)
                f.close()
                return

            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
