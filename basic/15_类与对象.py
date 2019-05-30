# coding=utf-8
"""
反射：通过字符串的形式动态导入模块,操作模块中的属性/函数,是一种基于字符串的事件驱动,常用于web框架路由
     module = __import__("module_name") <==> import module_ame
     __import__搜索模块
     import搜索模块并绑定到局部变量,import就是调用了__import__完成模块的检索
     4个内置函数：查找hasattr(obj,name)
                获取getattr(obj,name)
                添加setattr(obj,name,value)
                删除delattr(obj,name)

"""