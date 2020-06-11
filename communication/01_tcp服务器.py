# coding=utf-8
"""
socket是两台机器间通信的端点,socket编程是基于TCP/IP协议的网络编程
TCP(Transmission Control Protocol)传输控制协议：面向连接的、可靠地、基于字节流的传输层通信协议
UDP(User Datagram Protocol)用户数据包协议：面向数据包的,不建立连接,不可靠会丢包,将数据封包传输(不超过64k)

tcp如何保证传输可靠性？
确认和重传：接收方收到报文会确认,发送方发送一段时间后没有收到确认会重传

tcp连接四要素：local ip, local port, remote ip, remote port
HTTP请求的local IP remote IP remote PORT是固定的,只有local PORT是可变的,可用的local PORT数量就限制了C/S之间的tcp连接数量
查看可使用端口：sysctl -a | grep net.ipv4.ip_local_port_range

seq序列号：tcp是面向字节流的,字节流中的每个字节都按顺序编号,接收方根据编号进行确认,保证原始数据包的位置  ISN初始化序列号
ack确认号：期望收到对方下一个报文段的第一个字节的序列号,确认号ack=x+1表示序列号截止到seq=x的数据都已经收到

ISN(initial sequence number)是固定的吗？
三次握手的一个重要功能是客户端和服务端交换ISN以便让对方知道接下来接收数据的时候如何按序列号组装数据
如果ISN是固定的,攻击者很容易猜出后续的确认号,所以ISN是随机生成的
ISN = M + F(local ip, local port, remote ip, remote port)
M是一个计时器,每隔4毫秒加1   F是一个Hash算法,根据源IP、目的IP、源端口、目的端口生成一个随机数值

标志位：控制tcp连接的状态
SYN同步标志：建立tcp连接时用来同步序列号,SYN=1&ACK=0说明是连接请求报文段,对方同意连接会在响应报文段设置SYN=1&ACK=1
ACK确认标志：发送方发送数据时ACK=0,接收方收到数据后设置ACK=1,建立连接后传输的报文段ACK都为1
FIN结束标志：发送方数据发送完毕,请求释放连接

tcp状态
CLOSED：关闭状态,没有连接
LISTEN：监听状态,等待连接
SYN_SENT：发出连接请求,等待确认
SYN_RECD：收到连接请求,尚未确认
ESTABLISHED：连接建立,传输数据
FIN_WAIT1：(主动方)发送关闭请求,等待对方确认
CLOSE_WAIT：(被动方)收到对方关闭请求,已经确认
FIN_WAIT2：(主动方)收到对方确认,等待对方关闭请求
LAST_ACK：(被动方)发送关闭请求,等待对方最后一个ACK
TIME_WAIT：等待2MSL后没有收到回复说明对方已经关闭

客户端状态变化：CLOSED -> SYN_SENT -> ESTABLISHED -> FIN_WAIT1 -> FIN_WAIT2 -> TIME_WAIT -> CLOSED
服务器状态变化：LISTEN -> SYN_RECD -> ESTABLISHED -> CLOSE_WAIT -> LAST_ACK -> CLOSED

三次握手
1.客户端向服务器发送SYN报文seq=x,此时客户端处于SYN_SENT状态
2.服务器收到SYN报文后会应答SYN+ACK报文seq=y&ack=x+1,表示自己收到了客户端的SYN,此时服务器处于SYN_RECD状态
3.客户端收到SYN+ACK报文后会应答ACK报文seq=x+1&ack=y+1,此时客户端处于ESTABLISHED状态,服务器收到ACK报文后也处于ESTABLISHED状态

四次挥手
1.客户端向服务器发送FIN报文seq=x+2&ack=y+2,此时客户端处于FIN_WAIT1状态
2.服务器收到FIN报文后会应答ACK报文ack=x+3,表明已经收到客户端的FIN,此时服务端处于CLOSE_WAIT状态,客户端处于FIN_WAIT2状态
3.服务器数据发送完毕后也向客户端发送FIN报文seq=y+1,此时服务器处于LAST_ACK状态,等待来自客户端的最后一个ACK报文
4.客户端收到FIN后发送一个ACK报文ack=y+3并进入TIME_WAIT状态,等待可能会出现的ACK重传,服务器收到ACK后关闭连接进入CLOSED状态
  客户端等待2MSL后没有收到服务器的应答,认为服务器已经正常关闭连接,于是自己也关闭连接进入CLOSED状态

三次握手作用
确认客户端和服务端双方的接收和发送能力都正常
指定自己的初始化序列号为后面的可靠传输做准备
如果是HTTPS协议,三次握手的过程还会进行数字证书验证和秘钥加密

Q2.为什么是三次握手不是两次？
第一次握手服务器结论：客户端的发送和服务器的接收是正常的
第二次握手客户端结论：客户端的接收发送和服务器的接收发送都是正常的,但是此时服务器并不确定客户端的接收和服务器的发送是否正常
第三次握手服务器结论：客户端的接收和服务器的发送也是正常的

Q3.什么是半连接队列？
服务器第一次收到客户端的SYN报文后处于SYN_RECD状态,此时双方还没有完全建立连接,服务器会把这种状态下的请求放到半连接队列,已经完成三次握手的会放到全连接队列
SYN-ACK重传次数：如果服务器发送完SYN-ACK包未收到客户端确认便会进行重传,超过最大重传次数(超时时间)就将连接信息从半连接队列中删除

Q4.什么是SYN攻击？
客户端在短时间内伪造大量不存在的ip向服务器不断发送SYN报文,服务器会回复SYN+ACK报文并等待客户端确认,由于源地址不存在服务器得不到回复会不断重发直至超时
这些SYN包长时间占用半连接队列,导致正常的SYN请求因为队列满而被丢弃,从而引起网络阻塞甚至系统瘫痪,属于DOS/DDOS攻击
DOS(denial of service)拒绝服务攻击：在短时间内发送大量请求占用服务器资源导致服务器无法处理正常请求,即拒绝服务
DDOS(distribute denial of service)分布式拒绝服务攻击：控制多台机器同时发动DOS攻击
检测SYN攻击：netstat -anp | grep SYN_RECD
防御SYN攻击：缩短SYN超时时间、建立连接之后再分配TCB(Transmission Control Block)

Q5.三次握手过程中可以携带数据吗？
第三次握手是可以的,第一次和第二次握手不可以.如果第一次握手可以携带数据,攻击者会在第一次握手发送SYN报文时放入大量数据而不用理会服务器的接收发送能力是否正常
然后疯狂重复发送SYN报文,导致服务器消耗很多资源处理这些报文

Q1.为什么挥手需要四次？
因为当Server端收到Client端的SYN连接请求报文后,可以直接发送SYN+ACK报文,其中ACK报文是用来应答的,SYN报文是用来同步的
但是关闭连接时,当Server端收到FIN报文时很可能并不会立即关闭SOCKET,所以只能先回复一个ACK报文告诉Client端你发的FIN报文我收到了,
等到我Server端所有的报文都发送完了我才能发送FIN报文,所以需要四步握手

Q2.为什么TIME_WAIT状态需要经过2MSL(最大报文生存时间)才能返回到CLOSE状态？
1.保证客户端发送的最后一个ACK报文能够到达服务端,这个ACK报文有可能丢失导致处于LAST_ACK状态的服务器收不到对方的确认而无法进入CLOSED状态
2.防止出现"已失效的连接请求报文",等待2MSL可以使本次tcp连接持续时间内产生的所有报文都从网络中消失,下一个新的连接不会出现旧连接的请求报文
"""

