# coding=utf-8

# PATH_FUNC_DICT = {
#     "/index.py": index,
#     "/center.py": center,
# }
PATH_FUNC_DICT = dict()

# 通过装饰器实现web框架路由功能
def route(path):
    def inner(func):
        PATH_FUNC_DICT[path] = func
    return inner

@route("/index.py")
def index():
    with open("./templates/index.html", encoding="utf8") as f:
        return f.read()

@route("/center.py")
def center():
    with open("./templates/center.html", encoding="utf8") as f:
        return f.read()

def application(env, start_response):
    """
    WSGI(Web Server Gateway Interface)：web服务器必须具备wsgi接口,调用flask、django等web框架协同工作
    浏览器---web服务器---WSGI协议---web框架
    WSGI接口要求Web框架实现一个响应http请求的application函数
    :param env: 一个包含http请求信息的字典对象
    :param start_response: 一个发送http响应的函数
    :return:
    """

    # 返回header
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    # 返回body
    filename = env['PATH']

    # if filename == "/index.py":
    #     return index()
    # elif filename == "/center.py":
    #     return center()
    # elif filename == "***.py":
    #     pass
    # # ...
    # else:
    #     return "---当前请求页面无效---"

    # 改进版
    try:
        return PATH_FUNC_DICT[filename]()
    except Exception as e:
        return "当前请求异常 %s" % e