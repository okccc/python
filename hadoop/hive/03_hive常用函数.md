#### <font color=gray>字符串</font>
- length：长度  
hive> select length('abcedfg');
- reverse：反序  
hive> select reverse('abcedfg');  
- concat：拼接  
hive> select concat('abc','def','gh');  
- concat_ws：指定分隔符拼接  
hive> select concat_ws(',','abc','def','gh');  
- <font color=red>collect_set：行转列</font>  
hive> select split(concat_ws(',',collect_set(column)),',');  
- <font color=red>lateral view explode：列转行</font>  
hive> select lateral view explode(split(concat_ws(',',collect_set(column)),','));  
- trim：去除字符串两边空格  
hive> select trim(' abc ');  
- substring：截取  
hive> select substring('facebook',3);  
hive> select substring('facebook',-3);  
hive> select substring('facebook',3,2);  
hive> select substring('facebook',-3,2);  
- <font color=red>str_to_map：将字符串切割成键值对</font>  
hive> select str_to_map('aaa:11&bbb:22', '&', ':');  
hive> select str_to_map('aaa:11&bbb:22', '&', ':')['aaa'];  
- nvl：如果v1为空就返回v2  
hive> select nvl('...','-');  
- instr：索引  
hive> select instr('abcde','c');
- <font color=red>regexp_replace：替换</font>  
hive> select regexp_replace('2019-01-01','-','');
- <font color=red>regexp_extract：正则提取</font>  hive> 
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 1);  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 2);  
hive> select regexp_extract('foothebar', 'foo(.*?)(bar)', 0);  
- <font color=red>parse_url：解析url</font>  
hive> select parse_url('http://facebook.com/path/p1.php?query=1', 'PROTOCOL');           // http  
hive> select parse_url('http://facebook.com/path/p1.php?query=1', 'HOST');		         // facebook.com​  
hive> select parse_url('http://facebook.com/path/p1.php?query=1', 'PATH');		         // /path/p1.php​  
hive> select parse_url('http://facebook.com/path/p1.php?query=1', 'QUERY');		         // query=1  
hive> select parse_url('http://facebook.com/path/p1.php?query=1', 'QUERY','query');	     //  1  
hive> ​select parse_url('http://facebook.com/path/p1.php?query=1', 'FILE');			     // /path/p1.php?query=1​  
- <font color=red>get_json_object：解析json字符串</font>  
hive> select nvl(get_json_object(t.json,'$.timestamp'),'-');  
- <font color=red>reflect：使用java类中的方法</font>  
hive> select reflect('java.net.urldecoder','decode','...');      // 中文解码  
hive> select reflect("java.lang.string", "valueof", 1)         	 // 1  
hive> select reflect("java.lang.string", "isempty")              // true  
hive> select reflect("java.lang.math", "max", 2, 3)              // 3  
hive> select reflect("java.lang.math", "round", 2.5)             // 3  
hive> select reflect("java.lang.math", "exp", 1.0)            	 // 2.7182818284590455  
hive> select reflect("java.lang.math", "floor", 1.9)           	 // 1.0  
- repeat：复制字符串  
说明：返回重复n次后的str字符串
hive> select repeat('abc',5);  
- ascii：返回字符串第一个字符的ascii码  
hive> select ascii('abcde');  
- lpad：字符串补位  
hive> select lpad('abc',10,'td');  
hive> select rpad('abc',10,'td');  
- <font color=red>split：将字符串切割成数组</font>  
hive> select split('abtcdtef','t');  
#### <font color=gray>时间日期</font>
- year/month/day/hour/minute/second  
hive> select year('2016-10-19 16:23:08');  
- current_timestamp：当前时间戳  
hive> select current_timestamp();  
- unix_timestamp：unix时间  
hive> select unix_timestamp();  
- from_unixtime：日期格式转换  
hive> select from_unixtime(unix_timestamp(dt, 'yyyymmdd'),'yyyy-mm-dd');  
- to_date  
hive> select to_date('2011-12-08 10:03:01');  
- weekofyear：一年中的周数  
hive> select weekofyear('2016-10-19 12:13:25');  
- date_add：日期增加  
hive> select date_add('2016-10-18',10);  
- date_sub：日期减少  
hive> select date_sub('2016-10-18',10);   
- datediff：两个日期间隔  
hive> select datediff('2016-10-19','2016-03-15');  
- add_months：月份增加  
hive> select add_months('2009-08-31', 1);    
- <font color=red>trunc：某年(月)的第一天</font>  
hive> select trunc('2018-08-20','YEAR');  
hive> select trunc('2018-10-24','MM');  
- <font color=red>last_day：某月最后一天</font>  
hive> select last_day('2018-05-12');  
- 上个月的第一天/最后一天  
hive> select trunc(add_months(current_date,-1),'MM');  
hive> select last_day(add_months(current_date,-1));  
#### <font color=gray>数学运算</font>
- <font color=red>round：四舍五入</font>  
hive> select round(3.5);  
hive> select round(3.1415926,4);  
- floor：向下取整  
hive> select floor(3.1415926);  
- ceil：向上取整  
hive> select ceil(3.1415926);  
- rand：取随机数  
hive> select rand();  
0.5577432776034763  
- exp：计算自然对数e的a次方  
hive> select exp(2);  
- ln：计算a的自然对数e  
hive> select ln(7.38905609893065);  
- log10：计算以10为底a的对数  
hive> select log10(100);  
- log2：计算以2为底a的对数  
hive> select log2(8);  
- log：计算以a为底b的对数  
hive> select log(4, 256);  
- <font color=red>pmod：计算a除以b的余数</font>  
hive> select pmod(9,4);  
- pow：计算a的p次幂  
hive> select pow(2,4);  
- sqrt：计算a的平方根  
hive> select sqrt(16);  
- bin：计算a的二进制代表示  
hive> select bin(7);  
- hex：计算a的十六进制表示  
hive> select hex(17);  
hive> select hex('abc');  
- unhex；计算该十六进制字符串所代表的字符串  
hive> select unhex('616263');  
- conv：将数字从一个进制转换成另一个进制  
hive> select conv(17,10,16);  
hive> select conv(17,10,2);  
- abs：计算绝对值  
hive> select abs(-3.9);  
- sin：计算a的正弦值  
hive> select sin(0.8);  
- asin：计算a的反正弦值  
hive> select asin(0.7173560908995228);  
- cos：计算a的余弦值  
hive> select cos(0.9);  
- acos：计算a的反余弦值  
hive> select acos(0.6216099682706644);  
- positive：返回a本身  
hive> select positive(-10);  
- negative：返回a的相反数  
hive> select negative(-5);  
