### xargs
```bash
# linux命令可以从两个地方读取内容：标准输入和命令行参数
# 管道：将|左侧命令的标准输出转换为标准输入,提供给右侧命令作为参数
cat a.txt | grep 'mysql' == grep 'mysql' a.txt  
# 但是很多命令不能接收标准输入而只能接收命令行参数,导致管道无法使用
# xargs：可以将管道传递的标准输入转换为命令行参数传给后面的命令  
-d        # 指定分隔符,默认空格  
-i        # 可以用{}代替管道之前的标准输入
-n        # 参数过多时可以指定每次传递的参数个数  
-p        # 询问是否执行,输入y才真的执行,这样可以看清执行过程  
# 案例
# 杀掉某个用户所有进程
ps -ef | grep ^username | cut -c 10-15 | xargs kill -9
# 查看当前进程有哪些用户
ps -ef | awk '{print $1}' | sort | uniq
# 删除impala日志

```

### cut
```bash
# cut 作用于行数据的选取命令  
-b        # 以字节为单位进行分割  
-c        # 以字符为单位进行分割(处理中文)  
-d        # 指定分隔符  
-f        # 指定字段  
# 案例  
who | cut -b 3      # 提取每一行的第3个字节  
who | cut -b 3-5,8  # 提取每一行的第3,4,5,8个字节  
who | cut -b -3     # 提取前3个字节  
who | cut -b 3-     # 提取第3个字节到行尾  
cat /etc/passwd | head -5 | cut -d ':' -f 1      # 按冒号切割后取第1个字段    
cat /etc/passwd | head -5 | cut -d ':' -f 1,3-5  # 按冒号切割取第1345个字段  
cat /etc/passwd | head -5 | cut -d ':' -f -2     # 按冒号切割取前两个字段  
```

### sort
```bash
# sort 作用于行数据的排序命令  
-b        # 忽略最前面的空格符  
-f        # 忽略大小写  
-M        # 以月份排序  
-n        # 以数字排序(默认是以字符串排序)  
-r        # 反向排序  
-t        # 分隔符  
-k        # 按指定列排序  
-u        # 去重  
# 案例  
cat /etc/passwd | sort -t: -k3 | head -5              # 先将数据以冒号分割,然后按第3列排序  
cat /etc/passwd | sort -t: -k3n | head -5             # 按第3列升序排序且以数字排序  
cat /etc/passwd | sort -t: -k3nr | head -5            # 按第3列倒序排序且以数字排序  
cat /etc/passwd | sort -t: -k6.2,6.4 -k 1r | head -5  # 先以第六列第2~4个字符升序排序再以第一列降序排序  
cat /etc/passwd | sort -t: -k7 -u | head -5           # 先将数据以冒号分隔,然后按第7列升序排序并去重  
```

### uniq  
```bash
# uniq 对排序过的行数据去重,结合sort使用
-i        # 忽略大小写  
-c        # 计数  
-u        # 只显示不重复的行 
# 日志格样式
[30/Jul/2018 04:51:40 -0700] DEBUG    10.9.169.233 -anon- - "HEAD /desktop/debug/is_alive HTTP/1.1" returned in 5ms 
# 统计网站状态码
cat access.log | awk '{print $8}' | sort | uniq -c | sort -nr
# 统计一天内ip访问量排行
cat access.log | grep "21/Jan/2019" | awk '{print $5}' | sort | uniq -c | sort -nr  
# 统计指定时间段404数量
cat access/log | grep "21/Mar/2018 0[7-8]" | awk '{print $4}' | grep "404" | sort | uniq -c | sort -nr | wc -l  
# 统计一天内访问最频繁的时间段
cat access.log | grep "23/Jan/2019" | awk '{print $2}' | cut -c 1-2 | sort | uniq -c | sort -nr | head  
```

### grep
```bash
# grep(global search re print) 基于行的文本搜索工具  
# 格式: grep -option 'keyword' file  
-c        # 统计符合要求的行数  
-i        # 忽略大小写  
-n        # 输出时带上行号  
-v        # 取反
-f        # 对比文件
-x        # 完全相同的行
-w        # 部分单词相同的行
--color   # 高亮显示
-A2       # 打印符合要求的行及下面两行  
-B2       # 打印符合要求的行及上面两行  
-C2       # 打印符合要求的行及上下各两行  
# 案例  
grep -n [0-9] a.txt             # 选取包含数字的行  
grep -nv [0-9] a.txt            # 选取不包含数字的行  
grep '[^r]' a.txt               # 选取不包含某个字符的行  
grep '^import' a.txt            # 选取以import开头的行  
grep 'bin$' a.txt               # 选取以bin结尾的行  
grep -v '^$' a.txt              # 选取非空行  
grep 'mysql' *.sh               # 查看包含mysql的脚本    
# 查找当前目录下用到debit_order表的sql文件并统计使用次数
grep 'debit_order' *.sql | awk -F: '{print $1}' | uniq -c | sort -nr  
# 高亮显示关键字所在行的前10行和后10行
grep error mysql.log --color -A 10 -B 10  
# 输出两个文件都有的行(完全相同/部分相同)  
grep -xf/-wf a.log b.log  
# 输出后面文件有而前面文件没有的行
grep -vxf a.log b.log  
```

