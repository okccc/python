## sort
sort：一个作用于行数据的排序命名  
格式：sort [option] [file or stdin]  
如果 file 参数指定多个文件,sort会将这些文件连接起来当作一个文件进行排序  
option可选参数：  
-f  ：忽略大小写的差异,例如 A 与 a 视为编码相同；  
-b  ：忽略最前面的空格符部分；  
-M  ：以月份的名字来排序,例如 JAN, DEC 等等的排序方法；  
-n  ：使用『纯数字』进行排序(默认是以文字型态来排序的)；  
-r  ：反向排序；  
-u  ：就是 uniq ,相同的数据中,仅出现一行代表；  
-t  ：分隔符,默认是用 [tab] 键来分隔；  
-k  ：以那个区间 (field) 来进行排序的意思  
案例：  
[grubby@centos01]$ cat /etc/passwd | sort  
abrt:x:173:173::/etc/abrt:/sbin/nologin  
admin:x:510:510::/home/admin:/bin/bash  
adm:x:3:4:adm:/var/adm:/sbin/nologin  
bin:x:1:1:bin:/bin:/sbin/nologin  
chuck:x:506:506::/home/chuck:/bin/bash  
cat /etc/passwd | sort | head -5                             // 默认以第一个数据、字符串、升序  
cat /etc/passwd | sort -t ':' -k 3 | head -5               // 先将数据以：分割,然后按第3列排序  
cat /etc/passwd | sort -t ':' -k 3n | head -5              // 先将数据以：分割,然后按第3列升序排序,且以数字排序  
cat /etc/passwd | sort -t ':' -k 3nr | head -5             // 先将数据以：分割,然后按第3列倒序排序,且以数字排序  
cat /etc/passwd | sort -t':' -k 6.2,6.4 -k 1r | head -5      // 先以第六个域第2~4个字符正向排序,再以第一个域反向排序  
cat /etc/passwd | sort -t':' -k 7 -u | head -5         // 先将数据以：分割,然后按第7列升序排序,且去重  
uniq  
uniq：对排序过的行数据去重,结合sort使用  
格式：uniq [-icu]  
-i   ：忽略大小写  
-c  ：计数  
-u  ：只显示唯一的行  
cat words | sort | uniq -c            // 排序后删除重复行,且在行首显示重复次数  
cat words | sort | uniq -u            // 排序后仅显示不重复的行  
