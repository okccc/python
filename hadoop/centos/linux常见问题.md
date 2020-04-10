## linux常见问题
- <font color=red>crontab脚本运行失败</font>  
原因：crontab读不到相对路径,所以配调度时要写全路径(绝对路径),或者先进入这个目录再执行脚本  
方法一 ：30 01 * * * python /app/data/data-etl/odps-meta-data/task.py -e prod &>> /app/data/data-etl/odps-meta-data/error.log  
方法二：30 01 * * * cd /app/data/data-etl/odps-meta-data/ && python task.py -e prod &>> /app/data/data-etl/odps-meta-data/error.log

- bin/sh^M: bad interpreter: No such file or directory
[解决方案](https://www.cnblogs.com/felixzh/p/6108345.html)

- <font color=red>pip install scrapy报错</font>  
HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Max retries exceeded  
解决：将报错的域名添加到信任列表
pip install --trusted-host files.pythonhosted.org scrapy

- <font color=red>centos中文乱码</font>  
locale 看下当前语言是否是zh_CN,若不是就修改系统默认语言：vim /etc/sysconfig/i18n --> LANG="zh_CN.UTF-8"

- <font color=red>crontab误删除恢复</font>  
查看crontab运行日志：/var/log/cron*  
获取cmd命令：cat /var/log/cron | grep "hdfs" | grep "CMD" | awk -F '(' '{print $3}' | awk -F ')' '{print $1}' | sort -u > cmd.txt  
grep "hdfs": 过滤其他用户  
grep "CMD": 过滤非命令行  
sort -u: 去重

- <font color=red>ImportError: No module named pymysql</font>  
安装了pymysql但是导入错误,是因为安装路径不是python的执行路径,找到安装路径复制过去即可  
cp -r /usr/lib64/python2.7/site-packages/pymysql /usr/lib/python2.7/site-packages/

- <font color=red>SecureCRT无法连接centos虚拟机</font>  
VMWare->编辑->虚拟网络编辑器->VMnet8->NAT模式  
[解决方案](https://blog.csdn.net/r1142/article/details/81000966)

- <font color=red>VMware打不开虚拟机</font>  
开启模块DiskEarly的操作失败 | 虚拟机正在使用中获取所有权失败  
解决：删除虚拟机所在目录的所有.lck文件

- WMware Workstation与Hyper-v不兼容,请先从系统中移除Hyper-v角色,然后再运行VMware Workstation  
[编辑注册表](https://www.jianshu.com/p/fbab3c16f481)

- <font color=red>windows10关闭自动更新</font>  
windows+R -> services.msc -> Windows Update -> 停止并禁用

- <font color=red>git clone报错fatal: The remote end hung up unexpectedly</font>  
原因：git文件太大传输过程缓存不够或者被墙了  
解决：git config --global http.postBuffer 524288000