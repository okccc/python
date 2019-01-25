# coding=utf-8
"""
python有一套很有用的标准库
标准库                说明
builtins             内置函数
os                   操作系统接口
sys                  python自身运行环境
functools            常用工具
json                 编码和解码json对象
logging              记录日志,调试
multiprocessing      多进程
threading            多线程
copy                 拷贝
time                 时间
datetime             日期和时间
calendar             日历
hashlib              加密算法
random               随机数
re                   字符串正则匹配
socket               Sockets API
shutil               文件和目录管理
glob                 基于文件通配符搜索
"""
import hashlib

"""
hashlib: 加密算法,常用于登录注册
"""
# 创建hash对象,md5(message-Digest Algorithm 5)消息摘要算法,得到一个128bit=16byte=32位的密文
m = hashlib.md5()
print(m)  # <md5 HASH object @ 0x0000020D5C1709E0>
# 以字符串参数更新hash对象
m.update("hello".encode("utf-8"))
# 返回十六进制数字字符串
print(m.hexdigest())  # 5d41402abc4b2a76b9719d911017c592
# 不管如何更新hash对象,最终返回的都是32位长度的一串数值
m.update("jhsahdskdsadaldw".encode("utf-8"))
print(m.hexdigest())  # 0bec77eeeedd61ea5db95c0202b68d45

