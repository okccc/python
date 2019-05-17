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

请求方式
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

scrapy是纯Python编写的应用框架,使用了Twisted(协程)异步网络框架,且包含各种中间件接口,爬取速度贼快
Windows安装scrapy：
直接安装很麻烦,要手动安装很多模块(巨多坑),所以选择用anaconda安装
以管理员身份运行anaconda prompt：conda install scrapy一步搞定
Linux安装scrapy：
pip install scrapy
如果报错：Could not find a version that satisfies the requirement Twisted>=13.1.0 (from scrapy)
原因：centos系统将自带的python2升级到python3之后pip无法安装twisted
解决：yum install bzip2-devel --> 再重新编译安装Python：./configure prefix=/usr/local/python3  make && make install

打开Anaconda Prompt终端：
(base) C:\Users\chenqian>scrapy
scrapy 1.5.1 - no active project
Usage:
  scrapy <command> [options] [args]
Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print scrapy version
  view          Open URL in browser, as seen by scrapy
  [ more ]      More commands available when run from project directory
Use "scrapy <command> -h" to see more info about a command

scrapy项目四步骤：
1.新建项目：scrapy startproject myspider(项目名称)
|---myspider
    |---myspider                    # 项目的Python模块,将会从这里引用代码
    |   |---base.bash
    |   |---items.py                # 项目的目标文件
    |   |---pipelines.py            # 项目的管道文件
    |   |---settings.py             # 项目的配置文件
    |   |---spiders                 # 爬虫主程序
    |       |---base.bash
    |---scrapy.cfg                  # 项目的配置文件
2.明确目标(编写items.py)：设置需要保存的数据字段
3.制作爬虫(spiders/xxx.py)：爬取数据
  生成Spider模板：cd myspider --> scrapy genspider itcast(爬虫名) itcast.cn(网站域名)
  生成CrawlSpider模板：cd myspider --> scrapy genspider -t crawl tencent tencent.com
4.存储数据(pipelines.py)：设计管道存储爬取内容,存入文件或数据库
  当Item在Spider中被收集之后,它将会被传递到Item Pipeline,这些Item Pipeline组件按定义的顺序处理Item
运行：scrapy crawl ***
     scrapy crawl *** -o json/csv/xml
将myspider项目导入到pycharm运行,并选择装有scrapy框架的Anaconda3作为Project Interpreter

scrapy shell:
可以在不启动spider的情况下调试代码,也可以用来测试xpath和css表达式(结合IPython食用效果更佳)
案例：scrapy shell "http://esf.fang.com/"
***(此处省略n多日志)
[s] Available scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7fbc431bd3c8>
[s]   item       {}
[s]   request    <GET http://esf.fang.com/>
[s]   response   <200 http://esf.fang.com/>
[s]   settings   <scrapy.settings.Settings object at 0x7fbc41831748>
[s]   spider     <DefaultSpider 'default' at 0x7fbc4095e198>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser --> 这个很有用,可以在浏览器打开通过scrapy爬虫获取到的网页数据
In [1]:(此处调试代码)

Selectors选择器:
内置XPath和CSS Selector表达式,Selector有四个基本的方法,最常用的还是xpath
xpath()：传入xpath表达式,返回该表达式对应所有节点的selector list列表
extract()：序列化该节点为Unicode字符串并返回list -->  extract()==getall()  extract()[0]==get()
css()：传入CSS表达式,返回对应的所有节点的selector list列表,语法同BeautifulSoup4
re()：根据传入的正则表达式对数据进行提取,返回Unicode字符串list列表
"""
