#coding: utf8
'''
Created on 2014年10月8日

@author: zcy
'''

import requests

def down_http(url):
    http = requests.get(url)
    return http.content

def down_http_save(url, savepath):
    t = down_http(url)
    f = open(savepath, "wb")
    f.write(t)
    f.close()
    

if __name__ == '__main__':
#     s = "http://archive.ubuntukylin.com:10006/ubuntukylin/dists/trusty/Release.gpg"
    s = "http://archive.ubuntukylin.com:10006/ubuntukylin/dists/trusty/Release"
#     http = requests.get(s)
#     f = open("a.gpg", "wb")
#     f.write(http.content)
#     f.close()
    down_http_save(s, "fdfd")