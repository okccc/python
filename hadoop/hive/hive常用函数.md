## hive常用函数
[hive函数案例](http://blackproof.iteye.com/blog/2108353)  
[hive udf官网](https://cwiki.apache.org/confluence/display/hive/languagemanual+udf)    
[hive函数大全](http://blog.csdn.net/wisgood/article/details/17376393)
***
### <font color=red>字符串函数</font>
length  
语法：length(string a)  
返回值：int  
说明：返回字符串a的长度  
举例：  
hive> select length('abcedfg');  
7  
reverse  
语法：reverse(string a)  
返回值：string  
说明：返回字符串a的反转结果  
举例：  
hive> select reverse('abcedfg');  
gfdecba  
concat  
语法：concat(string a, string b…)  
返回值：string  
说明：返回输入字符串连接后的结果，支持任意个输入字符串  
举例：  
hive> select concat('abc','def','gh');  
abcdefgh  
concat_ws  
语法：concat_ws(string sep, string a, string b…)  
返回值：string  
说明：返回输入字符串连接后的结果，sep表示各个字符串间的分隔符  
举例：  
hive> select concat_ws(',','abc','def','gh') from lxw_dual;  
abc,def,gh  
collect_set  
说明：行转列  
举例：  
hive> select split(concat_ws(',',collect_set(column)),',') from dual;  
lateral  view explode  
说明：列转行  
举例：  
hive> select lateral view explode(split(concat_ws(',',collect_set(column)),',')) from dual;  
upper,ucase  
举例：  
hive> select upper('absed') from test;  
absed  
hive> select ucase('absed') from test;  
absed  
lower,lcase  
举例：  
hive> select lower('absed') from test;  
absed  
hive> select lcase('absed') from test;  
absed  
trim  
说明：去除字符串两边的空格  
举例：  
hive> select trim(' abc ') from test;  
abc  
ltrim  
说明：去除字符串左边的空格  
举例：  
hive> select ltrim(' abc') from test;  
abc  
rtrim  
说明：去除字符串右边的空格  
举例：  
hive> select rtrim('abc ') from test;  
abc  
substr,substring  
语法：substr(string a, int start),substring(string a, int start)  
说明：返回字符串a从start位置到结尾的字符串  
举例：  
hive> select substr('abcde',3) from test;  
cde  
hive> select substring('abcde',3) from test;  
cde  
hive>  selectsubstr('abcde',-1) from test; （和oracle相同）  
e  
语法：substr(string a, int start, int len),substring(string a, intstart, int len)  
说明：返回字符串a从start位置开始，长度为len的字符串  
举例：  
hive> select substr('abcde',3,2) from test;  
cd  
hive> select substring('abcde',3,2) from test;  
cd  
hive>select substring('abcde',-2,2) from test;  
de  
str_to_map  
map<string,string> str_to_map(text[, delimiter1, delimiter2]) splits text into key-value pairs using two delimiters. delimiter1 separates text into k-v pairs, and delimiter2 splits each k-v pair. default delimiters are ',' for delimiter1 and '=' for delimiter2.  
举例：  
hive> select str_to_map('aaa:11&bbb:22', '&', ':') from tmp.test;  
{"bbb":"22","aaa":"11"}  
hive> select str_to_map('aaa:11&bbb:22', '&', ':')['aaa'] from tmp.test;  
11  
注意：str_to_map必须作用于字符串，不然会报错caused by: java.lang.nullpointerexception  
hive> select str_to_map(null,'&','=');  
failed: semanticexception [error 10014]: line 1:7 wrong arguments ''='': all argument should be string/character type  
hive> select str_to_map('-','&','=');  
{"-":null}  
nvl  
语法：nvl(value1, value2)  
说明：如果value1值为空，默认返回value2（注意：value1和value2必须是同一种数据类型）  
举例：  
hive> select nvl(null,'--') from test;  
--  
instr  
语法：instr(string a, string a)  
说明：返回字符a在字符串a中位置索引  
举例：  
hive> select instr('abcde','c') from test;  
3  
regexp_replace  
语法：regexp_replace(string a, string b, string c)  
返回值：string  
说明：将字符串a中的符合java正则表达式b的部分替换为c；注意，在有些情况下要使用转义字符,类似oracle中的     				      
          regexp_replace函数  
举例：  
hive> regexp_replace(regexp_replace(regexp_replace(get_json_object(t.json,'$.request'),'get       
          /v40/banner/event.jpg\\?| http/1.1|& http/1.1',''),'&','","'),'=','":"')；  
regexp_extract  
语法：regexp_extract(string subject, string pattern, int index)  
返回值：string  
说明：将字符串subject按照pattern正则表达式的规则拆分，返回index指定的字符；注意，在有些情况下要使用转义字  
          符,类似oracle中的regexp_replace函数  
举例：  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 1) from dual;        --1表示返回第一个括号  
the  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 2) from dual;        --2表示返回第二个括号  
bar  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 0) from dual;        --0表示返回全部  
foothebar  
parse_url  
语法：parse_url(url, parttoextract[, key]) - extracts a part from a url  
说明：解析url字符串，parttoextract的选项包含[host,path,query,ref,protocol,file,authority,userinfo]  
举例 ：  
select parse_url('http://facebook.com/path/p1.php?query=1', 'protocol') ;          	--http  
select parse_url('http://facebook.com/path/p1.php?query=1', 'host');			---facebook.com​  
select parse_url('http://facebook.com/path/p1.php?query=1', 'ref');				---空​  
select parse_url('http://facebook.com/path/p1.php?query=1', 'path');			---/path/p1.php​  
select parse_url('http://facebook.com/path/p1.php?query=1', 'query');			---query=1  
select parse_url('http://facebook.com/path/p1.php?query=1', 'query','query');		---1  
​select parse_url('http://facebook.com/path/p1.php?query=1', 'file');				---/path/p1.php?query=1​  
​select parse_url('http://facebook.com/path/p1.php?query=1', 'authority');		---facebook.com​  
​select parse_url('http://facebook.com/path/p1.php?query=1', 'userinfo');​		---空  
get_json_object  
语法：get_json_object(string json_string, string path)  
返回值：string  
说明：解析json的字符串json_string，返回path指定的内容；如果输入的json字符串无效，那么返回null  
举例：  
hive> select nvl(get_json_object(t.json,'$.timestamp'),'-') as timestamp from test t;  
reflect（等同于java_method）  
说明：使用java里的类和方法  
select  reflect('java.net.urldecoder','decode',get_json_object(t.json,'$.request'));      --中文解码  
select  reflect("java.lang.string", "valueof", 1)         	 --1  
           reflect("java.lang.string", "isempty")             	 --true  
           reflect("java.lang.math", "max", 2, 3)             	 --3  
           reflect("java.lang.math", "min", 2, 3)          	  	  --2  
           reflect("java.lang.math", "round", 2.5)                   --3  
           reflect("java.lang.math", "exp", 1.0)            	          --2.7182818284590455  
           reflect("java.lang.math", "floor", 1.9)           	  	  --1.0  
repeat  
语法：repeat(string str, int n)  
返回值：string  
说明：返回重复n次后的str字符串  
举例：  
hive> select repeat('abc',5);  
abcabcabcabcabc  
ascii  
语法：ascii(string str)  
返回值：int  
说明：返回字符串str第一个字符的ascii码  
举例：  
hive> select ascii('abcde');  
97  
lpad  
语法：lpad(string str, int len, string pad)  
返回值：string  
说明：将str进行用pad进行左补足到len位  
举例：  
hive> select lpad('abc',10,'td');  
tdtdtdtabc  
rpad  
语法: rpad(string str, int len, string pad)  
返回值: string  
说明：将str进行用pad进行右补足到len位  
举例：  
hive> select rpad('abc',10,'td');  
abctdtdtdt  
split  
语法：split(string str, stringpat)  
返回值:：rray  
说明：按照pat字符串分割str，分割后是字符串数组  
举例：  
hive> select split('abtcdtef','t');  
["ab","cd","ef"]  
hive> select split('abtcdtef','t')[0];  
ab  
find_in_set  
语法：find_in_set(string str, string strlist)  
返回值：int  
说明：返回str在strlist第一次出现的位置，strlist是用逗号分割的字符串；如果没有找该str字符，则返回0  
举例：  
hive> select find_in_set('ab','ef,ab,de');  
2  
hive> select find_in_set('at','ef,ab,de');  
0  
### <font color=red>时间函数</font>
year、month、day、hour、minute、second
语法：year(string date)  
说明：返回日期中的年，月，日，时，分，秒（注意：日期是yyyy-mm-dd格式）  
举例：  
hive> select year('2016-10-19 16:23:08');  
2016  
...  
current_timestamp  
语法1：current_timestamp()  
说明：获得linux当前时间，精确到秒   
返回值：bigint  
举例：  
hive> select current_timestamp();  
2017-06-23 15:34:34  
unix_timestamp  
语法1：unix_timestamp()  
说明：获得当前时区的unix时间戳  
返回值：bigint  
举例：  
hive> select unix_timestamp();  
1476864152  
语法2：unix_timestamp(string date)  
说明：转换格式为"yyyy-mm-dd hh:mm:ss"的日期到unix时间戳；如果转化失败，则返回0  
举例：  
hive> select unix_timestamp('2016-10-18 16:05:03');  
1476864152  
语法3：unix_timestamp(string date, string pattern)  
说明：转换pattern格式的日期到unix时间戳；如果转化失败，则返回0  
举例：  
hive> select unix_timestamp('20161018','yyyymmdd');  
1476864152  
from_unixtime  
语法: from_unixtime(bigint unixtime[, string format])  
说明:转化unix时间戳（从1970-01-01 00:00:00 utc到指定时间的秒数）到当前时区的指定时间格式  
返回值：string  
举例：  
hive> select from_unixtime(unix_timestamp(),'yyyymmdd');  
20161019  
hive> select from_unixtime(unix_timestamp(),'yyyy-mm-dd');  
2016-10-19  
to_date  
语法：to_date(string timestamp)  
说明：返回日期时间字段中的日期部分（注意：日期是yyyy-mm-dd格式）  
举例：  
hive> select to_date('2011-12-08 10:03:01') from test;  
2011-12-08  
weekofyear  
语法： weekofyear (string date)  
说明：返回日期在当前的周数（注意：日期是yyyy-mm-dd格式）  
举例：  
hive> select weekofyear('2016-10-19 12:13:25');  
42  
datediff  
语法： datediff(string enddate, string startdate)  
说明：返回结束日期减去开始日期的天数  
举例：  
hive> select datediff('2016-10-19','2016-03-15');  
218  
date_add  
语法：date_add(string startdate, int days)  
说明：返回开始日期增加指定天数后的日期  
举例：  
hive> select date_add('2016-10-18',10);  
2016-10-28  
date_sub  
语法：date_sub (string startdate, int days)  
说明：返回开始日期减少指定天数后的日期  
举例：  
hive> select date_sub('2016-10-18',10);   
2016-10-08  
add_months  
举例：  
hive> select add_months('2009-08-31', 1);    
'2009-09-30'  
- 某个月第一天  
hive> select trunc('2018-10-24','MM');  
2018-10-01  
- 某年第一天  
hive> select trunc('2018-08-20','YEAR');  
2018-01-01  
- 某天所在月份最后一天  
hive> select last_day('2018-05-12');  
2018-05-31  
- 上个月的第一天    
hive> select trunc(add_months(current_date,-1),'MM');  
2018-09-01  
- 上个月最后一天   
hive> select last_day(add_months(current_date,-1));  
2018-09-30  

### <font color=red>数值计算</font>
round  
语法1：round(double a)  
返回值: bigint  
说明：返回double类型的整数值部分（遵循四舍五入）  
举例：  
hive> select round(3.1415926);  
3  
hive> select round(3.5);  
4  
语法2：round(double a, int d)  
返回值: double  
说明:返回指定精度d的double类型  
举例：  
hive> select round(3.1415926,4);  
3.1416  
floor  
语法：floor(double a)  
返回值：bigint  
说明：向下取整  
举例：  
hive> select floor(3.1415926) from lxw_dual;  
3  
hive> select floor(25) from lxw_dual;  
25  
ceil，ceiling  
语法：ceil(double a)  
返回值：bigint  
说明：向上取整  
举例：  
hive> select ceil(3.1415926) from lxw_dual;  
4  
hive> select ceil(46) from lxw_dual;  
46  
rand  
语法：rand(),rand(int seed)  
返回值：double  
说明：返回一个0到1范围内的随机数，如果指定种子seed，则会得到一个稳定的随机数序列  
举例：  
hive> select rand();  
0.5577432776034763  
hive> select rand(100);  
0.7220096548596434  
hive>select rand(100);  
0.7220096548596434  
exp  
语法：exp(double a)  
返回值：double  
说明：返回自然对数e的a次方  
举例：  
hive> select exp(2);  
7.38905609893065  
ln  
语法：ln(double a)  
返回值：double  
说明：返回a的自然对数  
举例：  
hive> select ln(7.38905609893065);  
2.0  
log10  
语法：log10(double a)  
返回值：double  
说明：返回以10为底的a的对数  
举例：  
hive> select log10(100);  
2.0  
log2  
语法：log2(double a)  
返回值：double  
说明：返回以2为底的a的对数  
举例：  
hive> select log2(8);  
3.0  
log  
语法：log(double base, double a)  
返回值：double  
说明：返回以base为底的a的对数  
举例：  
hive> select log(4,256);  
4.0  
pow，power  
语法：pow(double a, double p)  
返回值：double  
说明：返回a的p次幂  
举例：  
hive> select pow(2,4);  
16.0  
sqrt  
语法：sqrt(double a)  
返回值：double  
说明：返回a的平方根  
举例：  
hive> select sqrt(16);  
4.0  
bin  
语法：bin(bigint a)  
返回值：string  
说明：返回a的二进制代码表示  
举例：  
hive> select bin(7);  
111  
hex  
语法：hex(bigint a)  
返回值：string  
说明：如果变量是int类型，那么返回a的十六进制表示；如果变量是string类型，则返回该字符串的十六进制表示  
举例：  
hive> select hex(17);  
11  
hive> select hex('abc');  
616263  
unhex  
语法；unhex(string a)  
返回值：string  
说明：返回该十六进制字符串所代码的字符串  
举例：  
hive> select unhex('616263');  
abc  
conv  
语法：conv(bigint num, int from_base, int to_base)  
返回值：string  
说明：将数值num从from_base进制转化到to_base进制  
举例：  
hive> select conv(17,10,16);  
11  
hive> select conv(17,10,2);  
10001  
abs  
语法：abs(double a)  abs(int a)  
返回值：double       int  
说明：返回数值a的绝对值  
举例：  
hive> select abs(-3.9);  
3.9  
hive> select abs(10.9);  
10.9  
pmod  
语法：pmod(int a, int b),pmod(double a, double b)  
返回值：int double  
说明：返回正的a除以b的余数  
举例：  
hive> select pmod(9,4);  
1  
hive> select pmod(-9,4);  
3  
sin  
语法：sin(double a)  
返回值：double  
说明：返回a的正弦值  
举例：  
hive> select sin(0.8);  
0.7173560908995228  
asin  
语法：asin(double a)  
返回值：double  
说明：返回a的反正弦值  
举例：  
hive> select asin(0.7173560908995228);  
0.8  
cos  
语法：cos(double a)  
返回值：double  
说明：返回a的余弦值  
举例：  
hive> select cos(0.9);  
0.6216099682706644  
acos  
语法：acos(double a)  
返回值：double  
说明：返回a的反余弦值  
举例：  
hive> select acos(0.6216099682706644);  
0.9  
positive  
语法：positive(int a), positive(double a)  
返回值：int double  
说明：返回a本身  
举例：  
hive> select positive(-10);  
-10  
hive> select positive(12);  
12  
negative  
语法：negative(int a), negative(double a)  
返回值：int double  
说明：返回a的相反数  
举例：  
hive> select negative(-5);  
5  
hive> select negative(8);  
-8  
### <font color=red>条件函数</font>
if  
语法：if(boolean testcondition, t valuetrue, t valuefalseornull)  
返回值：t  
说明：当条件testcondition为true时，返回valuetrue；否则返回valuefalseornull  
举例：  
hive> select if(1=1,100,200);  
100  
hive> select if(uid is null,'-','uid');  
coalesce  
语法：coalesce(t v1, t v2,…)  
返回值：t  
说明：返回参数中的第一个非空值；如果所有值都为null，那么返回null  
举例：  
hive> select coalesce(null,'100','50′);  
100  
case  
语法1：case a when b then c [when d then e]* [else f] end  
返回值：t  
说明：如果a等于b，那么返回c；如果a等于d，那么返回e；否则返回f  
举例：  
hive> select case 100 when 50 then 'tom' when 100 then 'mary' else 'tim' end;  
mary  
hive> select case 200 when 50 then 'tom' when 100 then 'mary' else 'tim' end;  
tim  
语法2：case when a then b [when c then d]* [else e] end  
返回值：t  
说明：如果a为true,则返回b；如果c为true，则返回d；否则返回e  
举例：  
hive> select case when 1=2 then 'tom' when 2=2 then 'mary' else'tim' end;  
mary  
hive> select case when 1=1 then 'tom' when 2=2 then 'mary' else'tim' end;  
tom  
cast  
说明：类型转换  
语法: cast(expr as <type>)  
举例：  
hive> select cast(100 as string);  
