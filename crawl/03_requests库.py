# coding=utf-8
"""
Requests: 基于urllib3实现,继承了urllib2的所有特性,并且支持HTTP连接保持和连接池,支持使用cookie保持会话
          支持文件上传,支持自动确定响应内容的编码,支持国际化的URL和POST数据自动编码
fiddler抓包工具: 是一个位于浏览器和服务器之间的代理服务器,浏览器和服务器的收发数据都会先经过fiddler,这样就可以抓取请求和响应的整个过程
"""

import requests
import json


def get():
    # 请求地址
    url = "https://www.baidu.com/s?"
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
    # 参数
    params = {"wd": "知乎"}
    # 发送get请求(params接收字典/字符串的查询参数,字典类型自动转换为url编码,不需要urlencode())
    response = requests.get(url, params=params, headers=headers, allow_redirects=False)
    # 查看响应数据类型
    print(type(response))  # <class 'requests.models.Response'>
    print(response)  # <Response [200]>
    # 查看请求方式
    print(response.request)  # <PreparedRequest [GET]>
    # 查看响应头部字符编码
    print(response.encoding)  # utf-8
    # 查看响应url
    print(response.url)  # https://www.baidu.com/s?wd=%E7%9F%A5%E4%B9%8E
    # 查看响应吗
    print(response.status_code)  # 200
    # 查看响应头
    print(response.headers)
    # 追踪重定向：是一个Response对象的列表,为了完成请求而创建了这些对象,对象列表按照从远到近的请求排序
    print(type(response.history))  # <class 'list'>
    print(response.history)  # []  -- 如果是重定向会显示[<Response [302]>, <Response [302]>...]

    # 使用response.text时,Requests会基于HTTP响应的文本编码自动解码响应内容,大多数Unicode字符集都能被无缝解码
    # print(type(response.text))  # <class 'str'>
    # 使用response.content时,返回的是服务器响应数据的原始二进制字节流,可以用来保存图片等二进制文件
    # print(type(response.content))  # <class 'bytes'>
    # 注意：如果response.text乱码可以改成response.content.decode('charset')  # charset是该网站编码
    # print(response.content.decode("gb2312"))


def post():
    # 请求地址
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
    # 请求数据
    kw = input("输入翻译内容: ")
    formdata = {
        "i": kw,
        "doctype": "json"
    }
    # 发送post请求(data是请求数据)
    response = requests.post(url, data=formdata, headers=headers)
    # 查看响应数据
    print(response.text)
    # {"type": "EN2ZH_CN", "errorCode": 0, "elapsedTime": 1, "translateResult": [[{"src": "hello", "tgt": "你好"}]]}

    # 如果是json文件也可以直接显示
    print(response.json())
    # {'translateResult': [[{'src': 'hello', 'tgt': '你好'}]], 'type': 'EN2ZH_CN', 'errorCode': 0, 'elapsedTime': 1}

    # 对比数据类型发现：response.json() 其实就是 json.loads(response.text)
    print(type(response.json()))  # dict
    print(type(json.loads(response.text)))  # dict


def ajax():
    # 需求：抓取拉勾网java工程师职位信息(详见demo03)

    # 地址栏url
    # url = "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput="
    # 真实请求地址(F12-->Network-->Headers)
    url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"

    # 请求头(有些网站做了反爬虫,调试过程中headers可以多写几个参数(ua,cookie,referer,host...)尽量让请求看上去像是真实浏览器访问的不然会故意返回500错误,此处引申出selenium)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Cookie": "JSESSIONID=ABAAABAABEEAAJA6EA181175874A387649B864C48AE01AA; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537253504; _ga=GA1.2.1735615114.1537253505; user_trace_token=20180918145145-4ebed506-bb0f-11e8-baf2-5254005c3644; LGUID=20180918145145-4ebed7dd-bb0f-11e8-baf2-5254005c3644; _gid=GA1.2.1064196434.1537253505; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=search_code; SEARCH_ID=f52a4cd1d6dd4e50b78974df963ce515; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537258174; LGSID=20180918160935-2e005133-bb1a-11e8-baf2-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20180918160935-2e0053c0-bb1a-11e8-baf2-5254005c3644",
        "Referer": "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=",
        # ...
    }

    # 请求数据
    formdata = {
        "first": "false",
        "pn": 1,
        "kd": "java"
    }

    # 发送post请求
    for i in range(1, 10):
        formdata["pn"] = i
        response = requests.post(url, data=formdata, headers=headers)
        print(response.json())


