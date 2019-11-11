## cut
- cut：作用于行数据的选取命令  
-b：以字节为单位进行分割    
-c：以字符为单位进行分割(处理中文时才用)  
-d：指定分隔符  
-f：指定字段  
- 使用案例  
who | cut -b 3：提取每一 行的第3个字节  
who | cut -b 3-5,8：提取每一行的第3,4,5,8个字节  
who | cut -b -3：提取前3个字节  
who | cut -b 3-：提取第3个字节到行尾  
cat /etc/passwd | head -5 | cut -d ':' -f 1：按冒号切割后取第1个字段    
cat /etc/passwd | head -5 | cut -d ':' -f 1,3-5：按冒号切割取第1345个字段  
cat /etc/passwd | head -5 | cut -d ':' -f -2：按冒号切割取前两个字段  
## sort
- sort：作用于行数据的排序命令  
-b：忽略最前面的空格符  
-f：忽略大小写  
-M：以月份排序  
-n：以数字排序  
-r：反向排序  
-t：分隔符  
-k：以指定列排序  
-u：去重  
- 使用案例  
cat /etc/passwd | sort -t: -k3 | head -5：先将数据以冒号分割,然后按第3列排序  
cat /etc/passwd | sort -t: -k3n | head -5：按第3列升序排序且以数字排序  
cat /etc/passwd | sort -t: -k3nr | head -5：按第3列倒序排序且以数字排序  
cat /etc/passwd | sort -t: -k6.2,6.4 -k 1r | head -5：先以第六列第2~4个字符升序排序再以第一列降序排序  
cat /etc/passwd | sort -t: -k7 -u | head -5：先将数据以冒号分隔,然后按第7列升序排序并去重  
## uniq  
- uniq：对排序过的行数据去重  
-i：忽略大小写  
-c：计数  
-u：只显示不重复的行  
cat access.log | sort | uniq -c：排序后删除重复行并计数  
cat access.log | sort | uniq -u：排序后仅显示不重复的行  
- 使用案例  
cat access.log | awk '{print $8}' | sort | uniq -c | sort -nr：网站状态码统计  
cat access.log | grep "21/Jan/2019" | awk '{print $5}' | sort | uniq -c | sort -nr：查看一天内ip访问数  
cat access/log | grep "21/Mar/2018:0[7-8]" | awk '{print $4}' | grep "404" | sort | uniq -c | sort -nr | wc -l：查看一小时内404数量  
cat access.log | grep "23/Jan/2019" | awk '{print $2}' | cut -c 1-2 | sort | uniq -c | sort -nr | head：查看一天内访问最频繁的时间段  
## grep
- grep(global search re print)：基于行的文本搜索工具  
- 格式: grep -option 'keyword' file  
-c：统计符合要求的行数  
-i：忽略大小写  
-n：输出时带上行号  
-v：选取不包含指定条件的行  
-w：单词强制匹配  
-A2：打印符合要求的行及下面两行  
-B2：打印符合要求的行及上面两行  
-C2：打印符合要求的行及上下各两行  
- 使用案例  
grep -n [0-9] test.txt：选取包含数字的行  
grep -nv [0-9] test.txt：选取不包含数字的行  
grep '[^r]' test.txt：选取不包含某个字符的行  
grep '^import' test.txt: 选取以import开头的行  
grep 'bin$' test.txt：选取以bin结尾的行  
grep -v '^$' test.txt：选取非空行  
grep 'mysql' ./*.sh：查看当前目录下包含mysql的脚本    
<font color=red>grep 'debit_order' *.sql | awk -F: '{print $1}' | uniq -c | sort -nr</font>：查找当前目录下用到debit_order表的sql文件并统计使用次数  
grep error mysql.log --color -A 10 -B 10：高亮显示关键字所在行的前10行和后10行  
grep -wf/-vwf a.log b.log：输出两个文件相同/不同的内容  
## find
- find：在指定目录下按匹配规则查找文件(夹)  
- 格式：find path -option [-print] [-exec command] {} \  
- option  
-maxdepth/mindepth：有时候目录层次很深需要设置目录深度(跟在path后面)  
-type：按类型查找(b块设备/c字符设备文件/d目录/f普通文件/l符号链接文件/p管道文件)  
-name/perm/size/(no)user/(no)group/newer/empty：按名称/权限/大小/所属用户(组)/新旧/空文件查找  
-atime：按天查找(文件的3个时间戳atime/mtime/ctime;amin/mmin/cmin)  
-exec command {} \\; 对查找的结果执行相关操作  
- 使用案例  
find . -type d –print：在当前目录下查找文件夹  
find . ! -type d –print：在当前目录下查找非文件夹  
find . -type l –print：在当前目录下查找链接文件  
find . -type d -exec rm -rf {} \：找到当前目录下的文件夹并删掉  
<font color=red>find / -type f -perm 755 -name 'cloudera*'：查找根目录下cloudera相关可执行命令</font>
find . -type f -atime 5：在当前目录查找刚好5天前访问的文件  
find . -type f -amin -5：在当前目录查找5分钟内访问过的文件  
find . -type f -mtime -5 –print：在当前目录查找5天内修改过的文件  
find . -type f -mtime +5 –print：在当前目录查找5天前修改过的文件  
find . -type f -newer file：在当前目录下查找修改时间比file新的文件  
find . -maxdepth 3 -type f：向下深度最大为3层  
find . -mindepth 2 -type f：向下深度最少为2层  
find . -type f -size +10M –print：查找当前目录大于10M的文件  
find . -empty：查找当前目录下的空文件  
find . -maxdepth 1 -type f -name "*.txt" -exec cat > ./merge.tmp {} \; 合并小文件  
find . -type f -user root -exec chown hdfs {} \; 将当前目录下root用户文件改成hdfs用户  
find . -type f -mtime +180 -name "*.log" -exec rm -rf {} \; 将当前目录下半年前的日志文件删除  
## sed
- sed：基于行的流编辑器(stream editor)  
- 格式：sed -option 'command' file  
- option  
-n：安静模式,不输出全部行而只输出sed操作选中的行  
-e：多重编辑且命令顺序会影响结果  
-f：直接将sed动作写在一个文件内  
-r：让sed命令支持扩展的正则表达式  
<font color=red>-i：sed正常操作只输出结果到屏幕而不改变原文件,-i直接修改文件内容而不是在屏幕输出</font>  
- command  
a\：追加,在选中行的下一行插入字符串  
i\：插入,在选中行的上一行插入字符串  
c\：行替换,将选中的行替换为新的字符串  
d：删除,将选中的行删除  
p：打印,打印当前选择的行,通常结合sed -n使用  
<font color=red>s：字符串替换(可搭配正则使用),全局替换 s/old/new/g</font>  
- 正则表达式  
?：零次或一次,等同于{0,1}  
\*：零次或多次,等同于{0,}  
+：一次或多次,等同于{1,}  
<font color=red>\\：转义下一个字符,在字符串里要写成双斜杠\\</font>  
^：字符串开头,如果在[]内表示取反  
$：字符串结尾  
.：匹配除\n以外的任意单个字符  
[]：匹配内容  
{}：限定次数  
()：子表达式  
\d：匹配任意数字,等同于[0-9]  
\D：匹配任意非数字,等同于[^0-9]  
\w：匹配任意字符,等同于[a-zA-Z0-9_]  
\W：匹配任意非字符,等同于[^a-zA-Z0-9_]  
\s：匹配任意空白字符,等同于[\t\n\r\f]  
\S：匹配任意非空字符,等同于[^\t\n\r\f]  
{n}：刚好n次  
{n,}：至少n次  
{n,m}：至少n次至多m次  
&：保存搜索字符作相应替换,s/love/{&}/,love替换成{love}  
<font color=red>\1表示匹配到的第一个子串,\2表示匹配到的第二个子串</font>  
- 使用案例  
sed '1a\add one' file：在第一行的下一行添加字符串"add one"  
sed '1,$a\add one' file：在所有行的下一行都添加字符串"add one"  
sed '/first/a\add one' file：在包含"first"字符串的行的下一行添加字符串"add one"  
sed '/^ha.*day$/a\add one' file：在以ha开头day结尾的行的下一行添加字符串"add one"  
sed '$c\add one' file：将最后一行替换成字符串"add one"  
sed '4,$c\add one' file：将第四行以后的所有内容替换成字符串"add one",此时文件只剩下4行  
sed '/^ha.*day$/c\add one' file：将以ha开头day结尾的行替换成字符串"add one"  
sed '4,$d' file：删除第四行以后的所有内容  
sed '/^$/d' file：删除所有空白行  
sed '/^ha.*day$/d' file：删除以ha开头day结尾的行  
sed -n '/^ha.*day$/p' file：只打印以ha开头day结尾的行  
sed -e '1,5d' -e 's/test/check/' file：多重编辑且后面操作受前面影响  
sed 's/book/books/g' file：将文件中的所有book替换成books  
sed 's/book/books/2g' file：从第二处匹配的地方开始替换  
sed -i 's/book/books/g' file：直接编辑file,将book替换成books  
echo this is a test line | sed 's/\w\\+/{&}/g'：将选中的单词两边加上大括号  // {this} {is} {a} {test}  
sed 's/(.)line$/\1/g' file：匹配以line结尾的行line前面的部分  
sed 's/(.)is(.)line/\1\2/g' file：匹配is前面和line前面的部分  
echo this is digit 7 in a number | sed 's/digit\([0-9]\)/\1/'：this is 7 in a number  
echo aaa BBB | sed 's/\([a-z]\+\) \([A-Z]\+\)/\2\1/'：交换子串顺序  // BBB aaa  
## awk
- awk：强大的文本分析处理工具,擅长列操作
- 格式：awk [-F | -f | -v] 'BEGIN{} /.../{command1;command2} END{}' file  
-F：操作列的字段分隔符  
-f：调用脚本  
-v：定义变量  
BEGIN：初始化代码块,引用全局变量或设置FS分隔符  
/.../：匹配代码块,字符串或正则表达式  
{...}：命令代码块,多条命令用;分隔  
END：结束代码块,输出最终计算结果  
- 内置变量  
$0：整条记录  
$n：当前记录的第n个字段  
NR：行号  
NF：字段数  
OFS：输出字段分隔符,默认空格,制表符OFS='\t'  
ORS：输出记录分隔符,默认换行,即处理结果一行一行输出到屏幕  
&&：逻辑与  
||：逻辑或  
/aaa/：匹配包含aaa的行、!/aaa/匹配不包含aaa的行  
~/bbb/：匹配指定字段包含bbb的行、!~/bbb/匹配指定字段不包含bbb的行  
printf：%表示格式化输出,-8表示字符长度,s表示字符串类型,\n表示换行  
- 使用案例  
awk 'NR!=1{print}' file：不显示第一行  
awk 'NR>10{print}' file：只显示10行以后的内容  
awk 'END{print NR}' file：显示最后一行行号(统计行数)  
awk 'NR>=10&&NR<=20{print}' a.log：显示日志文件的10~20行  
awk -F: '{print $1 $3}' /etc/passwd：以冒号切割后连着输出指定列不分隔  
awk -F: '{print $1,$3,$5}' /etc/passwd：输出指定列使用空格分隔  
awk -F: '{print $1,$3,$5}' OFS=':' /etc/passwd：输出多个指定列并指定分隔符  
awk '/mysql/{print $0}' /etc/passwd：打印包含mysql的行  
awk '!/mysql/{print $0}' /etc/passwd：打印不包含mysql的行  
awk '/48\d*/{print $0}' /etc/passwd：打印包含数字且以48开头的行  
awk -F: '$1~/mail | mysql/{print $1}' /etc/passwd：打印$1字段是mail或mysql的行  
awk -F: '$1!~/mail | mysql/{print $1}' /etc/passwd：打印$1字段不是mail或mysql的行  
awk -F: '$3>=100{print $3}' /etc/passwd：打印$3>=100的行的第三个字段  
awk -F: '$1~/^m/ && $3>100{print $1,$3}' OFS=":" /etc/passwd：打印$1字段是m开头且$3>100的行的$1和$3字段且以冒号分隔  
awk '/MemFree/{print int($2/1024) "M"}' /proc/meminfo：计算剩余内存大小  
route -n | awk 'NR!=1{print}'  > ./route.txt：将查询结果输出到文件  
ll | awk 'NR!=1 {count+=$5} END{print count,"K"}'：计算当前目录下文件的总大小  
ll | awk 'NR!=1 {count[$3]++} END{for(i in count) print i,count[i]}'：计算当前目录下不同用户的文件数  
ll | awk 'NR!=1 {count[$3]+=$5} END{for(i in count) print i,count[i]}'：计算当前目录下不同用户的文件总大小  
netstat -an | awk '$6=="LISTEN"||NR==1 {printf "%-3s %-10s %-10s %-10s \n",NR,$1,$2,$3}'：格式化输出查询结果  
netstat -an | awk '$6~/CONN | LIST/{count[$6]++} END{for (i in count) print i,count[i]}'：计算指定状态的连接数量  