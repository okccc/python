# coding=utf-8
import socket
import re
import multiprocessing
from communication.dynamic import application

class WSGIServer(object):
    def __init__(self):
        # 1.创建socket对象,socket默认是阻塞的
        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # 设置允许重复使用端口,因为四次挥手后客户端(服务器)资源不会立马消失而是保持2~4分钟,如果服务器先挂了客户端再访问就会报错：端口已被占用
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 2.绑定地址
        self.server_socket.bind(("localhost", 8888))
        # 3.开启监听
        self.server_socket.listen(128)

    @staticmethod
    def service(new_socket):
        """为该客户端服务(短连接)"""

        # 1.接收请求：请求的html文件里可能包含<img src=""></img>等超链接,每个超链接都会发送一个请求
        # GET /index.html HTTP/1.1  GET /images/qt-logo.png HTTP/1.1  GET /classic.css HTTP/1.1  GET /favicon.ico HTTP/1.1
        request = new_socket.recv(1024).decode()  # 阻塞
        print(request)
        print("-" * 100)
        # 将http请求的多行字符串切割成行列表
        lines = request.splitlines()
        # 正则匹配请求行的path：取出前面不是/后面不是空格的这部分
        filename = re.match('[^/]+(/[^ ]*)', lines[0])  # 请求行'GET /xxx.html HTTP/1.1'
        if filename:
            filename = filename.group(1)
            # /代表首页
            if filename == "/":
                filename = "/index.html"
        # 2.响应请求
        # 静态资源部分
        if not filename.endswith(".py"):
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
        # 动态资源部分
        else:
            response_head = "HTTP/1.1 200 ok\r\n" + "\r\n"
            response_body = application(filename)
            new_socket.send(response_head.encode())
            new_socket.send(response_body.encode("gbk"))
        # 关闭连接(四次挥手)
        new_socket.close()

    def main(self):
        """使用进程实现并发http服务器(效率很低)"""
        while True:
            # 4.接收连接(三次握手)
            new_socket, addr = self.server_socket.accept()  # 阻塞
            # 5.响应客户端请求
            # (1).多进程实现
            p = multiprocessing.Process(target=self.service, args=(new_socket,))
            p.start()
            # linux上所有的东西都对应操作系统的一个文件描述符fd(一个数字),操作系统默认012对应标准输入/标准输出/错误输出,应用程序的fd从3开始
            # 由于进程间相互独立,创建子进程时会复制父进程的资源,此时有两个socket对象指向操作系统的同一个fd,必须等父进程和子进程的socket对象
            # 都关闭之后fd才会消失,否则浏览器会一直转圈处于等待状态;而创建子线程时是共享资源的,不存在这种现象,所以只要子线程关闭之后fd就消失了
            new_socket.close()


if __name__ == '__main__':
    wsgi = WSGIServer()
    wsgi.main()