# 免费代理
def proxy01():
    """
    注意：代理类型要和目标站点的url协议保持一致,即访问http站点就要用http类型的代理;如果用https代理访问http站点,虽然也能请求成功但其实并没有走代理而是用的本地ip直接访问
         可以通过response.headers/response.text结果对比是否使用了代理ip
    """

    # 请求地址
    url = "http://httpbin.org/ip"  # ip测试网站
    # 代理IP列表
    proxies = {
        "http": "http://119.10.67.144:808",  # 假设该代理ip有效
        # "https": "https://119.10.67.144:808",
    }
    # 随机选一个
    # 发送请求(代理要加上proxies参数)
    response1 = requests.get(url)
    response2 = requests.get(url, proxies=proxies)
    # 查看响应数据
    print(response1.headers)  # {'Server': 'gunicorn/19.8.1', 'Date': 'Wed, 20 Jun 2018 02:19:10 GMT', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true'}
    print(response2.headers)  # {'Server': 'Proxy'}
    print(response1.text)  # {"origin":"106.75.64.149"} -- 真实ip
    print(response2.text)  # {"origin":"119.10.67.144"} -- 代理ip

# 私密代理
def proxy02():
    # 请求地址
    url = "https://nba.hupu.com/"
    # 私密代理IP
    proxy = {"http": "http://user:password@ip:port/"}
    # 发送请求(代理要加上proxies参数)
    response = requests.get(url, proxies=proxy)
    # 查看响应数据
    print(response.text)


def web():
    # 请求地址
    url = "http://192.168.199.107"
    # auth = (账户名, 密码)
    auth = ("user", "password")
    # 发送请求
    response = requests.get(url, auth=auth)
    # 查看响应数据
    print(response.text)


def cookie():
    # 请求地址
    url = "https://www.baidu.com/"
    # 发送请求
    response = requests.get(url)
    # 返回CookieJar对象(如果一个响应中包含了cookie,可以利用cookies参数拿到)
    cookiejar = response.cookies
    print(type(cookiejar))  # <class 'requests.cookies.RequestsCookieJar'>
    print(cookiejar)  # <RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>
    # 将cookiejar转为字典类型
    cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    print(type(cookiedict))  # <class 'dict'>
    print(cookiedict)  # {'BDORZ': '27315'}


def session():
    # 创建session对象,可以保存cookie值
    session = requests.session()
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
    # 登录页面(通常带有login/sign字眼)：可通过fiddler抓包获取登录时的webform表单数据
    url_login = "https://signin.aliyun.com/1065151969971491/login.htm"
    # 登录后的其它页面
    url = "https://ide-cn-shanghai.data.aliyun.com/web/folder/listObject?keyword=&objectId=-1&projectId=29820&reRender=true&tenantId=171224272675329&type=1"
    # 需要登录的用户名和密码
    data = {"user_principal_name": "chenqian@1065151969971491", "password_ims": "Cq111111"}
    # 发送附带用户信息的请求(此时session已包含登录后的cookie值)
    session.post(url_login, data=data, headers=headers)
    # 然后就可以访问登录后的其它页面了
    response = session.get(url, headers=headers, allow_redirect=False)
    print(response.text)


if __name__ == "__main__":
    get()
    # post()
    # ajax()
    # proxy01()
    # proxy02()
    # web()
    # cookie()
    # session()
