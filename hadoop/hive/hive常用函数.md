## hive常用函数
[hive函数案例](http://blackproof.iteye.com/blog/2108353)  
[hive udf官网](https://cwiki.apache.org/confluence/display/hive/languagemanual+udf)    
[hive函数大全](http://blog.csdn.net/wisgood/article/details/17376393)
***
### <font color=red>string</font>
- length  
hive> select length('abcedfg');  
7  
- reverse  
hive> select reverse('abcedfg');  
gfdecba  
- concat  
hive> select concat('abc','def','gh');  
abcdefgh  
- concat_ws  
hive> select concat_ws(',','abc','def','gh') from dual;  
abc,def,gh  
- collect_set  
说明：行转列    
hive> select split(concat_ws(',',collect_set(column)),',') from dual;  
- lateral view explode  
说明：列转行    
hive> select lateral view explode(split(concat_ws(',',collect_set(column)),',')) from dual;  
- trim  
说明：去除字符串两边空格  
hive> select trim(' abc ') from test;  
abc  
- ltrim  
说明：去除字符串左边空格  
hive> select ltrim(' abc') from test;  
abc  
- rtrim  
说明：去除字符串右边空格  
hive> select rtrim('abc ') from test;  
abc  
- substr/substring  
说明：返回字符串a从start位置到结尾的字符串  
hive> select substr('abcde',3) from test;  
cde  
hive> select substr('abcde',-1) from test; (和oracle相同)  
e  
说明：返回字符串a从start位置开始,长度为len的字符串  
hive> select substr('abcde',3,2) from test;  
cd  
hive>select substring('abcde',-2,2) from test;  
de  
- str_to_map  
说明：splits text into key-value pairs using two delimiters. delimiter1 separates text into k-v pairs, and delimiter2 splits each k-v pair. default delimiters are ',' for delimiter1 and '=' for delimiter2.    
hive> select str_to_map('aaa:11&bbb:22', '&', ':') from tmp.test;  
{"bbb":"22","aaa":"11"}  
hive> select str_to_map('aaa:11&bbb:22', '&', ':')['aaa'] from tmp.test;  
11  
注意：str_to_map必须作用于字符串,不然会报错caused by: java.lang.nullpointerexception  
hive> select str_to_map(null,'&','=');  
failed: semanticexception [error 10014]: line 1:7 wrong arguments ''='': all argument should be string/character type  
hive> select str_to_map('-','&','=');  
{"-":null}  
- nvl  
说明：如果value1值为空,默认返回value2(注意：value1和value2必须是同一种数据类型)  
举例：  
hive> select nvl('...','') from test;  
...
- instr  
hive> select instr('abcde','c') from test;  
3  
- regexp_replace  
hive> regexp_replace(regexp_replace(regexp_replace(get_json_object(t.json,'$.request'),'get       
          /v40/banner/event.jpg\\?| http/1.1|& http/1.1',''),'&','","'),'=','":"');  
- regexp_extract  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 1) from dual;        --1表示返回第一个括号  
the  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 2) from dual;        --2表示返回第二个括号  
bar  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 0) from dual;        --0表示返回全部  
foothebar  
- parse_url  
select parse_url('http://facebook.com/path/p1.php?query=1', 'protocol') ;       --http  
select parse_url('http://facebook.com/path/p1.php?query=1', 'host');			---facebook.com​  
select parse_url('http://facebook.com/path/p1.php?query=1', 'ref');				---空​  
select parse_url('http://facebook.com/path/p1.php?query=1', 'path');			---/path/p1.php​  
select parse_url('http://facebook.com/path/p1.php?query=1', 'query');			---query=1  
select parse_url('http://facebook.com/path/p1.php?query=1', 'query','query');	--1  
​select parse_url('http://facebook.com/path/p1.php?query=1', 'file');			--/path/p1.php?query=1​  
​select parse_url('http://facebook.com/path/p1.php?query=1', 'authority');		---facebook.com​  
​select parse_url('http://facebook.com/path/p1.php?query=1', 'userinfo');​		---空  
- get_json_object  
hive> select nvl(get_json_object(t.json,'$.timestamp'),'-') as timestamp from test t;  
- reflect(等同于java_method)  
说明：使用java里的类和方法  
select reflect('java.net.urldecoder','decode',get_json_object(t.json,'$.request'));      --中文解码  
select reflect("java.lang.string", "valueof", 1)         	 --1  
select reflect("java.lang.string", "isempty")             	 --true  
select reflect("java.lang.math", "max", 2, 3)             	 --3  
select reflect("java.lang.math", "min", 2, 3)          	  	 --2  
select reflect("java.lang.math", "round", 2.5)               --3  
select reflect("java.lang.math", "exp", 1.0)            	 --2.7182818284590455  
select reflect("java.lang.math", "floor", 1.9)           	 --1.0  
- repeat  
说明：返回重复n次后的str字符串  
hive> select repeat('abc',5);  
abcabcabcabcabc  
- ascii  
说明：返回字符串str第一个字符的ascii码  
hive> select ascii('abcde');  
97  
- lpad  
说明：将str用pad左补足到len位  
hive> select lpad('abc',10,'td');  
tdtdtdtabc  
- rpad  
说明：将str用pad右补足到len位  
hive> select rpad('abc',10,'td');  
abctdtdtdt  
- split  
hive> select split('abtcdtef','t');  
["ab","cd","ef"]  
hive> select split('abtcdtef','t')[0];  
ab  
- find_in_set  
hive> select find_in_set('ab','ef,ab,de');  
2  
hive> select find_in_set('at','ef,ab,de');  
0  
### <font color=red>time</font>
year/month/day/hour/minute/second  
说明：返回日期中的年,月,日,时,分,秒(注意：日期是yyyy-mm-dd格式)  
hive> select year('2016-10-19 16:23:08');  
2016  
- current_timestamp    
hive> select current_timestamp();  
2017-06-23 15:34:34  
- unix_timestamp  
hive> select unix_timestamp();  
1476864152  
hive> select unix_timestamp('2016-10-18 16:05:03');  
1476864152  
hive> select unix_timestamp('20161018', 'yyyymmdd');  
1476864152  
- from_unixtime  
hive> select from_unixtime(unix_timestamp(dt, 'yyyymmdd'),'yyyy-mm-dd');  
2016-10-19  
- to_date  
hive> select to_date('2011-12-08 10:03:01') from test;  
2011-12-08  
- weekofyear  
hive> select weekofyear('2016-10-19 12:13:25');  
42  
- datediff  
hive> select datediff('2016-10-19','2016-03-15');  
218  
- date_add  
hive> select date_add('2016-10-18',10);  
2016-10-28  
- date_sub  
hive> select date_sub('2016-10-18',10);   
2016-10-08  
- add_months  
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

### <font color=red>math</font>
- round  
hive> select round(3.1415926);  
3  
hive> select round(3.5);  
4  
hive> select round(3.1415926,4);  
3.1416  
- floor  
hive> select floor(3.1415926) from dual;  
3  
- ceil/ceiling  
hive> select ceil(3.1415926) from dual;  
4  
- rand  
hive> select rand();  
0.5577432776034763  
- exp  
说明：返回自然对数e的a次方  
hive> select exp(2);  
7.38905609893065  
- ln  
说明：返回a的自然对数  
hive> select ln(7.38905609893065);  
2.0  
- log10  
说明：返回以10为底的a的对数  
hive> select log10(100);  
2.0  
- log2  
说明：返回以2为底的a的对数  
hive> select log2(8);  
3.0  
- log  
说明：返回以a为底的b的对数  
hive> select log(4,256);  
4.0  
- pow,power  
说明：返回a的p次幂  
hive> select pow(2,4);  
16.0  
- sqrt  
说明：返回a的平方根  
hive> select sqrt(16);  
4.0  
- bin  
说明：返回a的二进制代表示  
hive> select bin(7);  
111  
- hex  
说明：返回a的十六进制表示  
hive> select hex(17);  
11  
hive> select hex('abc');  
616263  
- unhex  
说明：返回该十六进制字符串所代表的字符串  
hive> select unhex('616263');  
abc  
- conv  
说明：将数值num从from_base进制转化到to_base进制  
hive> select conv(17,10,16);  
11  
hive> select conv(17,10,2);  
10001  
- abs  
hive> select abs(-3.9);  
3.9  
- pmod  
说明：返回a除以b的余数的绝对值    
hive> select pmod(9,4);  
1  
hive> select pmod(-9,4);  
3  
- sin  
说明：返回a的正弦值  
hive> select sin(0.8);  
0.7173560908995228  
- asin  
说明：返回a的反正弦值  
hive> select asin(0.7173560908995228);  
0.8  
- cos  
说明：返回a的余弦值  
hive> select cos(0.9);  
0.6216099682706644  
- acos  
说明：返回a的反余弦值  
hive> select acos(0.6216099682706644);  
0.9  
- positive  
说明：返回a本身  
举例：  
hive> select positive(-10);  
-10  
- negative  
说明：返回a的相反数  
hive> select negative(-5);  
5  
### <font color=red>condition</font>
- if  
hive> select if(1=1,100,200);  
100  
hive> select if(uid is null,'-','uid');  
- coalesce  
说明：返回参数中的第一个非空值;如果所有值都为null,那么返回null  
hive> select coalesce(null,'100','50′);  
100  
- case  
hive> select case 100 when 50 then 'tom' when 100 then 'mary' else 'tim' end;  
mary  
hive> select case when 1=2 then 'tom' when 2=2 then 'mary' else'tim' end;  
mary  
- cast  
hive> select cast(100 as string);  
