### process 
```bash
# ps (process status) 当前时刻进程快照
[root@master1 ~]# ps -ef | head  # e所有进程, f全格式
# UID用户id, PID进程id, PPID父进程id, C进程占用CPU百分比, STIME进程启动时间, 
# TTY进程在那个终端运行 ?表示与终端无关 pts/0表示由网络连接主机进程, TIME进程运行时间, CMD进程完整命令行
UID      PID   PPID   C   STIME   TTY       TIME   CMD
root       1      0   0   Apr21   ?     00:00:04   /sbin/init
root       2      0   0   Apr21   ?     00:00:00   [kthreadd]

[root@master1 ~]# ps -aux | head  # a所有进程, u以用户为主的格式, x不区分终端  
# %CPU进程占用CPU百分比, %MEM进程占用内存百分比, VSZ进程占用的虚拟内存, RSS进程占用的固定内存, STAT进程状态
USER     PID  %CPU  %MEM   VSZ  RSS  TTY  STAT  START  TIME  COMMAND
root       1   0.0   0.0 19364 1540  ?    Ss    Apr21  0:04  /sbin/init
root       2   0.0   0.0     0    0  ?    S     Apr21  0:00  [kthreadd] 

# top 动态显示进程信息
[root@master1 ~]# top
# 系统时间 + 系统运行时间 + 用户数 + 1/5/15分钟系统平均负载
top - 16:05:31 up 692 days, 37 min,  1 user,  load average: 0.20, 0.38, 0.32
# 总进程数(total) + 正在运行进程数(running) + 睡眠进程数(sleeping) + 停止的进程数(stopped) + 僵尸进程数(zombie)
Tasks: 218 total,   2 running, 215 sleeping,   0 stopped,   1 zombie
# 用户空间CPU占比(us) + 内核空间CPU占比(sy) + CPU空置率(id)  
%Cpu(s):  5.5 us,  0.5 sy,  0.0 ni, 94.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 32781920 total,  4626088 free, 14574136 used, 13581696 buff/cache
KiB Swap:  2097148 total,  1604300 free,   492848 used. 15342624 avail Mem 
# PR优先级, NI负值高优先级/正值低优先级, VIRT虚拟内存, RES真实内存, SHR共享内存, S linux进程5种状态(D=不可中断/R=运行/S=睡眠/T=停止/Z=僵尸)  
# %CPU进程占用CPU百分比, %MEM进程占用内存百分比, TIME+进程启动后占用cpu总时间, COMMAND进程完整命令行
  PID  USER      PR  NI    VIRT    RES    SHR  S  %CPU  %MEM    TIME+  COMMAND                                                                                  
32106 clouder+  20   0  8639896   2.9g  84364  S   5.0   9.4    4498:02   java                                                                                     
22292 clouder+  20   0  8347660   2.7g  13644  S   0.7   8.5    1372:14   java                                                                                     
10943 clouder+  20   0  5981184   1.4g  65396  S   0.7   4.4    1207:21   java                                                                                     
29364 hive      20   0  2358756   1.1g  41356  S   0.0   3.6   11:47.05   java                                                                                     
25562 hdfs      20   0  4977904 939212  22764  S   0.0   2.9   13:23.43   java                                                                                     
31207 impala    20   0  1895636 662760  37064  S   0.0   2.0    5:30.01   catalogd                                                                                 
26409 yarn      20   0  1887780 578052  21820  S   0.7   1.8   15:12.75   java                                                                                     
26473 mapred    20   0  1671052 542636  22188  S   0.0   1.7    8:59.98   java                                                                                     
25264 zookeep+  20   0  4070744 451856  11896  S   0.0   1.4    3:12.09   java                                                                                           
# 快捷键
space刷新, c 显示完整命令行, i 不显示idle/zombie进程 
P/M/T 根据CPU使用大小/内存使用大小/累计使用时间排序  
t/m 切换显示CPU/内存, H 切换到线程模式   
q 退出, W 将当前设置写入/root/.toprc
top -c -p 1956,2042  # 每隔3秒显示指定进程的资源使用情况

# nohup
nohup ./aaa.sh &  # 将该脚本放在后台执行,即使关闭当前终端也能继续运行  
jobs -l # 查看当前终端后台任务jobnum,包括running/stopped/Terminated,+是当前任务 -是后一个任务    
kill %jobnum/%PID  # 杀掉进程  
fg %jobnum  # 将后台程序调至前台运行
ctrl + z  # 暂停某个前台运行的命令并放到后台
bg %jobnum  # 调出暂停的后台命令继续执行 

# w
[root@master1 ~]# w
 11:32:35 up 692 days, 20:04,  1 user,  load average: 0.43, 0.21, 0.21
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    10.9.6.148       11:08    3.00s  0.03s  0.00s w
```