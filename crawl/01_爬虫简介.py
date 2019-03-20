# coding=utf-8
"""
爬虫：爬取网页数据的程序,网络爬取的过程可以理解为模拟浏览器操作的过程
robots协议：该网站各个页面的爬取权限
淘宝网：https://www.taobao.com/robots.txt
腾讯网：http://www.qq.com/robots.txt

网页三大特征
1.网页都有唯一的URL(统一资源定位符)
2.网页都使用HTML(超文本标记语言)描述页面信息 ---> 可以放超链接所以叫超文本
3.网页都使用HTTP/HTTPS(超文本传输协议)传输HTML数据
DNS：将域名映射成IP地址的域名解析服务

http请求方式
get是从服务器上获取数据,post是向服务器传送数据
get请求：参数显式的写在浏览器的url中,例如：http://www.baidu.com/s?wd=Chinese
post请求：参数在请求体当中,以隐式的方式发送,请求的参数包含在"Content-Type"消息头里,指明该消息体的媒体类型和编码 ---> 表单提交、大文本传输

cookie: 由于http协议是无状态的,服务器无法识别多个请求是否由同一个用户发起,网站服务器为了辨别用户身份和进行session跟踪会在response中返回一段
        cookie值存储在浏览器上,cookie可以保持登录信息到用户下次与服务器的会话,浏览器存储的cookie大小一般不超过4k

http请求包含：请求行,请求头,空行,请求体(post)
POST http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule HTTP/1.1
Host：fanyi.youdao.com                                           ---> 主机和端口号
Connection：keep-alive                                           ---> 连接类型
Upgrade-Insecure-Requests                                        ---> 升级为HTTPS请求
Accept：application/json, text/javascript, */*; q=0.01           ---> 传输文件类型
User-Agent：...                                                  ---> 浏览器名称(重要)
Referer：http://fanyi.youdao.com/                                ---> 页面跳转处(重要)
Accept-Encoding：gzip, deflate                                   ---> 文件编解码格式
Accept-Language：zh-CN,zh;q=0.9                                  ---> 浏览器愿意接收的数据 q表示权重
Cookie：...                                                      ---> Cookie(重要)
X-Requested-With：XMLHttpRequest                                 ---> 说明是ajax异步请求

i=rabbit&from=AUTO&to=AUTO&smartresult=dict&client=fanyideskweb

http状态码汇总
200：请求成功
301：永久性重定向    www.jindong.com --> www.jd.com
302：临时性重定向    未登录时访问个人中心会跳转到登录页面
403：没有权限访问
404：找不到资源
500：服务器错误
"""
