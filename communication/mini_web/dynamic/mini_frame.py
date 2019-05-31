# coding=utf-8
import pymysql
import re

# PATH_FUNC_DICT = {
#     "/index.html": index,
#     "/center.html": center,
# }
PATH_FUNC_DICT = dict()


# 通过装饰器实现web框架路由功能
def route(path):
    def inner(func):
        PATH_FUNC_DICT[path] = func

    return inner


@route("/index.html")
def index():
    # 读取html文件
    with open("./templates/index.html", encoding="utf8") as f:
        content = f.read()

    records = ()
    # 连接数据库
    try:
        conn = pymysql.connect(host='192.168.152.11', port=3306, user='root', password='root', db='mini_web',
                               charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM info;")
            records = cur.fetchall()
            print(len(records))
        except Exception as e:
            print("---%d行代码异常：%s---" % (e.__traceback__.tb_lineno, e))
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        print("---%d行代码异常：%s---" % (e.__traceback__.tb_lineno, e))

    # 前端页面待填充数据模板
    tr_template = """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007">
        </td>
    </tr>
    """
    # 往前端页面填充真实数据
    html = ""
    for record in records:
        html += tr_template % (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
    content = re.sub('{%content%}', html, content)

    # 返回结果
    return content


@route("/center.html")
def center():
    # 读取html文件
    with open("./templates/center.html", encoding="utf8") as f:
        content = f.read()

    records = ()
    # 连接数据库
    try:
        conn = pymysql.connect(host='192.168.152.11', port=3306, user='root', password='root', db='mini_web',
                               charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info FROM info AS i INNER JOIN focus AS f ON i.id=f.info_id;")
            records = cur.fetchall()
            print(len(records))
        except Exception as e:
            print("---%d行代码异常：%s---" % (e.__traceback__.tb_lineno, e))
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        print("---%d行代码异常：%s---" % (e.__traceback__.tb_lineno, e))

    # 前端页面待填充数据模板
    tr_template = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
            </td>
            <td>
                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="300268">
            </td>
        </tr>
        """
    # 往前端页面填充真实数据
    html = ""
    for record in records:
        html += tr_template % (record[0], record[1], record[2], record[3], record[4], record[5], record[6])
    content = re.sub('{%content%}', html, content)

    # 返回结果
    return content


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

    # if filename == "/index.html":
    #     return index()
    # elif filename == "/center.html":
    #     return center()
    # elif filename == "***.html":
    #     pass
    # # ...
    # else:
    #     return "---当前请求页面无效---"

    # 改进版
    try:
        return PATH_FUNC_DICT[filename]()
    except Exception as e:
        return "当前请求异常：%s" % e
