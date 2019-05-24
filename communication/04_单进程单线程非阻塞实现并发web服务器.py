# coding=utf-8
import socket
import time
import re

def theory():
    """单进程单线程使用非阻塞模式实现并发服务器原理"""

    server_socket = socket.socket(...)
    server_socket.setblocking(False)  # 将该socket设置成非阻塞模式
    client_sockets = list()
    while True:
        # 检测有没有新的客户端连接进来
        try:
            new_socket, addr = server_socket.accept()
        except Exception as e:
            print(e)
            print("---异常：当前没有客户端连接---")
        else:
            print("---没报异常说明有客户端连接进来了---")
            new_socket.setblocking(False)  # 将该socket设置成非阻塞模式
            # 将要检测的new_socket添加到列表
            client_sockets.append(new_socket)

        for client_socket in client_sockets:
            # 检测有没有新的消息发送过来
            try:
                recv_data = client_socket.recv(1024)
            except Exception as e:
                print(e)
                print("---异常：客户端还没有消息发送过来---")
            else:
                print("---没报异常说明有消息发送过来了---")
                if recv_data:
                    print("---对方发请求消息过来了---")
                    client_socket.send(...)
                else:
                    print("---对方调用了close,发送了空消息---")
                    # 那么这个socket就没用了,关闭socket并从列表中删除,不然列表会越来越大
                    client_socket.close()
                    client_sockets.remove(client_socket)


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
    """单进程单线程使用非阻塞模式实现并发(效率一般)"""

    # 1.创建socket对象
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # 2.绑定端口
    server_socket.bind(("", 9999))
    # 3.开启监听
    server_socket.listen(128)
    server_socket.setblocking(False)  # 将该socket设置成非阻塞
    client_sockets = list()  # 客户端列表
    while True:
        try:
            # 4.检测是否有新的客户端连接
            new_socket, addr = server_socket.accept()
        except Exception as e:
            # print(e)  # 没有客户端连接就会异常
            pass
        else:
            new_socket.setblocking(False)  # 将该socket设置成非阻塞
            # 将要检测的new_socket添加到列表
            client_sockets.append(new_socket)

        for client_socket in client_sockets:
            try:
                # 5.检测是否有新的消息发送过来
                request = client_socket.recv(1024).decode()
            except Exception as e:
                # print(e)  # 客户端没发消息就会异常
                pass
            else:
                if request:
                    print(request)
                    service(client_socket, request)
                else:
                    # 关闭socket并从列表中删除,不然列表会越来越大
                    client_sockets.remove(client_socket)
                    client_socket.close()


if __name__ == '__main__':
    main()
