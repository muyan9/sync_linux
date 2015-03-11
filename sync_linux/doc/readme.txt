主文件为unpack_pack.py
源文件中有若干标记，是eclipse编辑器中用于代码提示和错误修正用的提示符：
#TODO:		表示想要做什么，还不太紧急的东西
#FIXME:		表示需要尽快修正的内容，或者bug，或者其他重要或紧急的事

大致的流程：
1、检索目录中的文件夹，并认为所有的文件夹是一个linux发行版；
2、对发行版目录递归检索文件，若文件是压缩包，则递归解压缩扫描文件hash等属性；若不是压缩包，直接扫描hash等属性；
3、扫描完成后形成一个大数据集，格式见data_struct.txt文件，查询语句如下：
select t2.pid as pid, t1.filename as p_filename, t2.id, t2.filename, t2.md5 
from t_hashdata t1, t_hashdata t2
where t2.pid=t1.id
4、将数据集写入数据库中，用id、pid的方式记录数据关系，库结构见db_struct.sql文件，将在下面详述。




当前仅完成了发行版文件夹的首次扫描入库功能，对于持续获得的增量文件和可能有修改变动的文件暂时未做处理

一般来说发行版中的文件有三种可能：
1、下载后不会有任何更改的：如iso、rpm、deb等安装镜像、更新包；
2、下载后会有更新操作的：如yum或apt-get使用的更新记录库文件（ubuntu中的Contents-amd64.gz），和更新源中的hash描述文件等；
3、下载后有删除操作的：如centos5因为版本发行已经很长时间了，实际部署量已经很小，当前版本为5.11，若发布了5.12版本，可能会将原5.11版本的iso、更新文件等对应的5.11版本文件删除，但创建一个指向最新发行版的链接。

以上因素需要在处理增量文件时考虑


可以优化的部分：
1、hash.py：
当前计算了md5、sha1、sha256，但调用的是三个函数，完整读取文件后再计算，对于大文件肯定是处理起来很吃力的，可以写成一个函数并分片读取文件；




当前发行版数据是用rsync从rsync://mirrors.ustc.edu.cn同步的，使用命令如下：
rsync -azS rsync://mirrors.ustc.edu.cn/opensuse/ /sync_linux/opensuse/
rsync -azS rsync://mirrors.ustc.edu.cn/archlinux/ /sync_linux/archlinux/
rsync -azS rsync://mirrors.ustc.edu.cn/ubuntu/ /sync_linux/ubuntu/
......

标准的更新源rsync是带--delete参数的，表示当同步源已将之前存在的文件删除后，本地文件也做删除处理，而我们之前的设想是保留历史发行的所有文件，不做删除处理，这是导致存储量非常庞大的重要原因，可以根据需求决定如何设置此参数。


处理增量文件的几种思路：
1、对比文件树和库中记录；
2、同步开始前记录时间点，同步完成后用find或其他方式搜索修改时间大于该时间的文件，即为更新的文件；
3、目录监控，记录所有被改动的文件名；
4、保留rsync日志，搜寻路径，参数中有支持这个功能的设置；
5、若rsync支持同步时使用脚本控制一些动作，也许可以每更新一个文件调用一次处理脚本（不确定）；