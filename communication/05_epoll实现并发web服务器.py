# coding=utf-8
"""
应用程序自己产生的内存空间和操作系统的内存空间是分开的,
操作系统调用应用程序时会将应用程序内socket的fd复制到kernel轮询检测,进程、线程、协程实现的并发服务器性能瓶颈就在这里
epoll原理：
1.开辟一块应用程序和操作系统共享的内存空间,减少应用程序向操作系统复制fd的过程
2.用事件监听机制(谁饿谁举手而不是挨个问)代替轮询(一直狂转看有没有客户端连进来)
"""
import socket
import select  # select.epoll()只在linux生效
import re

def service(client_socket, request):
    """为该客户端服务(长连接)"""

    # 1.接收请求：请求的html文件里可能包含<img src=""></img>等超链接,每个超链接都会发送一个请求
    # GET /index.html HTTP/1.1  GET /images/qt-logo.png HTTP/1.1  GET /classic.css HTTP/1.1  GET /favicon.ico HTTP/1.1
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
        client_socket.send(response_head.encode())
        client_socket.close()
    else:
        # 请求成功
        # Content-Length告诉浏览器本次传输内容长度,浏览器收到body后不断开连接,继续使用当前连接请求新的资源,获取全部资源后浏览器自动断开连接
        response_head = "HTTP/1.1 200 ok\r\n" + "Content-Length:%d\r\n" % len(response_body) + "\r\n"
        client_socket.send(response_head.encode())
        client_socket.send(response_body)


def main():
    """epoll实现并发web服务器(效率极高)"""

    # 1.创建socket对象
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # 2.绑定端口
    server_socket.bind(("", 9999))
    # 3.开启监听
    server_socket.listen(128)
    server_socket.setblocking(False)  # 将该socket设置成非阻塞
    # 创建epoll对象
    epl = select.epoll()
    # 将监听套接字对应的fd注册到epoll中
    epl.register(server_socket.fileno(), select.EPOLLIN)  # select.EPOLLIN检测tcp_server_socket.fileno()是否有输入
    # 存放fd和socket的字典：key是该socket的fd,value是socket
    fd_event_dict = dict()

    while True:
        fd_event_list = epl.poll()  # 默认阻塞,直到os监测到有数据,通过事件通知方式告诉这个程序解阻塞
        for fd, event in fd_event_list:
            # 1.判断是否有新的客户端连接
            if fd == server_socket.fileno():
                # 说明有新的客户端连接tcp_Server
                new_socket, addr = server_socket.accept()
                # 把新的套接字也注册到epoll
                epl.register(new_socket.fileno(), select.EPOLLIN)
                # 往字典里添加fd和对应的socket
                fd_event_dict[new_socket.fileno()] = new_socket
            # 2.判断已连接的客户端是否有消息发过来
            elif event == select.EPOLLIN:
                # 说明已经连接的客户端有消息发过来了,通过fd获取socket接收消息
                request = fd_event_dict[fd].recv(1024).decode("utf-8")
                if request:
                    print(request)
                    service(fd_event_dict[fd], request)
                else:
                    fd_event_dict[fd].close()  # 关闭socket
                    epl.unregister(fd)  # 从epoll中注销该fd
                    fd_event_dict.pop(fd)  # 从字典中删除


if __name__ == '__main__':
    main()