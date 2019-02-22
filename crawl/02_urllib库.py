# coding=utf8
"""
http请求主要分为get和post两种:
get是从服务器上获取数据,post是向服务器传送数据
get请求: 参数显示在浏览器的url中,例如: http://www.baidu.com/s?wd=Chinese
post请求: 参数在请求体当中,以隐式的方式发送,请求的参数包含在"Content-Type"消息头里,指明该消息体的媒体类型和编码
注意: 尽量避免get方式提交表单,可能会导致安全问题

http状态码汇总:
200：请求成功
301：永久性重定向    www.jindong.com --> www.jd.com
302：临时性重定向    未登录时访问个人中心会跳转到登录页面
403：没有权限访问
404：找不到资源
500：服务器错误

http请求包含: 请求行,请求头,空行,请求体(post)
POST http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule HTTP/1.1
Host: fanyi.youdao.com
Connection: keep-alive
Content-Length: 202
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://fanyi.youdao.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://fanyi.youdao.com/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: OUTFOX_SEARCH_USER_ID=-388253338@10.169.0.84; JSESSIONID=aaal-CPvBwa9P85-5f7ew; OUTFOX_SEARCH_USER_ID_NCOO=2060469077.47785; fanyi-ad-id=39535; fanyi-ad-closed=1; ___rl__test__cookies=1517115259862

i=rabbit&from=AUTO&to=AUTO&smartresult=dict&client=fanyideskweb&salt=1517115259867&sign=cb455e27816176d6dbdbd09cfa87c8cd&doctype=json&version=2.1&keyfrom=fanyi.web&action=FY_BY_REALTIME&typoResult=false


urllib在python3中被改为urllib.parse
urllib2在python3中被改为urllib.request

1、urllib.parse模块
urlencode(): 编码   --将{key:value}字典转换成"key=value"字符串,拼接成能被web服务器接受的url
unquote(): 解码

2、urllib.request模块
request方法:
Request(): 构造请求对象,主要有3个参数: url,data(区分get/post请求): 默认为空;headers(http报头的键值对): 默认为空;
urlopen(): 发送请求
add_header(): 添加/修改一个HTTP报头
get_header(): 获取一个已有的HTTP报头,注意第一个字母大写,后面全小写

response方法:
read(): 读取服务器返回文件的内容
info(): 返回服务器响应的HTTP报头
getcode(): 返回HTTP请求的响应码
geturl(): 返回返回实际数据的url,防止重定向问题
"""

import urllib.request
import urllib.parse
import http.cookiejar
import random


def urllib01():
    # 待爬取url
    url = "http://www.baidu.com/"

    # 不同浏览器在发送请求的时候,会有不同的User-Agent头
    # urllib2默认的User-Agent头为：Python-urllib/x.y,需要伪装成浏览器
    # HTTP报头
    ua_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
    }

    # User-Agent列表
    ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
    ]

    # 随机选一个(针对反爬虫)
    user_agent = random.choice(ua_list)
    # print(type(user_agent))
    # print(user_agent)

    # 通过request()方法构造一个请求对象
    request = urllib.request.Request(url)  # 此时User-Agent: Python-urllib/3.5

    # 通过add_header()方法添加/修改一个HTTP报头
    request.add_header("User-Agent", user_agent)

    # 通过urlopen()方法发送请求,并返回服务器响应内容
    response = urllib.request.urlopen(request)

    # 输出服务器相应内容
    html = response.read().decode("utf-8")
    print(type(html))

    # 通过get_header()方法获取一个已有的HTTP报头,注意第一个字母大写,后面全小写
    print(request.get_header("User-agent"))

    # 输出HTTP响应码,成功返回200,4服务器页面出错,5服务器问题
    print(response.getcode())

    # 输出返回实际数据的url,防止重定向问题
    print(response.geturl())

    # 输出服务器相应的HTTP报头
    print(response.info)


