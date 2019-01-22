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
- 案例  
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
echo this is a test line|sed 's/\w\\+/{&}/g'：将选中的单词两边加上大括号  // {this} {is} {a} {test}  
sed 's/(.)line$/\1/g' file：匹配以line结尾的行line前面的部分  
sed 's/(.)is(.)line/\1\2/g' file：匹配is前面和line前面的部分  
echo this is digit 7 in a number|sed 's/digit\([0-9]\)/\1/'：this is 7 in a number  
echo aaa BBB|sed 's/\([a-z]\+\) \([A-Z]\+\)/\2\1/'：交换子串顺序  // BBB aaa  
