## awk

awk: 对文件或字符串做分析和处理,擅长列(域,字段)操作;  
格式: awk [-F|-f|-v] 'BEGIN{} /.../{command1; command2} END{}' file  
     -F域分隔符,默认空格(有时要用: );-f调用脚本,-v定义变量 var=value;  
'': 引用整个代码块  
BEGIN: 初始化代码块;在对每一行进行处理之前,初始化代码,主要是引用全局变量,设置FS分隔符  
/.../: 匹配代码块;可以是字符串或正则表达式  
{...}: 命令代码块;包含一条或多条命令,多条命令用;分隔  
END: 结尾代码块;在对每一行进行处理之后再执行的代码块,主要是最终计算或输出结果信息
内置变量:   
$0: 整条记录  
$n: 当前记录的第n个字段  
NR: 行号  
NF: 字段数  
OFS: 输出字段分隔符, 默认空格,制表符OFS='\t'  
ORS: 输出记录分隔符,默认换行,即处理结果一行一行输出到屏幕  
-F'[:#/]': 定义三个分隔符  
~    :  匹配,与==相比不是精确比较  
!~   : 不匹配,不精确比较  
==  : 等于,必须全部相等,精确比较  
!=   : 不等于,精确比较  
&& : 逻辑与  
||     : 逻辑或  
+    : 匹配时表示1个或1个以上  
/[0-9][0-9]+/: 两个或两个以上数字  
/[0-9][0-9]*/ : 一个或一个以上数字(+ * 只作用于前面一个数字)  
awk 'NR!=1 {print}'									//不显示第一行  
awk 'END{ print NR }' file							//统计文件行数  
awk -F: 'NR==5 || NR==6{print}'  /etc/passwd        //显示第5行和第6行  
print $NF											//打印出一行中的最后一个字段,$(NF-1)倒数第二个字  
awk -F: 'NF==4 {print }' /etc/passwd				//显示只有4个字段的行  
awk -F: '{print $1 $3}'  /etc/passwd				//$1与$3连着输出,不分隔  
awk -F: '{print $1,$3}'  /etc/passwd				//$1与$3使用空格分隔  
awk -F: '{print $1"\t"$3}'  /etc/passwd			    //$1与$3使用\t分隔  
awk -F: '{ print $1,$3 }' OFS='\t' /etc/passwd		//同上  
/.../匹配代码块:   
//纯字符匹配   !//纯字符不匹配   ~//字段值匹配    !~//字段值不匹配   ~/a1|a2/字段值匹配a1或a2  
awk '/mysql/' /etc/passwd  
awk '/mysql/{print}' /etc/passwd  
awk '/mysql/{print $0}' /etc/passwd                  	     //三条指令结果一样  
awk '!/mysql/{print $0}' /etc/passwd                  		 //输出不匹配mysql的行  
awk '/[2][7][7]*/{print $0}' /etc/passwd               		 //匹配包含27为数字开头的行,如27,277,2777...  
awk -F: '$1~/mail/{print $1}' /etc/passwd          			 //$1匹配指定内容才显示  
awk -F: '{if($1~/mail/) print $1}' /etc/passwd   			 //与上面相同  
awk -F: '$1!~/mail/{print $1}' /etc/passwd        		     //不匹配  
awk -F: '$1!~/mail|mysql/{print $1}' /etc/passwd  		     //同上  
条件表达式:   
==   !=   >   >=  
awk -F: '$1=="mysql"{print $3}' /etc/passwd  
awk -F: '{if($1=="mysql") print $3}' /etc/passwd             //与上面相同  
awk -F: '$1!="mysql"{print $3}' /etc/passwd                  //不等于  
awk -F: '$3>1000{print $3}' /etc/passwd                      //大于  
awk -F: '$3>=100{print $3}' /etc/passwd                      //大于等于  
awk -F: '$3<1{print $3}' /etc/passwd                         //小于  
awk -F":" '$3<=1{print $3}' /etc/passwd                      //小于等于  
逻辑运算符:   
&&　||  
awk -F: '$1~/mail/ && $3>8 {print }' /etc/passwd         //逻辑与,$1匹配mail,并且$3>8  
awk -F: '{if($1~/mail/ && $3>8) print }' /etc/passwd  
awk -F: '$1~/mail/ || $3>1000 {print }' /etc/passwd       //逻辑或  
awk -F: '{if($1~/mail/ || $3>1000) print }' /etc/passwd  
数值运算:   
awk -F: '$3 > 100' /etc/passwd  
awk -F: '$3 > 100 || $3 < 5' /etc/passwd  
awk -F: '$3+$4 > 200' /etc/passwd  
awk -F: '/mysql|mail/{print $3+10}' /etc/passwd                     //第三个字段加10打印
awk -F: '/mysql/{print $3-$4}' /etc/passwd                          //减法
awk -F: '/mysql/{print $3*$4}' /etc/passwd                          //求乘积
awk '/MemFree/{print $2/1024}' /proc/meminfo                        //除法
awk '/MemFree/{print int($2/1024)}' /proc/meminfo                   //取整
输出处理结果到文件:   
①在命令代码块中直接输出    route -n|awk 'NR!=1{print > "./fs"}'  
②使用重定向进行输出           route -n|awk 'NR!=1{print}'  > ./fs  
格式化输出:   
netstat -anp|awk '{ printf "%-8s %-8s %-10s\n",$1,$2,$3 }'  
printf表示格式化输出,%表示格式化输出,-8长度为8个字符,s表示字符串类型,\n是换行  
netstat -anp|awk '$6=="LISTEN" || NR==1 {printf "%-10s %-10s %-10s \n",$1,$2,$3}'  
netstat -anp|awk '$6=="LISTEN" || NR==1 {printf "%-3s %-10s %-10s %-10s \n",NR,$1,$2,$3}'  
案例:   
统计/etc/passwd的账户人数:   
awk 'BEGIN {count=0} {count+=1} END{print "total user count is ",count}' /etc/passwd  
total user count is  44  
统计当前目录下文件总大小:   
ll | awk 'NR!=1 && !/^d/{sum+=$5} END {print "the total size is :",int(sum/1024/1024),"M"}'  
,表示输出结果以空格分隔,不然就是连着输出,不分隔         int表示取整  
统计当前目录下不同用户的文件总数: (要用到for循环遍历)  
ll | awk 'NR!=1 && !/^d/{sum[$3]++} END {for(i in sum)printf "%-10s %-5s \n",i,sum[i]}'  
统计当前目录下不同用户的文件总大小:   
ll | awk 'begin{sum=0} NR!=1 && !/^d/{sum[$3]+=$5} END {for(i in sum) printf "%-10s %-5s %-3s \n",i,int(sum[i]/1024/1024),"M"}'  
统计netstat -anp 状态为LISTEN和CONNECT的连接数量:   
netstat -an | awk '$6~/CONNECT|LISTEN/{sum[$6]++} END {for(i in sum) printf "%-10s %-6s \n",i,sum[i]}'  
next语句:   
循环逐行匹配时next会跳过当前行,直接忽略下面语句,而进行下一行匹配,多用于合并操作;  
cat text.txt  
a  
b  
c  
d  
e  
awk 'NR%2==1{next}{print NR,$0;}' text.txt  
2 b  
4 d  
流程控制语句:   
很多要控制流程走向的shell程序都可以交给awk,而且性能很快;  
if判断:   
awk 'BEGIN{  
test=100;  
if(test>90){  
  print "very good";  
  }  
  else if(test>60){  
    print "good";  
  }  
  else{  
    print "no pass";  
  }  
}'  
very good  
for循环:   
awk 'BEGIN{  
total=0;  
for(i=0;i<=100;i++){  
  total+=i;  
}  
print total;  
}'  
5050  
do循环:   
awk 'BEGIN{  
total=0;  
i=0;  
do {total+=i;i++;} while(i<=100)  
  print total;  
}'  
5050  
数组:   
cat /etc/passwd  
root:x:0:0:root:/root:/bin/bash  
bin:x:1:1:bin:/bin:/sbin/nologin  
daemon:x:2:2:daemon:/sbin:/sbin/nologin  
显示/etc/passwd账户:   
cat /etc/passwd | awk -F: 'BEGIN {count=0} {name[count]=$1; count++} END{for(i = 0; i < NR; i++) print i,name[i]}'  
0 root  
1 bin  
2 daemon  
..  