def get():
    # 目标url
    url = "http://www.baidu.com/s"
    # 用户接口输入
    keyword = input("请输入要搜索的关键字: ")
    # url转码
    wd = urllib.parse.urlencode({"wd": keyword})
    # wd1 = urllib.parse.unquote(wd)
    print(wd)
    # 请求头
    headers = {"User-Agent": "Mozilla..."}
    # 拼接url
    fullurl = url + "?" + wd
    print(fullurl)
    # 构造请求对象
    request = urllib.request.Request(fullurl, headers=headers)
    # 发送请求
    response = urllib.request.urlopen(request)
    print(type(response.read()))  # <class 'bytes'>
    # 输出
    print("data: %s" % response.read().decode("utf-8"))
    print("info: %s" % response.info())
    print("code: %s" % response.getcode())  # 200
    print("url: %s" % response.geturl())  # http://www.baidu.com/s?wd=%E7%BE%8E%E5%A5%B3


def post():
    """
    注意: post请求的url要通过抓包获取,不是浏览器上显示的url
    """

    # {"errorCode":50}问题: 将url里的translate_o改成translate
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"

    # 完整的请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}

    # 用户接口输入
    kw = input("输入要翻译的内容:")

    # post请求数据(抓包时WebForms里的参数)
    formdata = {
        "i": kw,
        "doctype": "json"
    }

    # url转码
    data = urllib.parse.urlencode(formdata)
    # TypeError: POST data should be bytes or an iterable of bytes. It cannot be of type str.
    data1 = bytes(data, encoding="utf-8")

    # 创建请求对象(有data参数说明是post请求)
    request = urllib.request.Request(url, data=data1, headers=headers)
    # 向服务器提交请求
    response = urllib.request.urlopen(request)
    # 服务器响应数据
    result = response.read().decode("utf-8")
    print(result)


def ajax():
    """
    ajax动态加载的页面,数据来源是json;直接对ajax地址get/post就返回json数据了
    """

    # ajax页面的url也是通过抓包获取
    url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action="

    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}

    # post请求数据(分析抓包时WebForms里的参数找出规律)
    formdata = {
        "start": "0",
        "limit": "20"
    }

    # URL转码
    data = urllib.parse.urlencode(formdata)
    # TypeError: POST data should be bytes or an iterable of bytes. It cannot be of type str.
    data = bytes(data, encoding="utf-8")

    # 创建请求对象
    request = urllib.request.Request(url, data=data, headers=headers)
    # 向服务器提交请求
    response = urllib.request.urlopen(request)
    # 服务器响应数据
    result = response.read().decode("utf-8")

    # 保存到本地
    with open("D://movie.json", "w", encoding="utf-8") as f:
        f.write(result)


"""
cookie: 网站服务器为了辨别用户身份和进行Session跟踪而储存在浏览器上的一段文本文件,cookie可以保持登录信息到用户下次与服务器的会话
Python处理Cookie,一般是通过http.cookiejar模块和urllib.request模块的HTTPCookieProcessor处理器类一起使用
http.cookiejar模块: 存储cookie对象
HTTPCookieProcessor处理器: 处理cookie对象,并构建handler对象
"""
def cookie01():
    """
    1、访问网站获取cookie并输出在控制台
    """

    # 创建cookieJar对象用来保存cookie
    cookieJar = http.cookiejar.CookieJar()
    # 创建cookie处理器对象
    cookie_handler = urllib.request.HTTPCookieProcessor(cookieJar)
    # 创建opener
    opener = urllib.request.build_opener(cookie_handler)
    # 以get方式访问页面,会自动将cookie保存到cookieJar
    res1 = opener.open("http://www.baidu.com")
    # 输出页面
    # print(response.read().decode("utf-8"))
    # 从cookieJar获取cookie
    cookieStr = ""
    for item in cookieJar:
        cookieStr = cookieStr + item.name + "=" + item.value + ";"
    # 打印cookie
    print(cookieStr)


def cookie02():
    """
    2、访问网站获取cookie并保存到本地
    """

    # 本地文件路径
    filename = "C://users/qmtv/cookie.txt"
    # 创建cookieJar对象(用MozillaCookieJar,有save()实现)
    cookieJar = http.cookiejar.MozillaCookieJar(filename)
    # 创建cookie处理器对象
    cookie_handler = urllib.request.HTTPCookieProcessor(cookieJar)
    # 创建opener
    opener = urllib.request.build_opener(cookie_handler)
    # 访问页面,会自动将cookie保存到cookieJar
    res2 = opener.open("http://www.baidu.com")
    # 保存cookie到本地
    cookieJar.save()


