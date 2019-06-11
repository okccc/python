"""
视图是MVT框架的核心：接收请求(V)-->获取数据(M)-->返回结果(T)
Django通过视图接收请求,通过模型获取数据,调用模板展示结果

views
1.视图是定义在views.py中的函数,接收request对象(包含请求信息)作为第一个参数,Django提供render()函数简化了视图调用模板、构造上下文
2.定义完视图需要配置对应的url路由,每个app都会有单独的urls.py文件,然后将各个app的urls添加到project的urls.py文件
url路由包括正则表达式和视图两部分 --> Django使用正则匹配请求的url,一旦匹配成功就会调用对应的视图
注意：正则只匹配路径部分(即去除域名和参数的字符串)
http://192.168.233.11:7777/booktest/1/?i=1&j=2 --> 只匹配booktest/1/部分
匹配过程：先与project的url路由匹配,成功后再用剩余部分与app中的url路由匹配
先拿'booktest/'匹配project中的urls.py,再拿'1/'匹配app中的urls.py

url反向解析：{% url 'namespace:name' p1 p2 .. %} --> 请求链接由url的配置(namespace:name)动态生成而不是手动拼接
    好处：当修改url匹配规则时不需要额外维护模板里的请求链接,也可以避免链接后面漏掉'/'的问题
模板继承
    模板继承可以实现页面内容的重用 --> 比如同一个网站各个页面的头部/底部都是一样的,这些内容只需定义在父模板中即可
    block标签：在父模板中预留区域由子模板填充; extends继承：写在模板文件的第一行,父模板已有的字模板不需要重写
    定义父模板base.html: {% block block_name %}...{% endblock %}
    定义子模板index.html: {% extends "base.html" %}...{% block block_name %}...{% endblock %}
html转义
    如果输出的字符串中包含html标签(比如<>),需要将包含的html标签转义成字符串输出而不被解释执行
    < 会转换为&lt;
    > 会转换为&gt;
    ' (单引号) 会转换为&#39;
    " (双引号)会转换为 &quot;
    & 会转换为 &amp;
csrf跨域攻击
    Cross Site Request Forgery: 跨站请求伪造,只针对post请求
    跨站攻击：某些恶意网站上包含链接、表单按钮或者JS,它们会利用登录过的用户在浏览器中的认证信息试图在你的网站上完成某些操作
    django自带csrf中间件,只要在模板的form表单中添加{% csrf_token %}即可
验证码
    csrf_token没啥用还是得用验证码
分页

缓存
    减少服务器运算,提升服务器性能

步骤：定义视图函数 --> 配置urlconf --> 设计html模板

"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *

def index(request):
    """
    HttpRequest对象由Django自动创建,HttpResponse对象自己开发
    服务器接收http协议的请求后,会根据报文创建HttpRequest对象,并将其作为视图函数的第一个参数
    GET属性: 一个类字典对象,包含get请求方式的所有参数
    POST属性: 一个类字典对象,包含post请求方式的所有参数
    COOKIES属性: 一个标准的Python字典,包含所有的cookie,键和值都为字符串
    session属性: 一个既可读又可写的类字典对象,表示当前的会话,只有当Django启用会话时才可用,详细内容见"状态保持"
    is_ajax()方法: 如果请求是通过XMLHttpRequest发起的,则返回True
    """

    # 调通程序
    # return HttpResponse("hello")
    # 使用模板
    template_name = "booktest/index.html"
    # 构造字典类型的上下文(要往模板中传递的数据)
    context = {"books": BookInfo.objects.all()}
    # 返回渲染后的模板
    # return HttpResponse(loader.get_template(template_name).render(context))
    return render(request, template_name, context)

def detail01(request, bid):
    context = {"heros": BookInfo.objects.get(id=bid).heroinfo_set.all()}
    return render(request, "booktest/detail01.html", context)

def detail02(request, bid, hid):
    # 构造上下文
    context = {"hero": BookInfo.objects.get(id=bid).heroinfo_set.get(id=hid)}
    # 渲染模板
    return render(request, "booktest/detail02.html", context)

def add(request):
    b = BookInfo()
    b.title = "红楼梦"
    b.pub_date = '2019-01-01'
    b.reading = 10
    b.comments = 5
    b.save()
    return redirect(to='/booktest/index')

def delete(request, num):
    b = BookInfo.objects.get(id=num)
    b.delete()
    return redirect(to='/booktest/index')

def areas(request):
    area = AreaInfo.objects.get(title='常州市')
    parent = area.parent
    children = area.areainfo_set.all()
    context = {"area": area, "parent": parent, "children": children}
    return render(request, "booktest/areas.html", context)

def cookie01(request):
    """
    http协议是无状态的,客户端与服务器使用套接字通信完成之后会关闭当前socket连接,所以每次通信都是一次新的会话而不会记得之前的通信状态
    可以通过cookie或session两种方式实现会话保持
    会话保持的目的是在一段时间内跟踪请求者的状态从而实现跨页面访问当前请求者的数据
    类cookie：适用于记住用户名这种安全性不高的场景
    session：适用于账号密码、余额、等级、验证码等安全性较高的场景
    """
    response = HttpResponse("cookie测试")
    # 设置cookie
    # response.set_cookie(key='k1', value='v1', max_age=7*24*3600)
    # 删除cookie
    response.delete_cookie(key='k1')
    return response

def session01(request):
    # 设置session键值对
    request.session["username"] = "grubby"
    request.session["age"] = 18
    # 设置过期时间：默认两周,0表示关闭浏览器失效
    request.session.set_expiry(5)
    # 删除指定session_key的session_data值
    del request.session["age"]
    # 清空所有session_key的session_data值
    request.session.clear()
    # 删除所有session_key,并删除Cookie中的sessionid
    request.session.flush()
    return HttpResponse("session测试")

def login(request):
    """显示登录页面"""
    # 先判断是否是已登录用户
    if "is_login" in request.session:
        # 已登录直接跳转到首页
        return redirect(to='/booktest/index')
    else:
        # 未登录,看看是否记住用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
        else:
            username = ""
        # 报错：You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set
        # 原因：form表单提交的action路径要和URL路由对应的正则保持格式一致,即是否以/结尾
        return render(request, "booktest/login.html", {"username": username})

def login_check(request):
    """登录校验"""
    print(request.method)  # POST
    print(type(request.POST))  # <class 'django.http.request.QueryDict'>
    # 获取form表单数据
    # request对象的GET/POST请求返回的是QueryDict对象,类似字典但是允许一键多值的情况
    # get()返回单个值,如果有多个值就取最后一个  getlist()返回列表
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    # 校验用户名和密码
    if username == "grubby" and password == "grubby":
        # 登陆成功
        # 注意：redirect、href、action的path要以/开头表示绝对路径http://ip:port/path,不然是相对路径http://ip:port/current_path/path
        response = redirect(to='/booktest/index')
        # 判断是否要记住用户名
        if remember == "on":
            response.set_cookie("username", username, max_age=7*24*3600)
        # 记住用户登录状态
        request.session["is_login"] = True
        return response
    else:
        # 登陆失败
        return redirect(to='/booktest/login')

def login_ajax(request):
    """显式ajax登录页面"""
    return render(request, "booktest/login_ajax.html")

def login_ajax_check(request):
    """ajax登录校验"""
    print(request.method)
    # 获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 进行校验,返回json数据
    if username == 'grubby' and password == 'grubby':
        # 用户名密码正确
        # return redirect('/index')  ajax请求都在后台,不能返回页面或者重定向,必须返回JsonResponse()
        return JsonResponse({'res': 1})
    else:
        # 用户名或密码错误
        return JsonResponse({'res': 0})

def template01(request):
    """模板语言包括：变量{{ variable }}、标签{% tag %}、过滤器{{ variable|filter }}、注释{#...#}"""

    # 变量{{key.value}}前面的key可能是字典、对象或列表
    dict_data = {"title": "这是字典"}
    object_data = BookInfo.objects.get(id=1)
    list_data = [1, 2, 3]
    context1 = {"dict_data": dict_data, "list_data": list_data, "object_data": object_data}
    # 单行注释{# #} 多行注释{# comment #}{# endcomment #}
    books = BookInfo.objects.all()
    context2 = {"books": books}
    return render(request, "booktest/template.html", context2)

def inherit(request):
    """模板继承"""
    return render(request, "booktest/child.html", )

def escape(request):
    """模板转义"""
    # 模板对上下文传递的字符串进行输出时会转义 < > 等字符,显式的是原生字符串
    return render(request, "booktest/escape.html", {"context": "<h1>hello</h1>"})



