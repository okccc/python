## awk
- awk：强大的文本分析处理工具,擅长列操作
- 格式：awk [-F|-f|-v] 'BEGIN{} /.../{command1;command2} END{}' file  
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
awk 'NR==5||NR==6{print}' /etc/passwd：只显示第5行和第6行  
awk -F: '{print $1 $3}' /etc/passwd：以冒号切割后连着输出指定列不分隔  
awk -F: '{print $1,$3,$5}' /etc/passwd：输出指定列使用空格分隔  
awk -F: '{print $1,$3,$5}' OFS=':' /etc/passwd：输出多个指定列并指定分隔符  
awk '/mysql/{print $0}' /etc/passwd：打印包含mysql的行  
awk '!/mysql/{print $0}' /etc/passwd：打印不包含mysql的行  
awk '/48\d*/{print $0}' /etc/passwd：打印包含数字且以48开头的行  
awk -F: '$1~/mail|mysql/{print $1}' /etc/passwd：打印$1字段是mail或mysql的行  
awk -F: '$1!~/mail|mysql/{print $1}' /etc/passwd：打印$1字段不是mail或mysql的行  
awk -F: '$3>=100{print $3}' /etc/passwd：打印$3>=100的行的第三个字段  
awk -F: '$1~/^m/ && $3>100{print $1,$3}' OFS=":" /etc/passwd：打印$1字段是m开头且$3>100的行的$1和$3字段且以冒号分隔  
awk '/MemFree/{print int($2/1024) "M"}' /proc/meminfo：计算剩余内存大小  
route -n|awk 'NR!=1{print}'  > ./route.txt：将查询结果输出到文件  
ll | awk 'NR!=1 {count+=$5} END{print count,"K"}'：计算当前目录下文件的总大小  
ll | awk 'NR!=1 {count[$3]++} END{for(i in count) print i,count[i]}'：计算当前目录下不同用户的文件数  
ll | awk 'NR!=1 {count[$3]+=$5} END{for(i in count) print i,count[i]}'：计算当前目录下不同用户的文件总大小  
netstat -an|awk '$6=="LISTEN"||NR==1 {printf "%-3s %-10s %-10s %-10s \n",NR,$1,$2,$3}'：格式化输出查询结果  
netstat -an|awk '$6~/CONN|LIST/{count[$6]++} END{for (i in count) print i,count[i]}'：计算指定状态的连接数量  
 

