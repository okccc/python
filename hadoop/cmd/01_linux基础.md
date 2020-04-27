### disk
```bash
# / 根目录  
# /bin 可执行命令  
# /boot 内核以及启动所需的文件  
# /dev 设备文件  
# /etc 系统配置文件  
# /home 用户主目录,每个用户都会有一个自己的目录  
# /lib 系统最基本的共享库,几乎所有应用程序都会用到这些共享库  
# /mnt 临时映射文件系统,通常用来挂载使用  
# /opt 安装的外部软件  
# /proc 存储进程和系统信息  
# /root 超级用户主目录  
# /sbin 超级用户的可执行命令  
# /tmp 临时文件  
# /usr (非常重要)存放用户的应用程序,类似windows的program files  
# /var 系统默认日志存放目录,会不断变大

# fdisk
fdisk -l  # 显示磁盘信息  

# df (disk free)
[root@master1 ~]# df -hT  # 显示系统盘类型
# xfs 是业界最先进最具可升级性的文件系统,centos7默认xfs,centos6是ext4
# tmpfs 是不存在于实体硬盘的特殊文件系统,驻守在内存里,速度极快
Filesystem     Type      Size  Used Avail Use% Mounted on
/dev/vda1      xfs        20G   13G  7.3G  64% /
tmpfs          tmpfs      16G     0   16G   0% /dev/shm
/dev/vdb       xfs       500G   63G  438G  13% /data

[root@master1 ~]# df -ht xfs  # 显示指定类型磁盘的使用情况
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        20G   13G  7.3G  64% /
/dev/vdb        500G   63G  438G  13% /data

# du (disk usage)
du -sh  # 查看当前目录占用空间大小
du -sh --time *  # 查看当前目录占用空间大小以及更新时间
du -sh * | sort -rh | head  # 查看当前目录下所有文件与目录并按大小排序
du -h  # 查看当前目录下所有文件大小
du -h -d0,d1,d2 或者 du -h --max-depth=0,1,2  # 查看不同深度目录大小,d0就相当于du -sh  
```