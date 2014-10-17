#coding: utf8
import os
# Animal = Enum('Animal', 'ant bee cat dog')

class enum_filetype():
    iso = "iso"
    zip = "zip"
    targz = "targz"
    tarbz2 = "tarbz2"
    other = "other"

def _mktemp(type):
    if not type or type==enum_filetype.other:
        cmd = '/bin/mktemp -d --suffix _other'
    else:
        cmd = '/bin/mktemp -d --suffix _%s' % type
    
    return os.popen(cmd).read().strip()

def unpack_iso(filename):
    dir_tmp = _mktemp(enum_filetype.iso)
    os.popen('mount -o loop,ro "%s" %s' % (filename, dir_tmp))
    return dir_tmp

def unpack_zip(filename):
    dir_tmp = _mktemp(enum_filetype.iso)
    os.popen('unzip "%s" -d %s' % (filename, dir_tmp))
    return dir_tmp

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
    
def clean_unpack(path_dir):
    type = path_dir.split("_")[1]
    if type in enum_filetype.__dict__:
        if enum_filetype.__dict__[type] == enum_filetype.iso:
            os.popen('umount %s' % path_dir)
        os.removedirs(path_dir)
#TODO: 允许扩展解压种类
path = "/root/mount/222/NeoKylin-3.2.iso"
# a = unpack_iso(path)
# clean_unpack(a)