import socket

def server():
    # 1.创建socket对象：AF_INET表示ipv4地址,SOCK_STREAM表示TCP协议,SOCK_DGRAM表示UDP协议
    tcp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # 所有socket默认都是阻塞的
    # 2.绑定服务端ip和端口
    tcp_server_socket.bind(("10.16.40.46", 9999))
    # 3.开启监听：TCP必须先启动服务器等待客户端连接,UDP不建立连接无所谓先后顺序
    tcp_server_socket.listen()
    # 外循环响应所有客户端连接
    while True:
        # 4.接收客户端连接,三次握手
        new_socket, addr = tcp_server_socket.accept()  # 阻塞：一直等直到有客户端连接进来
        # print(new_socket)  # <socket.socket fd=836, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM,proto=0, laddr=('10.16.45.68', 9999), raddr=('10.16.45.68', 62413)>  本次连接信息
        # print(addr)  # ('10.16.45.68', 62413)  客户端ip和端口
        # 5.收发数据
        while True:
            # 接收消息
            msg = new_socket.recv(1024).decode()  # 阻塞：一直等直到客户端有消息发送过来
            print(msg)
            if msg == "bye":
                break
            # 发送消息
            info = input(">>>")
            new_socket.send(info.encode())
            if info == "bye":
                break
        # 关闭连接,四次挥手
        new_socket.close()

def client1():
    # 创建socket对象
    tcp_client_socket = socket.socket()
    # 连接服务器
    tcp_client_socket.connect(("10.16.40.46", 9999))
    # 循环保持和服务器会话
    while True:
        # 发送消息
        info = input(">>>")
        tcp_client_socket.send(info.encode())
        if info == "bye":
            break
        # 接收消息
        msg = tcp_client_socket.recv(1024).decode()
        print(msg)
        # 退出循环条件
        if msg == "bye":
            break
    # 关闭客户端
    tcp_client_socket.close()

def client2():
    # 创建socket对象
    tcp_client_socket = socket.socket()
    # 连接服务器
    tcp_client_socket.connect(("10.16.45.68", 9999))
    # 循环保持和服务器会话
    while True:
        # 发送消息
        info = input(">>>")
        tcp_client_socket.send(info.encode())
        if info == "bye":
            break
        # 接收消息
        msg = tcp_client_socket.recv(1024).decode()
        print(msg)
        # 退出循环条件
        if msg == "bye":
            break
    # 关闭客户端
    tcp_client_socket.close()


if __name__ == '__main__':
    # server()
    client1()
    # client2()
