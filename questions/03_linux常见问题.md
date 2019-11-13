## linux常见问题
- <font color=red>crontab脚本运行失败</font>  
原因：crontab读不到相对路径，所以配调度时要写全路径（绝对路径），或者先进入这个目录再执行脚本  
方法一 ：30 01 * * * python /app/data/data-etl/odps-meta-data/task.py -e prod &>> /app/data/data-etl/odps-meta-data/error.log  
方法二：30 01 * * * cd /app/data/data-etl/odps-meta-data/ && python task.py -e prod &>> /app/data/data-etl/odps-meta-data/error.log

- bin/sh^M: bad interpreter: No such file or directory
[解决方案](https://www.cnblogs.com/felixzh/p/6108345.html)

- <font color=red>pip install scrapy报错：Could not install packages due to an EnvironmentError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Max retries exceeded</font>
解决：将报错的域名添加到信任列表
pip install --trusted-host files.pythonhosted.org scrapy

- centos中文乱码：locale 看下当前语言是否是zh_CN  
若不是就修改系统默认语言：vim /etc/sysconfig/i18n --> LANG="zh_CN.UTF-8"

- crontab误删除恢复
查看crontab运行日志：/var/log/cron*  
获取cmd命令：cat /var/log/cron | grep "hdfs" | grep "CMD" | awk -F '(' '{print $3}' | awk -F ')' '{print $1}' | sort -u > cmd.txt    
grep "hdfs": 过滤其他用户  
grep "CMD": 过滤非命令行  
sort -u: 去重

- ImportError: No module named PyMySQL
安装了pymysql但是导入错误,是因为安装路径不是python的执行路径,找到安装路径复制过去即可    
cp -r /usr/lib64/python2.7/site-packagespymysql /usr/lib/python2.7/site-packages/

- SecureCRT无法连接centos虚拟机  
VMWare->编辑->虚拟网络编辑器->VMnet8->NAT模式  
[解决方案](https://blog.csdn.net/r1142/article/details/81000966)
