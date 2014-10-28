#coding: utf8
import os, shutil, inspect
import hash
dict_type_package = {'iso':'7z', 
                     'gz':'7z', 
                     'bz2':'7z',
                     'bzip2':'7z', 
                     'tar':'7z', 
                     'gzip':'7z', 
                     'cpio':'', 
                     'zip':'7z', 
                     'cab':'7z', 
                     'arj':'7z', 
                     '7z':'7z', 
                     'rpm':'', 
                     'deb':'', 
                     'xz':'', 
                     'lzma':'', 
                     'lzip':'', 
                     'lzop':''}

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
class unpack():
    def is_pack(self, filename):
        if not os.path.exists(filename):
            raise IOError("file '%s' not found!" % filename)
        
        l_filename = os.path.splitext(filename)
        if len(l_filename)==2:
            #splitextf分解/root/a.tar.gz的结果是tuple: ('/root/a.tar', '.gz')
            #所以要把扩展名的第一个字符’.’去掉
            extname = l_filename[1][1:]
            if extname in dict_type_package.keys():
                return dict_type_package[extname]
        
        return None
    
    def _mktemp(self):
        cmd = '/bin/mktemp -d -p /dev/shm/'
        return os.popen(cmd).read().strip()
     
    def unpack_7z(self, filename):
        if not os.path.exists(filename):
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = self._mktemp()
        
        cmd = '7za x -y -o%(dir_dst)s %(dir_src)s > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        os.popen(cmd)
        
        return dir_tmp
    
    #, flag_recursive=True
    def unpack(self, filename):
        ispack = self.is_pack(filename)
        if ispack:
            #查找是否有对应类型的解压缩方法，若有，直接动态调用对应的方法
            for i in inspect.getmembers(unpack):
                if i[0] == 'unpack_%s' % ispack:
                    dir_temp = i[1](self, filename)
                    return dir_temp
        
        return None
    
def removefiles(file):
    if os.path.isdir(file):
#         os.removedirs(file)
        shutil.rmtree(file)
    else:
        os.remove(file)

def walk_dir(filename):
    list_files = []
    for root,dirs,files in os.walk(filename):
        for file in files:
            list_files.append(os.path.join(root, file))
            
    return list_files

# def do_work(filename, pkgname_parent="", flag_delete=False):
#     u = unpack()
#     l = []
#     for file in walk_dir(filename):
#         dir_temp = u.unpack(file)
#         if dir_temp:
#             d_md5 = hash.md5_file(file)
#             d_sha1 = hash.sha1_file(file)
#             d_sha256 = hash.sha256_file(file)
# #             pkgname_parent = file.partition(filename)[2][1:]
# #             if pkgname_parent == os.path.basename(file):
# #                 pkgname_parent = ""
#             print pkgname_parent
#             l.append((file, pkgname_parent, d_md5, d_sha1, d_sha256))
#             ll = do_work(dir_temp, file, flag_delete=True)
#             l = l + ll
# #             print file, dir_temp
#         else:
# #             print 'hash:', pkgname_parent, file
#             #TODO: hash it
# #             print 1
#             d_md5 = hash.md5_file(file)
#             d_sha1 = hash.sha1_file(file)
#             d_sha256 = hash.sha256_file(file)
#             t_filename = file.partition(filename)[2]
#             print t_filename
#             l.append((file, pkgname_parent, d_md5, d_sha1, d_sha256))
#             removefiles(file)
#     else:
#         if flag_delete:
# #             print 'removefiles:', filename
#             removefiles(filename)
#             
#     return l

o_unpack = unpack()

def do_work(filename, pkgname_parent="", flag_delete=False):
    l = []
    for file in walk_dir(filename):
        if o_unpack.is_pack(file):
            dir_temp = o_unpack.unpack(file)
            d_md5 = hash.md5_file(file)
            d_sha1 = hash.sha1_file(file)
            d_sha256 = hash.sha256_file(file)
            t_filename = file.partition(filename)[2]
#             if pkgname_parent == os.path.basename(file):
#                 pkgname_parent = ""
            print pkgname_parent
            l.append((t_filename, pkgname_parent, d_md5, d_sha1, d_sha256))
            ll = do_work(dir_temp, file, flag_delete=True)
            l = l + ll
#             print file, dir_temp
        else:
#             print 'hash:', pkgname_parent, file
            #TODO: hash it
#             print 1
            d_md5 = hash.md5_file(file)
            d_sha1 = hash.sha1_file(file)
            d_sha256 = hash.sha256_file(file)
            t_filename = file.partition(filename)[2]
            print t_filename
            t_pkg_parent = pkgname_parent.partition(filename)[2]
            l.append((t_filename, t_pkg_parent, d_md5, d_sha1, d_sha256))
            removefiles(file)
    else:
        if flag_delete:
#             print 'removefiles:', filename
            removefiles(filename)
            
    return l


#TODO: 完成后移到上面去


if __name__ == "__main__":
# #TODO: 允许扩展解压种类
#     clean_unpack(a)
#     u = unpack()
    #delete tmp files and do not remove any origin files
    #TODO: first run, hash all files
    path = "/root/test/unpack/gz"
    l = do_work(path, flag_delete=False)
    for i in l :
        print i
    #TODO: not first run, read increment list