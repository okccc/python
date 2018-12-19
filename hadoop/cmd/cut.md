## cut
cut：一个作用于行数据的选取命令  
[参考文档](https://www.cnblogs.com/dong008259/archive/2011/12/09/2282679.html)  
可选参数：  
-b ：以字节为单位进行分割,这些字节位置将忽略多字节字符边界,除非也指定了 -n 标志,  
-c ：以字符为单位进行分割,  
-d ：自定义分隔符,默认为制表符,  
-f  ：与-d一起使用,指定显示哪个区域,  
-n ：取消分割多字节字符,仅和 -b 标志一起使用,如果字符的最后一个字节落在由 -b 标志的 List 参数指示的<br />范围之内,该字符将被写出,否则该字符将被排除,  
cut -d '分隔符' -f fields：用于有特定分隔字符  
cut -c 字符区间：用于排列整齐的信息  
cut三种定位：  
字节（bytes）,选项-b  
字符（characters）,选项-c（如果有中文就只能用-c不能用-b,非中文情况下-c和-b等同）  
域（fields）,选项-f  
案例：  
chenqian@centos01:~$ who  
chenqian pts/0        2018-04-09 11:22 (180.168.11.202)  
lichen   pts/4        2018-01-24 13:42 (mosh [2027])  
lichen   pts/5        2018-01-24 13:42 (mosh [2496])  
chenqian pts/6        2018-04-09 10:00 (180.168.11.202)  
who|cut -b 3                            // 提取每一行的第3个字节  
who|cut -b 3-5,8                      // 提取每一行的第3,4,5,8个字节  
注意：cut会先把-b后面所有的定位进行从小到大排序,然后再提取,who|cut -b 8,3-5结果其实是who|cut -b 3-5,8  
who|cut -b -3                           // 提取前3个字节  
who|cut -b 3-                           // 提取第3个字节到行尾  
chenqian@centos01:~$ cat /etc/passwd | head -5  
root:x:0:0:root:/root:/usr/bin/zsh  
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin  
bin:x:2:2:bin:/bin:/usr/sbin/nologin  
sys:x:3:3:sys:/dev:/usr/sbin/nologin  
sync:x:4:65534:sync:/bin:/bin/sync  
cat /etc/passwd|head -n 5|cut -d ':' -f 1                                   // 按：切割,取第1个字段  
cat /etc/passwd|head -n 5|cut -d ':' -f 1,3-5                             // 按：切割,取第1,3,4,5个字段  
cat /etc/passwd|head -n 5|cut -d ':' -f -2                                  // 按：切割,取前2个字  
