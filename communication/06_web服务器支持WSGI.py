# coding=utf-8
import socket
import re
import multiprocessing
import sys
import importlib

class WSGIServer(object):
    def __init__(self, port, application, static_path):
        # 1.创建socket对象,socket默认是阻塞的
        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # 设置允许重复使用端口,因为四次挥手后客户端(服务器)资源不会立马消失而是保持2~4分钟,如果服务器先挂了客户端再访问就会报错：端口已被占用
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 2.绑定地址
        self.server_socket.bind(("192.168.152.11", port))
        # 3.开启监听
        self.server_socket.listen(128)

        self.application = application
        self.static_path = static_path

    def service(self, new_socket):
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
        # a).静态资源部分
        if not filename.endswith(".html"):
            try:
                with open(self.static_path + filename, 'rb') as f:
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
        # b).动态资源部分
        else:
            # 向application函数传递的字典信息
            env = dict()
            env["PATH"] = filename
            # body部分
            response_body = self.application(env, self.start_response)
            # header部分
            response_head = "HTTP/1.1 %s\r\n" % self.status
            for each in self.headers:
                response_head += "%s:%s\r\n" % (each[0], each[1])
            response_head += "\r\n"
            # 拼接head和body返回
            response = response_head + response_body
            new_socket.send(response.encode())
        # 关闭连接(四次挥手)
        new_socket.close()

    def start_response(self, status, headers):
        self.status = status
        self.headers = headers

    def run_forever(self):
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


def main():
    if len(sys.argv) == 3:
        # 参数2是端口
        port = int(sys.argv[1])
        # 参数3是模块:函数
        frame_app = sys.argv[2]  # mini_frame:application
        # 正则匹配frame_app
        res = re.match('([^:]+):(.*)', frame_app)
        if res:
            frame_name = res.group(1)
            app_name = res.group(2)
            # 动态加载mini_frame模块,而不是import写死
            with open("mini_web/web_server.conf") as f:
                conf_info = eval(f.read())
            # 将存放mini_frame模块的路径dynamic加载到sys.path
            sys.path.append(conf_info['dynamic_path'])
            # frame = __import__(frame_name)
            frame = importlib.import_module(frame_name)
            # 获取模块中的属性
            application = getattr(frame, app_name)
            wsgi = WSGIServer(port, application, conf_info['static_path'])
            wsgi.run_forever()
        else:
            print("参数错误,请参照如下格式：python3 xxx.py 9999 mini_frame:application")
    else:
        print("参数错误,请参照如下格式：python3 xxx.py 9999 mini_frame:application")


if __name__ == '__main__':
    main()

