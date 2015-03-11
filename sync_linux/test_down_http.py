#coding: utf8
'''
Created on 2014年10月8日

@author: zcy
'''
import requests
import re
import sqlite3
import os

def down_http(url):
    http = requests.get(url)
    return (http.status_code, http.content)

def down_http_save(url, savepath):
    t = down_http(url)
    #TODO: 检查状态码
    f = open(savepath, "wb")
    f.write(t[1])
    f.close()
    
def split_hash_type(str):
    ret = {}
    # 6741294f4a70f56cde0765535fc145ad              142 main/binary-amd64/Release
    s = " (\w{32})\s*\d* (.*)"
    pattern = re.compile(s, re.M)
    match = pattern.findall(str)
    if match:
        ret["MD5Sum"] = {"dists/trusty/%s" % y:x for x,y in match}
    
    # 3170425d4b924a37384337f140800854c1a10b5e              142 main/binary-amd64/Release  
    s = " (\w{40})\s*\d* (.*)"
    pattern = re.compile(s, re.M)
    match = pattern.findall(str)
    if match:
        ret["SHA1"] = {"dists/trusty/%s" % y:x for x,y in match}
    
    # 4ffe16ad2cd2788c1e35101b72850880e31eac26797c0cde429dc6e435b2ce7f              142 main/binary-amd64/Release
    s = " (\w{64})\s*\d* (.*)"
    pattern = re.compile(s, re.M)
    match = pattern.findall(str)
    if match:
        ret["SHA256"] = {"dists/trusty/%s" % y:x for x,y in match}
        
    return ret

#没在数据库里记录的hash，目前以md5检索
def db_check_hash(dict_hash_info):
    d_md5 = dict_hash_info["MD5Sum"]
    d_sha1 = dict_hash_info["SHA1"]
    d_sha256 = dict_hash_info["SHA256"]
    conn = sqlite3.connect("hash_info.db")
    cursor = conn.cursor()
    for key in d_md5.keys():
        sql = "select md5 from hash where distribution_id=1 and filename='%s'" % key
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            #compare data
            if data[0] != d_md5[key]:
                #down
                #TODO: 这里应该走不到，如果走到了好像应该是错的
                sql = "update hash set md5='%s',sha1='%s',sha256='%s' where filename='%s'" \
                        % (d_md5[key], d_sha1[key], d_sha256[key], key)
                cursor.execute(sql)
                conn.commit()
        else:
            #down file
            if not os.path.exists(os.path.dirname(key)):
                os.makedirs(os.path.dirname(key))
            
            url_pre = "http://archive.ubuntukylin.com:10006/ubuntukylin/"
            print os.path.join(url_pre, key), key
            down_http_save(os.path.join(url_pre, key), key)
            #TODO: check hash
            #insert data
            sql = "insert into hash(distribution_id,filename,md5,sha1,sha256) \
                values(1,'%s','%s','%s','%s')" \
                % (key, d_md5[key], d_sha1[key], d_sha256[key])
            cursor.execute(sql)
            conn.commit()
#     for d in data:
#         if d[0] in d_md5.keys():
#             print "del", d[0]
# #             print dir(dict)
#             print len(d_md5.keys())
#             del d_md5[d[0]]
#             print len(d_md5)
        

if __name__ == '__main__':
#     s = "http://archive.ubuntukylin.com:10006/ubuntukylin/dists/trusty/Release.gpg"
#     s = "http://archive.ubuntukylin.com:10006/ubuntukylin/dists/trusty/Release"
#     t = down_http(s)
#     if t[0]==200:
#         print t[1]
    f = open("Release", "r")
    str = f.read()
    ret = split_hash_type(str)
    db_check_hash(ret)

    import gzip
    f = gzip.open('Packages.gz', 'rb')
    file_content = f.read()
#     print file_content
    f.close()
    
    #.*\n(.*\n)+"
    p_segment = """Package: .*?\n\n"""
    p_filename = "Filename:\s*(.*?)\n"
    p_md5 = "MD5sum:\s*(.*?)\n"
    p_sha1 = "SHA1:\s*(.*?)\n"
    p_sha256 = "SHA256:\s*(.*?)\n"
    match = re.findall(p_segment, file_content, re.S)
    if match:
        d_fileinfo = {}
        d_md5 = {}
        d_sha1 = {}
        d_sha256 = {}
        for line in match:
            s_filename = re.findall(p_filename, line, re.S)[0]
            s_md5 = re.findall(p_md5, line, re.S)[0]
            s_sha1 = re.findall(p_sha1, line, re.S)[0]
            s_sha256 = re.findall(p_sha256, line, re.S)[0]
            d_md5[s_filename] = s_md5
            d_sha1[s_filename] = s_sha1
            d_sha256[s_filename] = s_sha256
        else:
            d_fileinfo["MD5Sum"] = d_md5
            d_fileinfo["SHA1"] = d_sha1
            d_fileinfo["SHA256"] = d_sha256
            db_check_hash(d_fileinfo)