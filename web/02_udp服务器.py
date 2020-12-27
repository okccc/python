# coding=utf-8
import socket

def server():
    # 1.创建socket对象,指定UDP
    udp_server_socket = socket.socket(type=socket.SOCK_DGRAM)
    # 2.绑定ip和端口
    udp_server_socket.bind(("10.16.45.68", 9999))
    # UDP的server不需要监听也不需要建立连接
    while True:
        # 3.接收客户端消息,包含客户端地址信息
        msg, addr = udp_server_socket.recvfrom(1024)  # 阻塞直到有客户端发消息过来
        print(msg.decode())
        # print(addr)  # ('10.16.45.68', 56032)
        # 指定客户端地址发送消息
        info = input(">>>")
        udp_server_socket.sendto(info.encode(), addr)

def client1():
    # 创建socket对象,指定UDP
    udp_client_socket = socket.socket(type=socket.SOCK_DGRAM)
    while True:
        # 指定服务端地址发送消息,同时也会将自己的地址发送过去
        info = input(">>>")
        udp_client_socket.sendto(info.encode(), ("10.16.45.68", 9999))
        if info == "bye":
            break
        # 接收消息
        msg, addr = udp_client_socket.recvfrom(1024)
        print(msg.decode())
        if msg.decode() == "bye":
            break

def client2():
    # 创建socket对象,指定UDP
    udp_client_socket = socket.socket(type=socket.SOCK_DGRAM)
    while True:
        # 指定服务端地址发送消息,同时也会将自己的地址发送过去
        info = input(">>>")
        udp_client_socket.sendto(info.encode(), ("10.16.45.68", 9999))
        if info == "bye":
            break
        # 接收消息
        msg, addr = udp_client_socket.recvfrom(1024)
        print(msg.decode())
        if msg.decode() == "bye":
            break


if __name__ == '__main__':
    # server()
    # client1()
    client2()