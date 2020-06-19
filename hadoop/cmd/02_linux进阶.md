### $
```bash
$#       # 这个程序的参数个数  
$?       # 执行上一个指令的返回值(0表示正常)  
$0       # 这个程序的执行名字  
$n       # 这个程序的第n个参数值,n=1..9  
$*       # 这个程序的所有参数,此选项参数可超过9个  
$@       # 跟$*类似,但是可以当作数组用  
$$       # 这个程序的PID(脚本运行的当前进程ID号)  
$!       # 执行上一个背景指令的PID(后台运行的最后一个进程的进程ID号)  
$-       # 显示shell使用的当前选项,与set命令功能相同  
```

### iconv  
```bash
-l, --list                  # 所有字符集  
-f, --from                  # 修改前编码  
-t, --to                    # 修改后编码  
-c,                         # 忽略无效字符  
-o, --output                # 输出文件  
-s, --silent                # 安静模式  
  , --verbose               # 显示详细信息  
-?, --help                  # 帮助信息  
  , --usage                 # 使用信息  
-V, --version               # 版本号  
# 案例
iconv -f utf-8 -c -t gbk aaa.csv > bbb.csv  
```

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
# grep(global search re print) - print lines matching a pattern 基于行的文本搜索工具 
# 格式: grep -option 'str/re' file  
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

### find
```bash
# find - search for files in a directory hierarchy 在指定目录下按匹配规则查找文件(夹)  
# 格式：find path -option [-print] [-exec command] {} \  
-type                                           # 按类型查找(b块设备/c字符设备文件/d目录/f普通文件/l符号链接文件/p管道文件)  
-name/perm/size/(no)user/(no)group/newer/empty  # 按名称/权限/大小/所属用户(组)/新旧/空文件查找  
-atime(amin)                                    # 按天/分钟查找(文件的3个时间戳atime/mtime/ctime;amin/mmin/cmin)  
-maxdepth/mindepth                              # 有时候目录层次很深需要设置目录深度 
-exec command {} \;                            # 对查找的结果执行相关操作  
# 案例  
find . -type l                                  # 在当前目录下查找链接文件  
find / -type f -perm 755 -name 'cloudera*'      # 查找根目录下cloudera相关的可执行命令
find . -type f -atime 5                         # 在当前目录查找刚好5天前访问的文件  
find . -type f -mtime -5/+5                     # 在当前目录查找5天内/5天前修改过的文件  
find . -type f -newer a.txt                     # 在当前目录下查找修改时间比a.txt新的文件  
find . -type f -size +10M                       # 查找当前目录大于10M的文件  
find . -empty                                   # 查找当前目录下的空文件  
# 找到当前目录下的文件夹并删掉  
find . -type d -exec rm -rf {} \;
# 合并小文件
find . -maxdepth 3 -type f -name "*.txt" -exec cat > ./merge.txt {} \;
# 将当前目录下root用户文件改成hdfs用户
find . -type f -user root -exec chown hdfs {} \;
# 将当前目录下半年前的日志文件删除                        
find . -type f -mtime +180 -name "*.log" -exec rm -rf {} \;               
```

### sed
```bash
# sed(stream editor) - stream editor for filtering and transforming text 基于行的流编辑器
# 格式：sed -option 'command' file  
-n        # 安静模式,不输出全部行而只输出sed操作选中的行  
-e        # 多重编辑且命令顺序会影响结果  
-f        # 直接将sed动作写在一个文件内  
-r        # 让sed命令支持扩展的正则表达式  
-i        # sed默认是输出结果到屏幕而不改变原文件,-i直接修改文件内容
# command  
a\        # 追加,在选中行的下一行插入字符串  
i\        # 插入,在选中行的上一行插入字符串  
c\        # 行替换,将选中的行替换为新的字符串  
d         # 删除,将选中的行删除  
p         # 打印,打印当前选择的行,通常结合sed -n使用  
s         # 字符串替换(可搭配正则使用),全局替换 s/old/new/g  
&         # 保存搜索字符作相应替换,s/love/{&}/,love替换成{love}  
# 案例  
sed '1a\add one' a.txt                               # 在第一行的下一行添加字符串"add one"  
sed '1,$a\add one' a.txt                             # 在所有行的下一行都添加字符串"add one"  
sed '$c\add one' a.txt                               # 将最后一行替换成字符串"add one"  
sed '4,$c\add one' a.txt                             # 将第四行以后的所有内容替换成字符串"add one",此时文件只剩下4行  
sed '4,$d' a.txt                                     # 删除第四行以后的所有内容  
sed '/^$/d' a.txt                                    # 删除所有空白行  
sed '/first/a\add one' a.txt                         # 在包含"first"字符串的行的下一行添加字符串"add one"  
sed '/^ha.*day$/a\add one' a.txt                     # 在以ha开头day结尾的行的下一行添加字符串"add one"  
sed '/^ha.*day$/c\add one' a.txt                     # 将以ha开头day结尾的行替换成字符串"add one"  
sed '/^ha.*day$/d' a.txt                             # 删除以ha开头day结尾的行  
sed -n '/^ha.*day$/p' a.txt                          # 只打印以ha开头day结尾的行  
sed -e '1,5d' -e 's/test/check/' a.txt               # 多重编辑且后面操作受前面影响  
sed 's/book/books/g' a.txt                           # 将文件中的所有book替换成books  
sed 's/book/books/2g' a.txt                          # 从第二处匹配的地方开始替换  
sed -i 's/book/books/g' a.txt                        # 直接编辑a.txt,将book替换成books  
echo it is test | sed 's/\w\+/{&}/g'                 # 将选中的单词两边加上大括号  {it} {is} {test}  
sed 's/\(\) line/\1/g' a.txt                         # 匹配line前面的部分  
sed 's/\(.*\) is \(.*\) line/\1 \2/g' a.txt          # 匹配is前面和line前面的部分  
echo aa BB | sed 's/\([a-z]\+\) \([A-Z]\+\)/\2 \1/'  # 交换子串顺序  
```

