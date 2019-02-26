# coding=utf-8
"""
爬虫：爬取网页数据的程序,网络爬取的过程可以理解为模拟浏览器操作的过程
robots协议：该网站各个页面的爬取权限
淘宝网：https://www.taobao.com/robots.txt
腾讯网：http://www.qq.com/robots.txt

网页三大特征:
1.网页都有唯一的URL(统一资源定位符)
2.网页都使用HTML(超文本标记语言)描述页面信息 ---> 可以放超链接所以叫超文本
3.网页都使用HTTP/HTTPS(超文本传输协议)传输HTML数据
DNS：将域名映射成IP地址的域名解析服务


Scrapy是纯Python编写的应用框架,使用了Twisted(协程)异步网络框架,且包含各种中间件接口,爬取速度贼快

Windows安装Scrapy：
直接安装很麻烦,要手动安装很多模块(巨多坑),所以选择用anaconda安装
以管理员身份运行anaconda prompt：conda install Scrapy一步搞定
Linux安装Scrapy：
pip install Scrapy
如果报错：Could not find a version that satisfies the requirement Twisted>=13.1.0 (from Scrapy)
原因：centos系统将自带的python2升级到python3之后pip无法安装twisted
解决：yum install bzip2-devel --> 再重新编译安装Python：./configure prefix=/usr/local/python3  make && make install

打开Anaconda Prompt终端：
(base) C:\Users\chenqian>Scrapy
Scrapy 1.5.1 - no active project
Usage:
  Scrapy <command> [options] [args]
Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy
  [ more ]      More commands available when run from project directory
Use "Scrapy <command> -h" to see more info about a command

Scrapy项目四步骤：
1.新建项目：Scrapy startproject myspider(项目名称)
|---myspider
    |---myspider                    # 项目的Python模块,将会从这里引用代码
    |   |---base.bash
    |   |---items.py                # 项目的目标文件
    |   |---pipelines.py            # 项目的管道文件
    |   |---settings.py             # 项目的配置文件
    |   |---spiders                 # 爬虫主程序
    |       |---base.bash
    |---Scrapy.cfg                  # 项目的配置文件
2.明确目标(编写items.py)：设置需要保存的数据字段
3.制作爬虫(spiders/xxx.py)：爬取数据
  生成Spider模板：cd myspider;Scrapy genspider itcast(爬虫名) www.itcast.cn(网站域名)
  生成CrawlSpider模板：cd myspider;Scrapy genspider -t crawl tencent(爬虫名) tencent.com(网站域名)
4.存储数据(pipelines.py)：设计管道存储爬取内容,存入文件或数据库
  当Item在Spider中被收集之后,它将会被传递到Item Pipeline,这些Item Pipeline组件按定义的顺序处理Item
运行：Scrapy crawl ***
     Scrapy crawl *** -o json/csv/xml
将myspider项目导入到pycharm运行,并选择装有Scrapy框架的Anaconda3作为Project Interpreter

Scrapy shell:
可以在不启动spider的情况下调试代码,也可以用来测试xpath和css表达式(结合IPython食用效果更佳)
案例：Scrapy shell "http://esf.fang.com/"
***(此处省略n多日志)
[s] Available Scrapy objects:
[s]   Scrapy     Scrapy module (contains Scrapy.Request, Scrapy.Selector, etc)
[s]   crawler    <Scrapy.crawler.Crawler object at 0x7fbc431bd3c8>
[s]   item       {}
[s]   request    <GET http://esf.fang.com/>
[s]   response   <200 http://esf.fang.com/>
[s]   settings   <Scrapy.settings.Settings object at 0x7fbc41831748>
[s]   spider     <DefaultSpider 'default' at 0x7fbc4095e198>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a Scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser --> 这个很有用,可以在浏览器打开通过Scrapy爬虫获取到的网页数据
In [1]:(此处调试代码)

Selectors选择器:
内置XPath和CSS Selector表达式,Selector有四个基本的方法,最常用的还是xpath
xpath()：传入xpath表达式,返回该表达式对应所有节点的selector list列表
extract()：序列化该节点为Unicode字符串并返回list -->  extract()==getall()  extract()[0]==get()
css()：传入CSS表达式,返回对应的所有节点的selector list列表,语法同BeautifulSoup4
re()：根据传入的正则表达式对数据进行提取,返回Unicode字符串list列表

Scrapy不支持分布式,Scrapy-redis可以实现Scrapy分布式爬取
conda install Scrapy-redis或者pip install Scrapy-redis
Scrapy-redis提供了下面四个组件(components)：(四种组件意味着这四个模块都要做相应的修改)
    Scheduler
    Duplication Filter
    Item Pipeline
    Base Spider
Scrapy-redis的总体思路：在Scrapy的基础上添加了一套以Redis数据库为核心的组件.让Scrapy框架支持分布式的功能,主要在Redis里做请求指纹去重,请求分配,数据临时存储.
"""
