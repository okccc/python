## sed
sed：是一种流编辑器(stream editor),配合正则表达式功能强大,擅长行操作  
格式：sed -option 'command' file  
一次处理一行内容,先把当前处理的行存储在临时缓冲区中,称为"模式空间"(pattern space),接着用sed命令处理缓冲区内容并送往屏幕  
接着处理下一行,不断重复直到文件末尾,文件内容并没有改变,除非使用重定向存储输出  
-n：安静模式(slient)在一般sed的用法中,所有来自stdin的内容都会被列出到屏幕上,加上-n参数后,就只有经过  
       sed特殊处理的那一行(或者动作)才会被列出来    
-e：直接在指令列模式上进行 sed 的动作编辑  
-f：直接将 sed 的动作写在一个文件内, -f filename 则可以执行filename内的sed命令    
-r：让sed命令支持扩展的正则表达式    
-i：直接修改文件内容,而不是由屏幕输出  
常用command：  
a \：追加,在选中行的下一行插入字符串(多行字符串可以用\n分隔)   
i \：插入,在选中行的上一行插入字符串(多行字符串可以用\n分隔)   
c \：替换,将选定的行替换为新的字符串(多行字符串可以用\n分隔)    
d：  删除,将选中的行删除  
p：  打印,打印当前选择的行,通常结合sed -n 使用  
s：  替换(可搭配正则使用),通常s命令的用法是这样的：s/old/new/g  
配合正则表达式：  
^：匹配行开始,/^sed/匹配所有以sed开头的行    
$：匹配行结束,/sed$/匹配所有以sed结尾的行   
.：匹配一个非换行符的任意字符,/s.d/匹配s后接一个任意字符,最后是d    
*：匹配0个或多个字符,/*sed/匹配所有模板是一个或多个空格后紧跟sed的行    
[]：匹配一个指定范围内的字符,如/[sS]ed/匹配sed和Sed  
[^]：匹配一个不在指定范围内的字符,如：/[^A-RT-Z]ed/匹配不包含A-R和T-Z的一个字母开头,紧跟ed的行    
\(..\)：匹配子串,保存匹配的字符,如s/\(love\)able/\1rs,loveable被替换成lovers  
           \1表示匹配到的第一个子串,\2表示匹配到的第二个子串  
&：保存搜索字符用来替换其他字符,如s/love/**&**/,love替换成**love**    
\<：匹配单词的开始,如：/\<love/匹配包含以love开头的行  
\>：匹配单词的结束,如：/love\>/匹配包含以love结尾的行   
x\{m\}：重复字符x,m次,如：/0\{5\}/匹配包含5个0的行  
x\{m,\}：重复字符x,至少m次,如：/0\{5,\}/匹配至少有5个0的行    
x\{m,n\}：重复字符x,至少m次,不多于n次,如：/0\{5,10\}/匹配5~10个0的行    
a命令：  
sed '1a \add one' file          //在第一行之后增加字符串”add one“  
sed '1,$a \add one' file          //在第一行和最后一行所有的行后面都加上”add one“  
sed '/first/a \add one' file          //在包含”first”字符串的行的后面加上字符串”add one“  
sed '/^ha.*day$/a \add one' file      //在以ha开头,以day结尾的行后面加上”add one“  
c命令：  
sed '$c \add one' file            //将最后一行替换成字符串”add one”  
sed '4,$c \add one' file          //将第四行到最后一行的内容替换成字符串”add one”  
sed '/^ha.*day$/c \replace line' file     //将以ha开头,以day结尾的行替换成”replace line”  
d命令：  
sed '4,$d' file             //删除第四行到最后一行中的内容  
sed '/^$/d' file              //删除空白行  
sed '/^ha.*day$/d' file         //删除以ha开头,以day结尾的行  
p命令：  
sed -n '/^ha.*day$/p' file          //打印以ha开始,以day结尾的行  
s命令：  
<font color=red>sed 's/line/text/g' file</font>         //将文件中的所有line替换成text,g表示全局替换    
<font color=red>sed -i 's/book/books/g' file</font>        //直接编辑file,将book替换成books  
sed 's/line/text/2g' file         //从第二处匹配的地方开始替换  
sed 's/\(.*\)line$/\1/g' file         //匹配以line结尾的行line前面的部分  
sed 's/\(.*\)is\(.*\)line/\1\2/g' file      //匹配is前面和line前面的部分  
&命令：  
echo this is a test line | sed 's/\w\+/[&]/g'   //[this] [is] [a] [test] [line]  
sed 's/^192.168.0.1/&localhost/' file     //192.168.0.1localhost  
\1命令：  
echo this is digit 7 in a number | sed 's/digit \([0-9]\)/\1/'      //this is 7 in a number  
echo aaa BBB | sed 's/\([a-z]\+\) \([A-Z]\+\)/\2 \1/'         //BBB aaa  
选定行范围：  
sed -n '5,/^test/p' file          //打印从第5行开始到第一个以test开始的行之间的所有行  
-e命令：  
sed -e '1,5d' -e 's/test/check/' file     //后面的受前面的影响  
