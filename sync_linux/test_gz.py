#coding: utf8
import os 
import gzip 

# def read_gz_file(path): 
#     if os.path.exists(path): 
#         with gzip.open(path, 'rb') as pf: 
#             for line in pf: 
#                 yield line 
#     else: 
#         print('the path [{}] is not exist!'.format(path)) 
# 
# con = read_gz_file() 
# if getattr(con, '__iter__', None):
#     print con 
#     for line in con: 
#         print line


path = 'd:/test/unpack/gz/mkinitcpio-0.2.1.tar.gz'



def unpack_gz(filename):
    #TODO: temp dir
    temp_dir  = ""
    gf = gzip.open(filename, 'rb')
#     data = gf.read()
    primaryname = os.path.splitext(os.path.basename(path))[0]
    f = open(os.path.join(temp_dir, primaryname), 'wb')
    data = gf.read(1024*1024)
    while data:
        f.write(data)
        data = gf.read(1024*1024)
    f.close()
    gf.close()


unpack_gz(path)