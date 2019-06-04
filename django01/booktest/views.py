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

templates
在project根目录下创建templates目录并在settings.py中设置TEMPLATES的DIRS值
模板语言包括：变量{{ variable }}、标签{% tag %}、过滤器{{ variable|filter }}、注释{{ #...# }}
    for标签：{% for ... in ... %}...{{ forloop.counter }}...{% empty %}...{% endfor %}
    if标签：{% if ... %}...{% elif ... %}...{% else %}...{% endif %}
    单行注释：{# 这是注释 #}
    多行注释：{% comment %}...{% endcomment %}
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
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import BookInfo, HeroInfo

def index(request):
    # 调通程序
    # return HttpResponse("hello")

    # 模板名称
    template_name = "booktest/index.html"
    # 构造字典类型的上下文(要往模板中传递的数据)
    context = {"books": BookInfo.objects.all()}
    # 返回渲染后的模板
    # return HttpResponse(loader.get_template(template_name).render(context))
    return render(request, template_name, context)

def detail01(request, num):
    # 构造上下文
    context = {"heros": BookInfo.objects.get(id=num).heroinfo_set.all()}
    # 渲染模板
    return render(request, "booktest/detail01.html", context)

def detail02(request, num1, num2):
    # 构造上下文
    context = {"hero": BookInfo.objects.get(id=num1).heroinfo_set.get(id=num2)}
    # 渲染模板
    return render(request, "booktest/detail02.html", context)