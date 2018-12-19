## grep
grep(global search re print)：基于行的文本搜索工具  
格式: grep <font color=red>[-cinvABC]</font> 'keyword' file  
grep error mysql.log --color   高亮显示关键字  
grep error mysql.log --color -A 10 -B 10  高亮显示关键字所在行的前10行和后10行  
-c ：打印符合要求的行数  
-i ：忽略大小写  
-n ：在输出符合要求的行的同时连同行号一起输出  
-v ：排除不符合要求的行  
-A ：后跟一个数字,例如 –A2 则表示打印符合要求的行及下面两行
-B ：后跟一个数字,例如 –B2 则表示打印符合要求的行及上面两行
-C ：后跟一个数字,例如 –C2 则表示打印符合要求的行及上下各两行
过滤出包含数字的行：grep [0-9] test.txt  
过滤出包含数字和字符的行：grep [0-9a-zA-Z] test.txt  
过滤出不包含数字的行：grep -v [0-9] test.txt  
过滤出不包含某个字符的行：grep '[^r]' test.txt  
过滤出以export开头的行：grep '^export' test.txt  
过滤出以bin结尾的行：grep 'bin$' test.txt  
过滤出非空行：grep -v '^$' test.txt    ('^$'表示空行)  
grep 'mysql' ./*.sh：查看当前目录下包含mysql的脚本

## find 
find：在指定目录下按匹配规则查找文件(夹)  
格式：find path -option [-print] [-exec command] {} \  
-option常用选项：  
- type  
b: 块设备 d: 目录 c: 字符设备文件 p: 管道文件 l: 符号链接文件 f: 普通文件
find . -type d –print                             --> 在当前目录下查找文件夹  
find . ! -type d –print                           --> 在当前目录下查找非文件夹  
find . -type l –print                             --> 在当前目录下查找链接文件  
find ./ -type d -exec rm -rf {} \                  --> 找到当前目录下的文件夹并删掉  
- name  
find . -name filename                              --> 在当前目录及其子目录下查找名字为filename的文件  
find . -name "*.c"                                 --> 在当前目录及其子目录下查找扩展名为“c”的文件  
- perm  
find . -perm 755 –print                           --> 在当前目录下查找文件权限为755的文件  
- prune  
find /apps -path "/apps/bin" -prune -o –print     --> 在/apps目录下查找文件且忽略/apps/bin目录  
- user  
find ~ -user aaa –print                           --> 在$HOME目录中查找文件属主为aaa的文件  
- group  
find ~ -group bbb –print                          --> 在$HOME目录下查找属于bbb用户组的文件  
- atime 天,-amin 分钟-mtime 天,-mmin 分钟-ctime 天,-cmin 分钟  
find . -type f -atime 7                            --> 在当前目录查找刚好7天前访问的文件  
find . -type f -amin +10                           --> 在当前目录查找访问时间超过10分钟的文件  
find . -mtime -5 –print                           --> 在当前目录查找5天内修改过的文件  
find . -mtime +3 –print                           --> 在当前目录查找3天前修改过的文件  
- nogroup  
find . -nogroup -print                             --> 在当前目录查找无有效所属组的文件  
- nouser  
find . -nouser –print                             --> 在当前目录查找无有效属主的文件  
- newer   
find . -type f -newer file1 ！ file2               --> 在当前目录查找修改时间比file1新但比file2旧的文件  
- depth  
find . -maxdepth 3 -type f                         --> 向下深度最大为3层  
find . -mindepth 2 -type f                         --> 向下深度最少为2层  
- size  
find . -size +1000k –print                        --> 在当前目录下查找大于1 M的文件  
find . -size -1000k –print                        --> 在当前目录下查找小于1 M的文件  
find . -size 1000k –print                         --> 在当前目录下查找等于1 M的文件  
- empty  
find . -empty                                      --> 在当前目录下找空文件  
- exec -command {} \;  
find ./ -type f -user root -exec chown tom {} \;                                 -->  查找root用户的文件并将所有权改为tom  
find ./ -type f -name "*.txt" -exec cat {} \; > all.txt                            -->  查找.txt文件并合并重定向到all.txt文件
find ./ -type f -mtime +30 -name "*.log" -exce cp {} old \;                      --> 将30天前的.log文件复制到old目录