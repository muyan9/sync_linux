#coding: utf8
'''
Created on 2014年10月8日

@author: zcy
'''

import ftplib

def tt(a):
    print len(a), a

if __name__ == '__main__':
    ftp = ftplib.FTP()
    ftp.connect("mirrors.sohu.com", 21)
    ftp.login("anonymous", "")
#     ftp.dir(s_dir)
#     ftp.dir("fedora", tt)
#     print type(s_dir)
#     tt = s_dir.split
#     print tt
    print ftp.pwd()