def cookie03():
    """
    3、从文件获取cookie,作为请求的一部分访问页面
    """

    # 创建cookieJar对象(用MozillaCookieJar,有load()实现)
    cookieJar = http.cookiejar.MozillaCookieJar()
    # 从文件中读取cookie内容
    cookieJar.load("C://users/qmtv/cookie.txt")
    # 创建cookie处理器对象
    cookie_handler = urllib.request.HTTPCookieProcessor(cookieJar)
    # 创建opener
    opener = urllib.request.build_opener(cookie_handler)
    # 访问页面
    res3 = opener.open("http://www.baidu.com")
    # 输出
    print(res3.read().decode("utf-8", "ignore"))


"""
urlopen()不支持代理和cookie等http/https高级功能的问题:
解决方案: 使用相关handler处理器来创建特定功能的处理器对象(其实urlopen也是一个特殊的opener)

1、通过urllib.request模块创建相关handler处理器对象
2、通过urllib.request模块的build_opener()方法使用这些处理器对象,创建自定义opener对象
3、opener对象调用open()方法发送http请求
"""
def http_handler():
    """
    HTTPHandler处理器
    """

    # 创建httphandler处理器,专门处理http请求
    # debuglevel参数默认0,设为1会自动打开Debug log模式,程序执行时会打印收发包信息,方便调试
    http_handler = urllib.request.HTTPHandler(debuglevel=1)
    # 创建opener对象
    opener = urllib.request.build_opener(http_handler)
    # 创建request对象
    request = urllib.request.Request("http://www.baidu.com/")
    # 调用open()方法发送请求
    response = opener.open(request)
    # 输出结果
    print(response.read().decode("utf-8"))


def proxy_handler01():
    """
    ProxyHandler处理器: 使用代理IP,针对反爬虫
    很多网站会通过检测某一时段内IP的访问次数(流量统计、系统日志等),将不正常的IP封掉
    所以我们可以设置一些代理服务器,每隔一段时间换一个代理,就算IP被禁止,依然可以换个IP继续爬取
    """

    # 代理IP列表
    proxy_list = [
        {"http": "113.89.54.209:9999"},
        {"http": "58.220.95.107:8080"},
        {"http": "163.125.17.110:8888"}
    ]
    # 随机选一个
    proxy = random.choice(proxy_list)
    # 创建代理服务器,有代理IP
    httpproxy_handler = urllib.request.ProxyHandler(proxy)
    # 创建代理服务器,没有代理IP
    noproxy_handler = urllib.request.ProxyHandler({})
    # 设置开关
    proxySwitch = True
    # 判断
    if proxySwitch:
        opener = urllib.request.build_opener(httpproxy_handler)
    else:
        opener = urllib.request.build_opener(noproxy_handler)
    # 创建request对象
    request = urllib.request.Request("http://www.baidu.com")
    # 发送请求(此时只有opener.open()方法才会使用代理,而urlopen()方法不会使用代理)
    response = opener.open(request)
    # opener全局设置(此时不管opener.open()还是urlopen()都会使用代理)
    urllib.request.install_opener(opener)
    # 输出结果
    print(response.read().decode("utf-8"))


def proxy_handler02():
    """
    但是免费代理有很大缺陷,可以花钱买专门的代理,通过用户名/密码授权使用
    urllib.request模块:
    HTTPPasswordMgrWithDefaultRealm(): 保存私密代理的用户密码
    ProxyBasicAuthHandler(): 处理代理的身份验证。
    """

    # 用户和密码
    user = "test"
    passwd = "test"
    # 代理服务器
    proxy = "163.125.17.110:8888"
    # 创建密码管理对象
    passwdMgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    # 添加账户信息(第一个参数realm是与远程服务器相关的域信息,一般写None,后面三个参数分别是: 代理服务器、用户名、密码)
    passwdMgr.add_password(None, proxy, user, passwd)
    # 创建代理基础用户名/密码的处理器对象
    proxyauth_handler = urllib.request.ProxyBasicAuthHandler(passwdMgr)
    # 创建opener对象
    opener = urllib.request.build_opener(proxyauth_handler)
    # 创建request对象
    request = urllib.request.Request("http://www.baidu.com")
    # 发送请求
    response = opener.open(request)
    # 输出结果
    print(response.read().decode("utf-8"))


if __name__ == "__main__":
    urllib01()
    # get()
    # post()
    # ajax()
    # cookie01()
    # cookie02()
    # cookie03()
    # HTTPHandler()
    # ProxyHandler01()
    # ProxyHandler02()