### awk
```bash
# awk - pattern scanning and processing language 擅长列操作的文本分析处理工具
# 格式：awk [-F | -f | -v] 'BEGIN{} /.../{command1;command2} END{}' file  
-F          # 字段分隔符,默认空格  
-f          # 调用脚本  
-v          # 定义变量  
BEGIN       # 初始化代码块,引用全局变量或设置FS分隔符  
/.../       # 匹配代码块,字符串或正则表达式  
{...}       # 命令代码块,多条命令用分号分隔,默认{print}={print $0} 
END         # 结束代码块,输出最终计算结果  
# 内置变量    
$0/$n       # 整行记录/当前行的第n个字段  
NR/NF       # 行号/字段数  
OFS/ORS     # 输出字段分隔符,默认空格,制表符OFS='\t' / 输出记录分隔符,默认换行,即处理结果一行一行输出到屏幕  
&&/||       # 逻辑与/逻辑或  
/aaa/       # 匹配包含aaa的行  !/aaa/匹配不包含aaa的行  
$n~/bbb/    # 匹配指定字段包含bbb的行  $n!~/bbb/匹配指定字段不包含bbb的行  
printf      # %表示格式化输出,-8表示字符长度,s表示字符串类型,\n表示换行  
# 案例  
awk 'NR!=1' a.log                                 # 不显示第一行  
awk 'NR>10' a.log                                 # 只显示10行以后的内容  
awk 'END{print NR}' a.log                         # 显示最后一行行号(统计行数)  
awk 'NR>=10&&NR<=20' a.log                        # 显示日志文件的10~20行  
awk -F: '{print $1 $3}' /etc/passwd               # 以冒号切割后连着输出指定列不分隔  
awk -F: '{print $1,$3,$5}' /etc/passwd            # 输出指定列使用空格分隔  
awk -F: '{print $1,$3,$5}' OFS=':' /etc/passwd    # 输出多个指定列并指定分隔符  
awk '/mysql/' /etc/passwd                         # 打印包含mysql的行  
awk '!/mysql/' /etc/passwd                        # 打印不包含mysql的行  
awk '/48\d*/' /etc/passwd                         # 打印包含数字且以48开头的行  
awk -F: '$1~/mail|mysql/' /etc/passwd             # 打印$1字段是mail或mysql的行  
awk -F: '$1!~/mail|mysql/' /etc/passwd            # 打印$1字段不是mail或mysql的行  
awk -F: '$1~/^m/ && $3>100' /etc/passwd           # 打印$1字段是m开头且$3>100的行  
awk '/MemFree/{print int($2/1024) "M"}' /proc/meminfo  # 计算剩余内存大小  
ll | awk 'NR!=1 {count[$3]++} END{for(i in count) print i,count[i]}'                    # 计算当前目录下不同用户的文件数  
netstat -an | awk '$6=="LISTEN" {printf "%-3s %-5s %-3s %-13s \n",NR,$1,$2,$3}'         # 格式化输出查询结果  
netstat -an | awk '$6~/CONN|LIST/{count[$6]++} END{for (i in count) print i,count[i]}'  # 计算指定状态的连接数量  
```