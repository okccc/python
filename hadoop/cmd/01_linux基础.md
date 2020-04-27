### netstat
```bash
[root@master1 ~]# netstat | head -5
# 有源TCP连接
Active Internet connections (w/o servers)
# 协议  接收/发送队列(通常是0)  本机地址  外部地址  状态
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 master1.meihao:palace-6 master1.meihaofen:46282 ESTABLISHED
tcp        0      0 master1.meihaofen:53288 master1.meihaofenq:7432 ESTABLISHED
tcp        0      0 master1.meihaofen:39856 namenode1.me:inovaport1 ESTABLISHED
# 有源Unix域套接口(只用于本机通信)
Active UNIX domain sockets (w/o servers)
# 协议  连接到本套接口的进程号  标识  状态  inode  路径
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ]         DGRAM      CONNECTED     9827     /run/systemd/cgroups-agent
unix  2      [ ]         DGRAM                    9864     /run/systemd/shutdownd
unix  2      [ ]         DGRAM      CONNECTED     9427     /run/systemd/notify

-a, --all                     # 列出所有选项
-i, --interface               # 显示接口信息
-l, --listen                  # 只列出监听选项
-n, --not                     # 域名解析:不显示主机端口和用户,全部用数字代替
-p, --process                 # 显示相关连接的进程
-r, --route                   # 显示路由信息
-s, --sort                    # 按照协议分类统计
-t, --tcp                     # 显示tcp相关选项
-u, --udp                     # 显示udp相关选项
-x, --unix                    # 显示unix相关选项

# 查看tcp的数量
netstat -ant | wc -l
# 查看tcp的各种状态统计
netstat -ant | awk '{print $6}' | sort | uniq -c | sort -nr
# 查看连接某服务端口最多的IP地址前10
netstat -ant | grep 'ip:port' | awk '{print $5}' | awk -F: '{print $1}' | sort | uniq -c | sort -nr | head -10
```