# coding=utf-8
import time

def login():
    return "---登录页面 %s---" % time.ctime()

def register():
    return "---注册页面 %s---" % time.ctime()

def profile():
    return "---个人中心页面 %s---" % time.ctime()

def application(filename):
    if filename == "/login.py":
        return login()
    elif filename == "/register.py":
        return register()
    elif filename == "/profile.py":
        return profile()
    else:
        return "---当前请求页面无效---"
