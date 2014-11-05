#coding: utf8
import os, shutil, inspect, logging
import hash, loggingconfig

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
        logger_unpack_7z = logging.getLogger("unpack_7z")
        if not os.path.exists(filename):
            logger_unpack_7z.error("file '%s' not found!" % filename)
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = mktemp()
        logger_unpack_7z.debug(dir_tmp)
        
#         extname = os.path.splitext(filename)[1]
#         if extname == '.iso':
#             cmd = 'mount -oloop,ro %(dir_src)s %(dir_dst)s' % {'dir_src':filename, 'dir_dst':dir_tmp}
#         else:
#             cmd = '7za x -y -o%(dir_dst)s %(dir_src)s > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        cmd = '7za x -y -o"%(dir_dst)s" "%(dir_src)s" > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        logger_unpack_7z.debug(cmd)
        os.popen(cmd)
        
        logger_unpack_7z.info("%s -> %s" % (filename, dir_tmp))
        
        return dir_tmp

    def unpack_rpm(self, filename):
        logger_unpack_rpm = logging.getLogger("unpack_rpm")
        if not os.path.exists(filename):
            logger_unpack_rpm.error("file '%s' not found!" % filename)
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = mktemp()
        logger_unpack_rpm.debug(dir_tmp)
        cmd = 'cd %(dir_dst)s && rpm2cpio "%(dir_src)s" | cpio -di > /dev/null' % {'dir_src':filename, 'dir_dst':dir_tmp}
        logger_unpack_rpm.debug(cmd)
        os.popen(cmd)
        logger_unpack_rpm.info("%s -> %s" % (filename, dir_tmp))
        
        return dir_tmp

    def unpack_iso(self, filename):
        logger_unpack_iso = logging.getLogger("unpack_iso")
        if not os.path.exists(filename):
            logger_unpack_iso.error("file '%s' not fount!" % filename)
            raise IOError("file '%s' not found!" % filename)
        
        dir_tmp = mktemp()
        logger_unpack_iso.debug(dir_tmp)
        #TODO: 考虑用更好的方式，不需拷贝，又能兼顾到即算即删，与下面的删除方法兼容
        cmd = 'mount -oloop,ro "%(dir_src)s" %(dir_dst)s' % {'dir_src':filename, 'dir_dst':dir_tmp}
        logger_unpack_iso.debug(cmd)
        os.popen(cmd)
        dir_tmp1 = mktemp()
        logger_unpack_iso.debug(dir_tmp1)
        cmd = 'cp -r %s/* %s/' % (dir_tmp, dir_tmp1)
        logger_unpack_iso.debug(cmd)
        os.popen(cmd)
        cmd = 'umount %s' % dir_tmp
        logger_unpack_iso.debug(cmd)
        os.popen(cmd)
        removefiles(dir_tmp)
        logger_unpack_iso.debug("remove %s" % dir_tmp)
        logger_unpack_iso.info("%s -> %s" % (filename, dir_tmp))
        return dir_tmp1
    
    #, flag_recursive=True
    def unpack(self, filename):
        logger_unpack = logging.getLogger("unpack")
        ispack = is_pack(filename)
        logger_unpack.debug("%s is a package!" % filename)
        if ispack:
            #查找是否有对应类型的解压缩方法，若有，直接动态调用对应的方法
            for i in inspect.getmembers(unpack):
                if i[0] == 'unpack_%s' % ispack:
                    logger_unpack.debug("package type : %s" % i[0])
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
    logger_do_work = logging.getLogger("do_work")
    l = []
    
    for file in walk_dir(filename):
        #FIXME: 判断解压临时存储位置是否能放得下，用一次读取n次计算的方式解决
        if os.path.islink(file):
            os.unlink(file)
            logger_do_work.debug('unlink %s' % file)
            continue
        d_md5 = hash.md5_file(file)
        d_sha1 = hash.sha1_file(file)
        d_sha256 = hash.sha256_file(file)
        filesize = os.stat(file).st_size
        
        cmd= 'file "%s" | cut -c %s-' % (file, len(file)+3)
        logger_do_work.debug(cmd)
        filetype =os.popen(cmd).read().strip() 

        t_filename = file.partition(filename)[2]
        
        if is_pack(file):
            dir_temp = o_unpack.unpack(file)
            pkg_info = (t_filename, pkgname_parent, d_md5, d_sha1, d_sha256, filesize, filetype)
            logger_do_work.debug("recursive do_work start: %s", t_filename)
            ll = do_work(dir_temp,list_data, t_filename, flag_delete=True)
            logger_do_work.debug("recursive do_work end: %s", t_filename)
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
    return l

def insert_data(node, node_parent_id):
    logger_insert_data = logging.getLogger("insert_data")
    node_type = type(node)
    if node_type==type(()):
        sql = "insert into t_hashdata1\
        (pid, filename, md5, sha1, sha256, filesize, filetype) \
        values(%(pid)s, '%(filename)s', '%(md5)s', \
        '%(sha1)s', '%(sha256)s', %(filesize)s, '%(filetype)s')" \
        % {'pid':node_parent_id, 'filename':node[0], 'md5':node[2], 'sha1':node[3], 
           'sha256':node[4], 'filesize':node[5], 'filetype':node[6]}
        logger_insert_data.debug(sql)
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
    loggingconfig.config_logging("unpack_and_hash.log", 'debug', 'logs')
    logger = logging.getLogger("main")
    #TODO: 允许扩展解压种类
    #delete tmp files and do not remove any origin files
    #TODO: first run, hash all files
    path = "/root/test/unpack/rpm"
    l = do_work(path, [], pkgname_parent='centos', flag_delete=False)
    import pickle
    pickle.dump(l, open("a.bak", 'wb'))
    insert_data(l, 3)
    
#     for i in l :
#         print i
    #TODO: not first run, read increment list
    
    #TODO: 有些文件是更新的，如何处理
    #TODO: 加入时间字段，区别历史版本