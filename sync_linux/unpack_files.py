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

# def unpack_iso(filename):
#     dir_tmp = _mktemp(enum_filetype.iso)
#     os.popen('mount -o loop,ro "%s" %s' % (filename, dir_tmp))
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
    def unpack_7z(self, filename):
        if not os.path.exists(filename):
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = mktemp()
        
        cmd = '7za x -y -o%(dir_dst)s %(dir_src)s > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        os.popen(cmd)
        
        return dir_tmp
    
    #, flag_recursive=True
    def unpack(self, filename):
        ispack = is_pack(filename)
        if ispack:
            #查找是否有对应类型的解压缩方法，若有，直接动态调用对应的方法
            for i in inspect.getmembers(unpack):
                if i[0] == 'unpack_%s' % ispack:
                    dir_temp = i[1](self, filename)
                    return dir_temp
        
        return None

def is_pack(filename):
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

def mktemp():
    cmd = '/bin/mktemp -d -p /dev/shm/'
    return os.popen(cmd).read().strip()
    
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


o_unpack = unpack()

def do_work(filename, pkgname_parent="", flag_delete=False):
    '''
{
    ('/a.tar.gz', '', 'md5', 'sha1', 'sha256'): 
    [
        {
            ('/a.tar', '/a.tar.gz', 'md5', 'sha1', 'sha256'): 
            [
                {
                    ('/a/b.tar.gz', '/a.tar', 'md5', 'sha1', 'sha256'): 
                    [
                        {
                            ('/b.tar', '/a/b.tar.gz', 'md5', 'sha1', 'sha256'): 
                            [
                                ('/b/f4', '/b.tar', 'md5', 'sha1', 'sha256'), 
                                ('/b/f3', '/b.tar', 'md5', 'sha1', 'sha256')
                            ]
                        }
                    ]
                }, 
                ('/a/f2', '/a.tar', 'md5', 'sha1', 'sha256'), 
                ('/a/f1', '/a.tar', 'md5', 'sha1', 'sha256')
            ]
        }
    ]
}
('/t1', '', 'md5', 'sha1', 'sha256')

'''
    l = []
    d = {}
    for file in walk_dir(filename):
        d_md5 = hash.md5_file(file)
        d_sha1 = hash.sha1_file(file)
        d_sha256 = hash.sha256_file(file)
        filesize = os.stat(file).st_size
        t_filename = file.partition(filename)[2]
        
        if is_pack(file):
            dir_temp = o_unpack.unpack(file)
            pkg_info = (t_filename, pkgname_parent, d_md5, d_sha1, d_sha256, filesize)
            ll = do_work(dir_temp, t_filename, flag_delete=True)
            d[pkg_info] = ll
            l.append(d)
        else:
            l.append((t_filename, pkgname_parent, d_md5, d_sha1, d_sha256))
            if flag_delete:
                removefiles(file)
    else:
        if flag_delete:
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
    l = do_work(path, pkgname_parent='centos', flag_delete=False)
    for i in l :
        print i
    #TODO: not first run, read increment list
    
    #TODO: 有些文件是更新的，如何处理
    #TODO: 加入时间字段，区别历史版本