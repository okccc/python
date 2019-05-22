# coding=utf-8
"""
socket是两台机器间通信的端点,socket编程是基于TCP/IP协议的网络编程
TCP协议：面向连接的字节流传输,建立长连接(3次握手,4次挥手)形成通道,可靠不丢包,适用于传输较大数据,拆包时可能会黏包
UDP协议：面向数据包的,不建立连接,不可靠会丢包,将数据封包传输(不超过64k)
socket是全双工的,有两个通道,可以同时收发数据;关闭时每个方向要单独关闭,所以是四次挥手
"""
import socket

def server():
    # 1.创建socket对象：AF_INET表示ipv4地址,SOCK_STREAM表示TCP协议,SOCK_DGRAM表示UDP协议
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # 2.绑定服务端ip和端口
    s.bind(("10.16.45.68", 9999))
    # 3.开启监听：TCP必须先启动服务器等待客户端连接,UDP不建立连接无所谓先后顺序
    s.listen()
    # 外循环响应所有客户端连接
    while True:
        # 4.接收客户端连接,三次握手
        conn, addr = s.accept()  # 阻塞模式：必须三次握手成功,tcp协议一次只能和一个人聊
        # print(conn)  # <socket.socket fd=836, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM,proto=0, laddr=('10.16.45.68', 9999), raddr=('10.16.45.68', 62413)>  本次连接信息
        # print(addr)  # ('10.16.45.68', 62413)  客户端ip和端口
        # 5.收发数据
        while True:
            # 接收消息
            msg = conn.recv(1024).decode()
            print(msg)
            if msg == "bye":
                break
            # 发送消息
            info = input(">>>")
            conn.send(info.encode())
            if info == "bye":
                break
        # 关闭连接,四次挥手
        conn.close()

def client1():
    # 创建socket对象
    s = socket.socket()
    # 连接服务器
    s.connect(("10.16.45.68", 9999))
    # 循环保持和服务器会话
    while True:
        # 发送消息
        info = input(">>>")
        s.send(info.encode())
        if info == "bye":
            break
        # 接收消息
        msg = s.recv(1024).decode()
        print(msg)
        # 退出循环条件
        if msg == "bye":
            break
    # 关闭客户端
    s.close()

def client2():
    # 创建socket对象
    s = socket.socket()
    # 连接服务器
    s.connect(("10.16.45.68", 9999))
    # 循环保持和服务器会话
    while True:
        # 发送消息
        info = input(">>>")
        s.send(info.encode())
        if info == "bye":
            break
        # 接收消息
        msg = s.recv(1024).decode()
        print(msg)
        # 退出循环条件
        if msg == "bye":
            break
    # 关闭客户端
    s.close()


if __name__ == '__main__':
    # server()
    # client1()
    client2()
