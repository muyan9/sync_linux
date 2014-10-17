#coding: utf8
import os, sys

def unpack_iso(filename):
    s_in, s_out = os.popen("/bin/mktemp")
    print s_in

def unpack_zip(filename):
    pass

def unpack_targz(filename):
    pass

def unpack_tarbz2(filename):
    pass

def unpack(filename):
    if not filename:
        raise Exception("fdsf")
    l_filename = os.path.splitext(filename)
    if len(l_filename)==2:
        extname = l_filename[1]
    return extname
    
    
    
    
    
path = "/root/a/b/c.exe"
# print unpack(path)
# print unpack_iso(path)


import subprocess
p = subprocess.Popen('d:\\a.bat', stdout=subprocess.PIPE)
print p.stdout.read().decode("gbk")
