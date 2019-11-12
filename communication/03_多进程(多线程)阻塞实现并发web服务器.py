# coding=utf-8
"""
HTTP协议：超文本传输协议,是从互联网服务器向本地浏览器传输超文本的协议
get是从服务器上获取数据,post是向服务器传送数据
get请求：参数显式的写在浏览器的url中,例如：http://www.baidu.com/s?wd=Chinese
post请求：参数在请求体当中,以隐式的方式发送,请求的参数包含在"Content-Type"消息头里,指明该消息体的媒体类型和编码 ---> 表单提交、大文本传输

http请求：请求行,请求头(10~19),空行,请求体
GET / HTTP/1.1                                                   ---> 请求行(请求方法+url+协议版本)
Host: fanyi.youdao.com                                           ---> 主机和端口号
Connection: keep-alive                                           ---> 连接类型为长连接
Upgrade-Insecure-Requests                                        ---> 升级为HTTPS请求
Accept: application/json, text/javascript, */*; q=0.01           ---> 浏览器接收的文件类型
User-Agent: ...                                                  ---> 浏览器版本(重要)
Referer: http://fanyi.youdao.com/                                ---> 页面跳转处(重要)
Accept-Encoding: gzip, deflate                                   ---> 浏览器接收的文件压缩格式
Accept-Language: zh-CN,zh;q=0.9                                  ---> 浏览器接收的语言,q表示权重
Cookie: ...                                                      ---> Cookie(重要)
X-Requested-With: XMLHttpRequest                                 ---> 说明是ajax异步请求

i=rabbit&from=AUTO&to=AUTO&smartresult=dict&client=fanyideskweb  ---> 请求体(post才有)

http响应：响应行,响应头,空行,响应体
HTTP/1.1 200 OK                                                  ---> 响应行(必须)
...                                                              ---> 响应头

<!DOCTYPE html>                                                  ---> 响应体

http状态码：告诉客户端服务器的执行状态
200：请求成功
301：永久性重定向    www.jindong.com --> www.jd.com
302：临时性重定向    未登录时访问个人中心会跳转到登录页面
403：没有权限访问
404：找不到资源
500：服务器错误

cookie：由于http协议是无状态的,服务器无法识别多个请求是否由同一个用户发起,网站服务器为了辨别用户身份和进行session跟踪会在response中返回一段
        cookie值存储在浏览器上,cookie可以保持登录信息到用户下次与服务器的会话,浏览器存储的cookie大小一般不超过4k
"""
import socket
import re
import multiprocessing
import threading
import gevent
from gevent import monkey

monkey.patch_all()

def service(new_socket):
    """为该客户端服务(短连接)"""

    # 1.接收请求：请求的html文件里可能包含<img src=""></img>等超链接,每个超链接都会发送一个请求
    # GET /index.html HTTP/1.1  GET /images/qt-logo.png HTTP/1.1  GET /classic.css HTTP/1.1  GET /favicon.ico HTTP/1.1
    request = new_socket.recv(1024).decode()  # 阻塞
    print(request)
    print("-" * 100)
    # 将http请求的多行字符串切割成行列表
    lines = request.splitlines()
    # 正则匹配请求行的url：取出前面不是/后面不是空格的这部分
    filename = re.match('[^/]+(/[^ ]*)', lines[0])  # 请求行'GET / HTTP/1.1'
    if filename:
        filename = filename.group(1)
        # /代表首页
        if filename == "/":
            filename = "/index.html"

    # 2.响应请求
    try:
        # 此处可能读不到文件,需要try/except
        with open('./html' + filename, 'rb') as f:
            # 读取url对应的html内容作为响应体返回
            response_body = f.read()
    except Exception as e:
        print(e)
        # 请求失败
        response_head = "HTTP/1.1 404 not found\r\n" + "\r\n" + "<h1>sorry~<h1>"
        new_socket.send(response_head.encode())
    else:
        # 请求成功
        response_head = "HTTP/1.1 200 ok\r\n" + "\r\n"
        new_socket.send(response_head.encode())
        new_socket.send(response_body)
    finally:
        # 3.关闭连接(四次挥手),结束本次会话
        new_socket.close()


def main():
    """使用进程、线程、协程实现并发http服务器(效率很低)"""

    # 1.创建socket对象,socket默认是阻塞的
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # 设置允许重复使用端口
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 2.绑定地址
    server_socket.bind(("localhost", 8888))
    # 3.开启监听
    server_socket.listen(128)
    while True:
        # 4.接收连接(三次握手)
        new_socket, addr = server_socket.accept()  # 阻塞
        # 5.响应客户端请求
        # (1).多进程实现
        # p = multiprocessing.Process(target=service, args=(new_socket,))
        # p.start()
        # # linux上所有的东西都对应操作系统的一个文件描述符fd(一个数字),操作系统默认012对应标准输入/标准输出/错误输出,应用程序的fd从3开始
        # # 由于进程间相互独立,创建子进程时会复制父进程的资源,此时有两个socket对象指向操作系统的同一个fd,必须等父进程和子进程的socket对象
        # # 都关闭之后fd才会消失,否则浏览器会一直转圈处于等待状态;而创建子线程时是共享资源的,不存在这种现象,所以只要子线程关闭之后fd就消失了
        # new_socket.close()

        # (2).多线程实现
        # t = threading.Thread(target=service, args=(new_socket,))
        # t.start()

        # (3).协程实现：使用猴子补丁将阻塞的地方都改成非阻塞
        gevent.spawn(service, new_socket)


if __name__ == '__main__':
    main()