#coding: utf8
import os
# Animal = Enum('Animal', 'ant bee cat dog')
a = ['iso', 'gz', 'bz2', 'bzip2', 'tar', 'gzip', 'cpio', 'zip', 'cab', 'arj', '7z', 'rpm', 'deb', 'xz', 'lzma', 'lzip', 'lzop']
# class enum_filetype():
#     iso = "iso"
#     zip = "zip"
#     targz = "tar.gz"
#     tarbz2 = "tar.bz2"
#     other = "other"
#     a = {'iso':['iso'], 'zip':['zip'], }
# 
# def _mktemp(type):
#     if not type or type==enum_filetype.other:
#         cmd = '/bin/mktemp -d --suffix _other'
#     else:
#         cmd = '/bin/mktemp -d --suffix _%s' % type
#     
#     return os.popen(cmd).read().strip()
# 
# def unpack_iso(filename):
#     dir_tmp = _mktemp(enum_filetype.iso)
#     os.popen('mount -o loop,ro "%s" %s' % (filename, dir_tmp))
#     return dir_tmp
# 
# def unpack_zip(filename):
#     dir_tmp = _mktemp(enum_filetype.zip)
#     os.popen('unzip "%s" -d %s' % (filename, dir_tmp))
#     return dir_tmp
# 
# def unpack_tarbz2(filename):
#     dir_tmp = _mktemp(enum_filetype.tarbz2)
#     pass
# 
# def unpack_gz(filename):
#     dir_tmp = _mktemp(enum_filetype.tarbz2)
#     gf = gzip.open(filename, 'rb')
# #     data = gf.read()
#     primaryname = os.path.splitext(os.path.basename(path))[0]
#     f = open(os.path.join(dir_tmp, primaryname), 'wb')
#     data = gf.read(1024*1024)
#     while data:
#         f.write(data)
#         data = gf.read(1024*1024)
#     f.close()
#     gf.close()
#     return dir_tmp



"""
  -j, --bzip2                filter the archive through bzip2
  -J, --xz                   filter the archive through xz
      --lzip                 filter the archive through lzip
      --lzma                 filter the archive through lzma
      --lzop
      --no-auto-compress     do not use archive suffix to determine the
                             compression program
  -z, --gzip, --gunzip, --ungzip   filter the archive through gzip
  -Z, --compress, --uncompress   filter the archive through compress
"""
#--recursion
#-C, --directory=DIR

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
        
if __name__ == "__main__":
#TODO: 允许扩展解压种类
    path = "/root/mount/222/NeoKylin-3.2.iso"
    a = unpack_iso(path)
    clean_unpack(a)
    
    path = 'd:/test/unpack/gz/mkinitcpio-0.2.1.tar.gz'
    unpack_gz(path)
