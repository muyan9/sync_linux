#coding: utf8
import os, shutil, inspect
import hash
dict_type_package = {'iso':'iso', 
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
                     'rpm':'rpm', 
                     'drpm':'',
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
        
#         extname = os.path.splitext(filename)[1]
#         if extname == '.iso':
#             cmd = 'mount -oloop,ro %(dir_src)s %(dir_dst)s' % {'dir_src':filename, 'dir_dst':dir_tmp}
#         else:
#             cmd = '7za x -y -o%(dir_dst)s %(dir_src)s > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        cmd = '7za x -y -o%(dir_dst)s %(dir_src)s > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        os.popen(cmd)
        
        return dir_tmp

    def unpack_rpm(self, filename):
        if not os.path.exists(filename):
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = mktemp()
        
        cmd = 'cd %(dir_dst)s && rpm2cpio %(dir_src)s | cpio -di > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        os.popen(cmd)
        
        return dir_tmp

    def unpack_iso(self, filename):
        if not os.path.exists(filename):
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = mktemp()
        #TODO: 考虑用更好的方式，不需拷贝，又能兼顾到即算即删，与下面的删除方法兼容
        cmd = 'mount -oloop,ro %(dir_src)s %(dir_dst)s' % {'dir_src':filename, 'dir_dst':dir_tmp}
        os.popen(cmd)
        dir_tmp1 = mktemp()
        cmd = 'cp -r %s/* %s/' % (dir_tmp, dir_tmp1)
        os.popen(cmd)
        cmd = 'umount %s' % dir_tmp
        os.popen(cmd)
        removefiles(dir_tmp)
        
        return dir_tmp1
    
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
    cmd = '/bin/mktemp -d -p /root/test/unpack/tmp'
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

def do_work(filename, list_data, pkgname_parent="", flag_delete=False):
    '''
{
    ('/a.tar.gz', '', 'md5', 'sha1', 'sha256', 'filesize'): 
    [
        {
            ('/a.tar', '/a.tar.gz', 'md5', 'sha1', 'sha256', 'filesize'): 
            [
                {
                    ('/a/b.tar.gz', '/a.tar', 'md5', 'sha1', 'sha256', 'filesize'): 
                    [
                        {
                            ('/b.tar', '/a/b.tar.gz', 'md5', 'sha1', 'sha256', 'filesize'): 
                            [
                                ('/b/f4', '/b.tar', 'md5', 'sha1', 'sha256', 'filesize'), 
                                ('/b/f3', '/b.tar', 'md5', 'sha1', 'sha256', 'filesize')
                            ]
                        }
                    ]
                }, 
                ('/a/f2', '/a.tar', 'md5', 'sha1', 'sha256', 'filesize'), 
                ('/a/f1', '/a.tar', 'md5', 'sha1', 'sha256', 'filesize')
            ]
        }
    ]
}
('/t1', '', 'md5', 'sha1', 'sha256', 'filesize')

'''
    l = []
    
    for file in walk_dir(filename):
        #FIXME: 判断解压临时存储位置是否能放得下，用一次读取n次计算的方式解决
        if os.path.islink(file):
            os.unlink(file)
            continue
        d_md5 = hash.md5_file(file)
        d_sha1 = hash.sha1_file(file)
        d_sha256 = hash.sha256_file(file)
        filesize = os.stat(file).st_size
        
        cmd= 'file %s | cut -c %s-' % (file, len(file)+3)
        filetype  =os.popen(cmd).read().strip() 

        t_filename = file.partition(filename)[2]
        
        if is_pack(file):
            dir_temp = o_unpack.unpack(file)
            pkg_info = (t_filename, pkgname_parent, d_md5, d_sha1, d_sha256, filesize, filetype)
            ll = do_work(dir_temp,list_data, t_filename, flag_delete=True)
            d = {}
            d[pkg_info] = ll
            l.append(d)
        else:
            l.append((t_filename, pkgname_parent, d_md5, d_sha1, d_sha256, filesize, filetype))
            if flag_delete:
                removefiles(file)
    else:
        if flag_delete:
            removefiles(filename)
#     list_data.append(l)
    return l

def insert_data(node, node_parent_id):
    #('/a/f2', '/a.tar', 'md5', 'sha1', 'sha256', 'filesize'), 
    node_type = type(node)
    if node_type==type(()):
        sql = "insert into t_hashdata\
        (pid, filename, md5, sha1, sha256, filesize, filetype) \
        values(%(pid)s, '%(filename)s', '%(md5)s', \
        '%(sha1)s', '%(sha256)s', %(filesize)s, '%(filetype)s')" \
        % {'pid':node_parent_id, 'filename':node[0], 'md5':node[2], 'sha1':node[3], 
           'sha256':node[4], 'filesize':node[5], 'filetype':node[6]}
        print  sql
        cursor.execute(sql)
        return conn.insert_id()
    elif node_type==type({}):
        key = node.keys()[0]
        value = node[key]
        id = insert_data(key, node_parent_id)
        insert_data(value, id)
    elif node_type==type([]):
        for i in node:
            insert_data(i, node_parent_id)
    else:
        pass
    
import MySQLdb
conn = MySQLdb.Connect(host = "10.255.193.222", port=3306, user="sync", passwd="linux", db="sync_linux")
cursor = conn.cursor()

if __name__ == "__main__":
    #TODO: 允许扩展解压种类
    #delete tmp files and do not remove any origin files
    #TODO: first run, hash all files
    path = "/root/test/unpack/rpm"
    l = do_work(path, [], pkgname_parent='centos', flag_delete=False)
#     print l
    insert_data(l, 2)
    
#     for i in l :
#         print i
    #TODO: not first run, read increment list
    
    #TODO: 有些文件是更新的，如何处理
    #TODO: 加入时间字段，区别历史版本